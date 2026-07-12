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
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/actions.xml',
        'views/root_menu.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
