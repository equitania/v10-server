# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'syscoon SKR03 - Accounting',
    'version': '9.0.1.0',
    'author': 'Mathias Neef',
    'website': 'https://syscoon.com',
    'category': 'Localization/Account Charts',
    'description': """
Dieses  Modul beinhaltet einen deutschen Kontenrahmen basierend auf dem SKR03.
==============================================================================

German accounting chart and localization.
    """,
    'depends': ['l10n_de'],
    'demo': [],
    'data': [
        'account_chart.xml',
        'account_tax_fiscal_position.xml',
        'account.chart.template.yml',
    ],
    'installable': True,
}
