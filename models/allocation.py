# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AssetFlowAllocation(models.Model):
    _name = 'assetflow.allocation'
    _description = 'Asset Allocation Log'
    _order = 'allocation_date desc'

    asset_id = fields.Many2one('assetflow.asset', string='Asset', required=True, index=True)
    assignee_type = fields.Selection([
        ('employee', 'Employee'),
        ('department', 'Department')
    ], string='Assignee Type', required=True, default='employee')
    
    employee_id = fields.Many2one('res.users', string='Employee', domain="[('share', '=', False)]")
    department_id = fields.Many2one('assetflow.department', string='Department')
    
    allocation_date = fields.Date(string='Allocation Date', required=True, default=fields.Date.context_today)
    expected_return_date = fields.Date(string='Expected Return Date')
    actual_return_date = fields.Date(string='Actual Return Date')
    check_in_notes = fields.Text(string='Check-in Notes')
    
    status = fields.Selection([
        ('active', 'Active'),
        ('returned', 'Returned'),
        ('transferred', 'Transferred')
    ], string='Status', default='active', required=True, index=True)

    @api.constrains('assignee_type', 'employee_id', 'department_id')
    def _check_assignee_presence(self):
        for rec in self:
            if rec.assignee_type == 'employee' and not rec.employee_id:
                raise ValidationError(_('Assignee type is Employee but no Employee was selected.'))
            if rec.assignee_type == 'department' and not rec.department_id:
                raise ValidationError(_('Assignee type is Department but no Department was selected.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            asset = self.env['assetflow.asset'].browse(vals.get('asset_id'))
            if not asset.exists():
                raise ValidationError(_('The requested asset does not exist.'))
            if asset.status != 'available':
                raise ValidationError(_('Asset %s is already allocated.') % asset.asset_tag)
            
            # Lock the asset status
            asset.write({
                'status': 'allocated',
                'employee_id': vals.get('employee_id') if vals.get('assignee_type') == 'employee' else False,
                'department_id': vals.get('department_id') if vals.get('assignee_type') == 'department' else False,
            })
        return super(AssetFlowAllocation, self).create(vals_list)

    def action_return(self, check_in_notes=False, condition='excellent'):
        for rec in self:
            if rec.status != 'active':
                raise ValidationError(_('Only active allocations can be returned.'))
            
            rec.write({
                'status': 'returned',
                'actual_return_date': fields.Date.context_today(self),
                'check_in_notes': check_in_notes
            })
            rec.asset_id.write({
                'status': 'available',
                'employee_id': False,
                'department_id': False,
                'condition': condition
            })
        return True
