# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'syscoon Finance-Export',
    'version': '9.0.0.2',
    'category': 'Accounting',
    'author': 'Mathias Neef',
    'description': """
Generates a CSV-Export for Datev and other German Accounting Programms.
    """,
    'sequence': 190,
    'website': 'http://syscoon.com',
    'depends' : ['account'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'data/scheduler.xml',
        'views/menu.xml',
        'views/key.xml',
        'views/auto_account.xml',
        'views/move.xml',
        'views/configuration.xml',
        'views/logger.xml',
        'views/exports.xml',
        'wizard/move_create_view.xml',
        'wizard/move_unlink_view.xml',
        'wizard/move_export_view.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}