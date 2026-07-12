# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AssetFlowAuditCycle(models.Model):
    _name = 'assetflow.audit.cycle'
    _description = 'Asset Audit Cycle'
    _order = 'date_start desc'

    name = fields.Char(string='Audit Cycle Number', required=True, copy=False, index=True, default='/')
    audit_name = fields.Char(string='Audit Name', required=True)
    scope = fields.Selection([
        ('department', 'Department'),
        ('location', 'Location')
    ], string='Scope', required=True, default='department')
    
    department_id = fields.Many2one('assetflow.department', string='Department')
    location = fields.Char(string='Scope Location')
    
    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.context_today)
    date_end = fields.Date(string='End Date', required=True)
    
    auditor_ids = fields.Many2many('res.users', string='Assigned Auditors', domain="[('share', '=', False)]")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed')
    ], string='Status', default='draft', required=True, index=True)

    record_ids = fields.One2many('assetflow.audit.record', 'cycle_id', string='Audit Records')
    discrepancy_ids = fields.One2many('assetflow.audit.discrepancy', 'cycle_id', string='Audit Discrepancies')

    @api.constrains('scope', 'department_id', 'location')
    def _check_scope_data(self):
        for rec in self:
            if rec.scope == 'department' and not rec.department_id:
                raise ValidationError(_("Please select a Department for the audit scope."))
            if rec.scope == 'location' and not rec.location:
                raise ValidationError(_("Please input a Scope Location for the audit scope."))

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for rec in self:
            if rec.date_start and rec.date_end and rec.date_start > rec.date_end:
                raise ValidationError(_("The audit start date cannot be later than the end date."))

    @api.constrains('status', 'scope', 'department_id', 'location', 'date_start', 'date_end')
    def _check_duplicate_active_cycles(self):
        for rec in self:
            if rec.status in ('draft', 'in_progress', 'completed'):
                domain = [
                    ('id', '!=', rec.id),
                    ('status', 'in', ('draft', 'in_progress', 'completed')),
                    ('scope', '=', rec.scope),
                    ('date_start', '<=', rec.date_end),
                    ('date_end', '>=', rec.date_start)
                ]
                if rec.scope == 'department':
                    domain.append(('department_id', '=', rec.department_id.id))
                else:
                    domain.append(('location', '=', rec.location))
                
                duplicates = self.search(domain)
                if duplicates:
                    raise ValidationError(_(
                        "An active audit cycle already covers this scope and period (Cycle: %s)."
                    ) % duplicates[0].name)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals.get('name') == '/':
                seq = self.env['ir.sequence'].next_by_code('assetflow.audit.cycle')
                if not seq:
                    count = self.search_count([]) + 1
                    seq = 'AUD-%s' % str(count).zfill(4)
                vals['name'] = seq
        return super(AssetFlowAuditCycle, self).create(vals_list)

    def action_start(self):
        for rec in self:
            if rec.status != 'draft':
                raise ValidationError(_("Only draft audit cycles can be started."))
            
            # Find assets in scope
            domain = []
            if rec.scope == 'department':
                domain.append(('department_id', '=', rec.department_id.id))
            else:
                domain.append(('location', '=', rec.location))
            
            assets = self.env['assetflow.asset'].search(domain)
            if not assets:
                raise ValidationError(_("No assets found in the specified scope."))

            # Auto-populate records
            records_vals = []
            for asset in assets:
                records_vals.append({
                    'cycle_id': rec.id,
                    'asset_id': asset.id,
                    'verification_status': 'verified',
                    'audit_date': fields.Date.context_today(self)
                })
            
            if records_vals:
                self.env['assetflow.audit.record'].create(records_vals)
                
            rec.write({'status': 'in_progress'})
        return True

    def action_complete(self):
        for rec in self:
            if rec.status != 'in_progress':
                raise ValidationError(_("Only cycles in progress can be completed."))
            
            # Generate discrepancies
            rec.discrepancy_ids.unlink() # Clear previous
            discrepancies_vals = []
            for record in rec.record_ids:
                if record.verification_status in ('missing', 'damaged'):
                    discrepancies_vals.append({
                        'cycle_id': rec.id,
                        'asset_id': record.asset_id.id,
                        'record_id': record.id,
                        'discrepancy_type': record.verification_status,
                        'notes': record.notes
                    })
            
            if discrepancies_vals:
                self.env['assetflow.audit.discrepancy'].create(discrepancies_vals)
                
            rec.write({'status': 'completed'})
        return True

    def action_close(self):
        for rec in self:
            if rec.status != 'completed':
                raise ValidationError(_("Only completed audit cycles can be closed."))
            
            # Update affected assets
            for record in rec.record_ids:
                if record.verification_status == 'missing':
                    record.asset_id.write({'status': 'lost'})
            
            rec.write({'status': 'closed'})
        return True


class AssetFlowAuditRecord(models.Model):
    _name = 'assetflow.audit.record'
    _description = 'Asset Audit Verification Record'
    _order = 'audit_date desc'

    cycle_id = fields.Many2one('assetflow.audit.cycle', string='Audit Cycle', required=True, ondelete='cascade', index=True)
    asset_id = fields.Many2one('assetflow.asset', string='Asset', required=True, index=True)
    auditor_id = fields.Many2one('res.users', string='Auditor', default=lambda self: self.env.user)
    
    verification_status = fields.Selection([
        ('verified', 'Verified'),
        ('missing', 'Missing'),
        ('damaged', 'Damaged')
    ], string='Verification Status', required=True, default='verified')
    
    notes = fields.Text(string='Notes')
    audit_date = fields.Date(string='Audit Date', required=True, default=fields.Date.context_today)


class AssetFlowAuditDiscrepancy(models.Model):
    _name = 'assetflow.audit.discrepancy'
    _description = 'Audit Discrepancy Record'
    _order = 'create_date desc'

    cycle_id = fields.Many2one('assetflow.audit.cycle', string='Audit Cycle', required=True, ondelete='cascade', index=True)
    asset_id = fields.Many2one('assetflow.asset', string='Asset', required=True, index=True)
    record_id = fields.Many2one('assetflow.audit.record', string='Verification Source', required=True, ondelete='cascade')
    
    discrepancy_type = fields.Selection([
        ('missing', 'Missing'),
        ('damaged', 'Damaged')
    ], string='Discrepancy Type', required=True)
    
    status = fields.Selection([
        ('pending', 'Pending Resolution'),
        ('resolved', 'Resolved')
    ], string='Resolution Status', default='pending', required=True)
    
    notes = fields.Text(string='Resolution Notes')
