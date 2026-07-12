# -*- coding: utf-8 -*-
from odoo import models, fields

class AssetFlowDepartment(models.Model):
    _name = 'assetflow.department'
    _description = 'AssetFlow Department'
    _parent_store = True # Enable hierarchy parent stores
    _parent_name = 'parent_id'

    name = fields.Char(string='Department Name', required=True)
    head_id = fields.Many2one(
        'res.users', 
        string='Department Head', 
        domain="[('share', '=', False)]",
        help="Assign a Department Head from existing internal employee accounts"
    )
    parent_id = fields.Many2one(
        'assetflow.department', 
        string='Parent Department', 
        ondelete='restrict', 
        index=True
    )
    # parent_path is required for Odoo standard hierarchy functions
    parent_path = fields.Char(index=True)
    
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Status', default='active', required=True)
    
    active = fields.Boolean(default=True, help="Set to inactive to archive this department")

    # Simple name get override for tree lists
    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.parent_id:
                name = f"{record.parent_id.name} / {name}"
            result.append((record.id, name))
        return result
