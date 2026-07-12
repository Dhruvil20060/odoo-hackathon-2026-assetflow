# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    department_id = fields.Many2one('assetflow.department', string='Department')
    
    role = fields.Selection([
        ('employee', 'Employee'),
        ('dept_head', 'Department Head'),
        ('asset_manager', 'Asset Manager'),
        ('admin', 'Admin')
    ], string='Role', default='employee', required=True)
    
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Status', default='active', required=True)

    @api.model_create_multi
    def create(self, vals_list):
        users = super(ResUsers, self).create(vals_list)
        for user in users:
            user._sync_security_groups()
        return users

    def write(self, vals):
        res = super(ResUsers, self).write(vals)
        if 'role' in vals or 'status' in vals:
            for user in self:
                user._sync_security_groups()
        return res

    def _sync_security_groups(self):
        """Synchronizes Odoo XML groups based on the custom role field selection."""
        self.ensure_one()
        
        # Load references to the XML groups
        group_emp = self.env.ref('assetflow.group_employee', raise_if_not_found=False)
        group_head = self.env.ref('assetflow.group_dept_head', raise_if_not_found=False)
        group_mgr = self.env.ref('assetflow.group_asset_manager', raise_if_not_found=False)
        group_adm = self.env.ref('assetflow.group_admin', raise_if_not_found=False)

        if not all([group_emp, group_head, group_mgr, group_adm]):
            return # Skip if security groups are not loaded yet (e.g. during module install)

        # Map role selections to target groups to add
        groups_to_add = self.env['res.groups']
        groups_to_remove = self.env['res.groups']

        # Determine alignment
        if self.status == 'inactive':
            # Remove all custom security access on deactivation
            groups_to_remove = group_emp + group_head + group_mgr + group_adm
        else:
            if self.role == 'employee':
                groups_to_add = group_emp
                groups_to_remove = group_head + group_mgr + group_adm
            elif self.role == 'dept_head':
                groups_to_add = group_head
                groups_to_remove = group_mgr + group_adm
            elif self.role == 'asset_manager':
                groups_to_add = group_mgr
                groups_to_remove = group_adm
            elif self.role == 'admin':
                groups_to_add = group_adm

        # Execute assignment changes
        if groups_to_add:
            self.write({'groups_id': [(4, g.id) for g in groups_to_add]})
        if groups_to_remove:
            self.write({'groups_id': [(3, g.id) for g in groups_to_remove]})
