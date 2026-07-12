# -*- coding: utf-8 -*-
from odoo import models, api

class AssetFlowDashboardModel(models.AbstractModel):
    _name = 'assetflow.dashboard'
    _description = 'AssetFlow Dashboard Data Bridge'

    @api.model
    def get_dashboard_stats(self):
        """
        Exposes static placeholder datasets matching Screen 2 requirements.
        Other developers can override this method to fetch actual database aggregates.
        """
        # Count available / allocated assets
        assets = self.env['assetflow.asset'].search([]) if self.env.registry.get('assetflow.asset') else []
        avail_count = len([a for a in assets if a.status == 'available']) if assets else 27
        alloc_count = len([a for a in assets if a.status == 'allocated']) if assets else 56

        return {
            'kpis': {
                'available': avail_count,
                'allocated': alloc_count,
                'maintenance_today': 3,
                'active_bookings': 8,
                'pending_transfers': 2,
                'upcoming_returns': 12,
            },
            'alert': {
                'message': '1 Overdue returns active - flagged for follow-up'
            },
            'activities': [
                {'id': 1, 'desc': 'Laptop AF-0114 allocated to Priya from Engineering', 'time': '2 hours ago'},
                {'id': 2, 'desc': 'Room B2 - booking confirmed - 2:00 to 3:00 PM', 'time': '4 hours ago'},
                {'id': 3, 'desc': 'Projector AF-0056 - maintenance resolved', 'time': '1 day ago'}
            ]
        }
