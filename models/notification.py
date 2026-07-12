# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AssetFlowNotification(models.Model):
    _name = 'assetflow.notification'
    _description = 'System Notification'
    _order = 'create_date desc'

    title = fields.Char(string='Title', required=True)
    message = fields.Text(string='Message', required=True)
    user_id = fields.Many2one('res.users', string='Recipient User', required=True, index=True)
    is_read = fields.Boolean(string='Read', default=False, index=True)
    
    notif_type = fields.Selection([
        ('assigned', 'Asset Assigned'),
        ('maint_appr', 'Maintenance Approved'),
        ('maint_rej', 'Maintenance Rejected'),
        ('book_conf', 'Booking Confirmed'),
        ('book_canc', 'Booking Cancelled'),
        ('book_rem', 'Booking Reminder'),
        ('trf_appr', 'Transfer Approved'),
        ('overdue', 'Overdue Return'),
        ('audit_disc', 'Audit Discrepancy')
    ], string='Notification Type', required=True, index=True)
    
    module = fields.Selection([
        ('asset', 'Assets'),
        ('allocation', 'Allocations'),
        ('booking', 'Bookings'),
        ('maintenance', 'Maintenance'),
        ('audit', 'Audit'),
        ('general', 'General')
    ], string='Related Module', required=True, default='general')

    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], string='Priority', default='low', required=True, index=True)

    status = fields.Selection([
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed')
    ], string='Status', default='pending', required=True)


class AssetFlowActivityLog(models.Model):
    _name = 'assetflow.activity.log'
    _description = 'User Activity Log'
    _order = 'timestamp desc'

    user_id = fields.Many2one('res.users', string='Actor', required=True, index=True)
    action = fields.Char(string='Action', required=True)
    timestamp = fields.Datetime(string='Date & Time', required=True, default=fields.Datetime.now)
    description = fields.Text(string='Description')
    
    module = fields.Selection([
        ('asset', 'Assets'),
        ('allocation', 'Allocations'),
        ('booking', 'Bookings'),
        ('maintenance', 'Maintenance'),
        ('audit', 'Audit'),
        ('system', 'System')
    ], string='Module', required=True, default='system')
