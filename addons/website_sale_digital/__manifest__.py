# -*- encoding: utf-8 -*-
{
    'name': 'Website Sale Digital - Sell digital products',
    'version': '1.0.190724',
    'category': 'Website',
    'description': """
Sell digital product using attachments to virtual products
""",
    'depends': [
        'document',
        'website_sale',
    ],
    'installable': True,
    'data': [
        'views/website_sale_digital.xml',
        'views/website_sale_digital_view.xml',
    ],
    'demo': [
        'data/product_demo.xml',
    ],
}
