# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AssetFlowDepartment(models.Model):
    _name = 'assetflow.department'
    _description = 'Department Management'
    _parent_store = True
    _parent_name = 'parent_id'
    _order = 'name'

    name = fields.Char(string='Department Name', required=True, index=True)
    code = fields.Char(string='Department Code', required=True, copy=False, index=True, default='/')
    head_id = fields.Many2one('res.users', string='Department Head', domain="[('share', '=', False)]")
    parent_id = fields.Many2one('assetflow.department', string='Parent Department', ondelete='restrict', index=True)
    parent_path = fields.Char(index=True)
    
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Status', default='active', required=True)
    
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'The department code must be unique!'),
    ]

    @api.constrains('parent_id')
    def _verify_no_recursive_loops(self):
        if not self._check_recursion():
            raise ValidationError(_('Error! You cannot create recursive departments.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('code') or vals.get('code') == '/':
                vals['code'] = self.env['ir.sequence'].next_by_code('assetflow.department') or '/'
            if 'code' in vals:
                vals['code'] = vals['code'].upper().strip()
        return super(AssetFlowDepartment, self).create(vals_list)

    def write(self, vals):
        if 'code' in vals:
            vals['code'] = vals['code'].upper().strip()
        return super(AssetFlowDepartment, self).write(vals)
