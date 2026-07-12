# -*- coding: utf-8 -*-
{
    'name': 'AssetFlow - Enterprise Asset & Resource Management',
    'version': '18.0.1.0.0',
    'category': 'Operations/Assets',
    'summary': 'Simplify, digitize, track, allocate, and maintain physical assets and shared resources.',
    'description': """
AssetFlow ERP Module
====================
A comprehensive ERP solution built for the Odoo Hackathon to track, allocate, and maintain organization-wide physical assets.

Key Foundations Established:
- Security groups (Employee, Department Head, Asset Manager, Admin)
- Structural master menus
- Base models (Departments, Categories, Extended Users)
    """,
    'author': 'Priyam (Team Leader), Hackathon Team',
    'website': 'https://github.com/AssetFlow',
    'depends': ['base'],
    'data': [
        'data/department_sequence.xml',
        'data/asset_sequence.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'views/actions.xml',
        'views/department_views.xml',
        'views/category_views.xml',
        'views/employee_views.xml',
        'views/asset_views.xml',
        'views/allocation_views.xml',
        'views/transfer_views.xml',
        'views/notification_views.xml',
        'views/booking_views.xml',
<<<<<<< Updated upstream
=======
        'views/maintenance_views.xml',
>>>>>>> Stashed changes
        'views/dashboard.xml',
        'views/root_menu.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'assetflow/static/src/scss/dashboard.scss',
            'assetflow/static/src/js/dashboard.js',
            'assetflow/static/src/xml/dashboard_templates.xml',
            'assetflow/views/dashboard_booking.xml',
<<<<<<< Updated upstream
=======
            'assetflow/views/maintenance_dashboard.xml',
>>>>>>> Stashed changes
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
