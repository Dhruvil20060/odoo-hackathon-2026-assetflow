# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AssetFlowAsset(models.Model):
    _name = 'assetflow.asset'
    _description = 'Asset Inventory'
    _order = 'asset_tag desc'

    name = fields.Char(string='Asset Name', required=True, index=True)
    asset_tag = fields.Char(string='Asset Tag', required=True, copy=False, index=True, default='/')
    serial_number = fields.Char(string='Serial Number', index=True)
    category_id = fields.Many2one('assetflow.category', string='Category', required=True, index=True)
    department_id = fields.Many2one('assetflow.department', string='Department')
    employee_id = fields.Many2one('res.users', string='Assigned Employee', domain="[('share', '=', False)]")
    
    acquisition_date = fields.Date(string='Acquisition Date', default=fields.Date.context_today)
    acquisition_cost = fields.Float(string='Acquisition Cost')
    condition = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor')
    ], string='Condition', default='excellent', required=True)
    location = fields.Char(string='Current Location')
    is_bookable = fields.Boolean(string='Shared / Bookable Asset', default=False)
    
    status = fields.Selection([
        ('available', 'Available'),
        ('allocated', 'Allocated'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Under Maintenance'),
        ('lost', 'Lost'),
        ('retired', 'Retired'),
        ('disposed', 'Disposed')
    ], string='Status', default='available', required=True, index=True)
    
    description = fields.Text(string='Description')
    notes = fields.Text(string='Notes')
    photo = fields.Binary(string='Photo')
    document_ids = fields.Many2many('ir.attachment', string='Documents')

    _sql_constraints = [
        ('tag_unique', 'unique(asset_tag)', 'The asset tag must be unique!'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('asset_tag') or vals.get('asset_tag') == '/':
                vals['asset_tag'] = self.env['ir.sequence'].next_by_code('assetflow.asset') or '/'
        return super(AssetFlowAsset, self).create(vals_list)
