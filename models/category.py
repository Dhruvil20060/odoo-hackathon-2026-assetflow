# -*- coding: utf-8 -*-
from odoo import models, fields

class AssetFlowCategory(models.Model):
    _name = 'assetflow.category'
    _description = 'AssetFlow Asset Category'

    name = fields.Char(string='Category Name', required=True)
    description = fields.Text(string='Description')
    custom_field_ids = fields.One2many(
        'assetflow.category.field', 
        'category_id', 
        string='Custom Fields',
        help="Specify category-specific dynamic fields (e.g. Warranty period for Electronics)"
    )

class AssetFlowCategoryField(models.Model):
    _name = 'assetflow.category.field'
    _description = 'AssetFlow Category Custom Field Definition'

    category_id = fields.Many2one('assetflow.category', string='Category', ondelete='cascade', required=True)
    name = fields.Char(string='Field Name', required=True, help="e.g., Warranty Period (months), License Plate")
    field_type = fields.Selection([
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('boolean', 'Boolean')
    ], string='Field Type', default='text', required=True)
    is_required = fields.Boolean(string='Required', default=False)
