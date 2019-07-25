# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Tours',
    'category': 'Hidden',
    'description': """
Odoo Web tours.
========================

""",
    'version': '1.0.190724',
    'depends': ['web'],
    'data': [
        'security/ir.model.access.csv',
        'views/tour_templates.xml',
        'views/tour_views.xml'
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'auto_install': False
}
