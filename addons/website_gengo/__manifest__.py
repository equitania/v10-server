# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Gengo Translator',
    'version': '1.0.190724',
    'category': 'Website',
    'description': """
Website Gengo Translator
========================

Translate you website in one click
""",
    'depends': [
        'website',
        'base_gengo'
    ],
    'data': [
        'views/website_gengo_templates.xml',
    ]
}
