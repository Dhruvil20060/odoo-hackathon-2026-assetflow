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
        # Default signup is strictly Employee role
        for vals in vals_list:
            vals['role'] = 'employee'
        users = super(ResUsers, self).create(vals_list)
        for user in users:
            user._sync_role_groups()
        return users

    def write(self, vals):
        res = super(ResUsers, self).write(vals)
        if 'role' in vals or 'status' in vals:
            for user in self:
                user._sync_role_groups()
        return res

    def _sync_role_groups(self):
        self.ensure_one()
        g_emp = self.env.ref('assetflow.group_employee', raise_if_not_found=False)
        g_head = self.env.ref('assetflow.group_dept_head', raise_if_not_found=False)
        g_mgr = self.env.ref('assetflow.group_asset_manager', raise_if_not_found=False)
        g_adm = self.env.ref('assetflow.group_admin', raise_if_not_found=False)

        if not all([g_emp, g_head, g_mgr, g_adm]):
            return

        to_add = self.env['res.groups']
        to_remove = self.env['res.groups']

        if self.status == 'inactive':
            to_remove = g_emp + g_head + g_mgr + g_adm
        else:
            if self.role == 'employee':
                to_add = g_emp
                to_remove = g_head + g_mgr + g_adm
            elif self.role == 'dept_head':
                to_add = g_head
                to_remove = g_mgr + g_adm
            elif self.role == 'asset_manager':
                to_add = g_mgr
                to_remove = g_adm
            elif self.role == 'admin':
                to_add = g_adm

        if to_add:
            self.write({'groups_id': [(4, g.id) for g in to_add]})
        if to_remove:
            self.write({'groups_id': [(3, g.id) for g in to_remove]})
