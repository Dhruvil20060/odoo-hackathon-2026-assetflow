# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AssetFlowCategory(models.Model):
    _name = 'assetflow.category'
    _description = 'Asset Category Management'
    _order = 'name'

    name = fields.Char(string='Category Name', required=True, index=True)
    description = fields.Text(string='Description')
    warranty_period = fields.Integer(string='Warranty Period (months)', help="Warranty coverage length in months")
    
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Status', default='active', required=True)
    
    active = fields.Boolean(string='Active', default=True)

    @api.constrains('warranty_period')
    def _validate_warranty_period(self):
        for rec in self:
            if rec.warranty_period < 0:
                raise ValidationError(_('Warranty period cannot be negative.'))
