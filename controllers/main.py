# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class AssetFlowController(http.Controller):
    """
    AssetFlow Controller Foundation.
    Provides standard base endpoints for session management, dynamic attributes, 
    and hooks that other developers can use for dashboard statistics API requests.
    """

    @http.route('/assetflow/session_info', type='json', auth='user', methods=['POST'])
    def session_info(self):
        """Returns the current logged-in employee profile information."""
        user = request.env.user
        return {
            'uid': user.id,
            'name': user.name,
            'email': user.login,
            'role': user.role,
            'status': user.status,
            'department': {
                'id': user.department_id.id,
                'name': user.department_id.name
            } if user.department_id else None
        }
