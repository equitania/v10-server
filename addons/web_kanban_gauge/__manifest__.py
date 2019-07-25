# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Gauge Widget for Kanban',
    'category': 'Hidden',
    'description': """
This widget allows to display gauges using d3 library.
""",
    'version': '1.0.190724',
    'depends': ['web_kanban'],
    'data' : [
        'views/web_kanban_gauge_templates.xml',
    ],
    'qweb': [
    ],
    'auto_install': True,
}
