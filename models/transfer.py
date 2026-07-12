# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AssetFlowTransfer(models.Model):
    _name = 'assetflow.transfer'
    _description = 'Asset Transfer Request'
    _order = 'requested_date desc'

    asset_id = fields.Many2one('assetflow.asset', string='Asset', required=True, index=True)
    requestor_id = fields.Many2one('res.users', string='Requestor', required=True, default=lambda self: self.env.user)
    
    target_assignee_type = fields.Selection([
        ('employee', 'Employee'),
        ('department', 'Department')
    ], string='Target Assignee Type', required=True, default='employee')
    
    target_employee_id = fields.Many2one('res.users', string='Target Employee', domain="[('share', '=', False)]")
    target_department_id = fields.Many2one('assetflow.department', string='Target Department')
    
    reason = fields.Text(string='Reason for Transfer')
    requested_date = fields.Date(string='Requested Date', required=True, default=fields.Date.context_today)
    
    status = fields.Selection([
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('reallocated', 'Reallocated'),
        ('rejected', 'Rejected')
    ], string='Status', default='requested', required=True, index=True)

    @api.constrains('target_assignee_type', 'target_employee_id', 'target_department_id')
    def _check_target_presence(self):
        for rec in self:
            if rec.target_assignee_type == 'employee' and not rec.target_employee_id:
                raise ValidationError(_('Target assignee type is Employee but no Employee was selected.'))
            if rec.target_assignee_type == 'department' and not rec.target_department_id:
                raise ValidationError(_('Target assignee type is Department but no Department was selected.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            asset = self.env['assetflow.asset'].browse(vals.get('asset_id'))
            if not asset.exists():
                raise ValidationError(_('The requested asset does not exist.'))
            if asset.status != 'allocated':
                raise ValidationError(_('Transfer requests can only be raised for currently allocated assets.'))
            
            # Check for existing pending transfer requests
            pending = self.search([
                ('asset_id', '=', asset.id),
                ('status', 'in', ('requested', 'approved'))
            ])
            if pending:
                raise ValidationError(_('A transfer request is already pending for asset %s.') % asset.asset_tag)
                
        return super(AssetFlowTransfer, self).create(vals_list)

    def action_approve(self):
        for rec in self:
            if rec.status != 'requested':
                raise ValidationError(_('Only requested transfers can be approved.'))
            rec.write({'status': 'approved'})
        return True

    def action_reject(self):
        for rec in self:
            if rec.status != 'requested':
                raise ValidationError(_('Only requested transfers can be rejected.'))
            rec.write({'status': 'rejected'})
        return True

    def action_reallocate(self):
        for rec in self:
            if rec.status != 'approved':
                raise ValidationError(_('Only approved transfers can be reallocated.'))
            
            # Find the active allocation
            active_alloc = self.env['assetflow.allocation'].search([
                ('asset_id', '=', rec.asset_id.id),
                ('status', '=', 'active')
            ], limit=1)
            
            if not active_alloc:
                raise ValidationError(_('No active allocation found for asset %s.') % rec.asset_id.asset_tag)
            
            # Close the current active allocation
            active_alloc.write({
                'status': 'transferred',
                'actual_return_date': fields.Date.context_today(self),
                'check_in_notes': _('Closed via transfer request %s') % rec.id
            })

            # Temporarily release the asset status block to allow creation trigger
            rec.asset_id.write({'status': 'available'})

            # Create the new allocation mapping
            self.env['assetflow.allocation'].create({
                'asset_id': rec.asset_id.id,
                'assignee_type': rec.target_assignee_type,
                'employee_id': rec.target_employee_id.id,
                'department_id': rec.target_department_id.id,
                'allocation_date': fields.Date.context_today(self),
                'status': 'active'
            })

            # Update transfer record state
            rec.write({'status': 'reallocated'})
            
        return True
