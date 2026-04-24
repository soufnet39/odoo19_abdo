# -*- coding: utf-8 -*-
{
    'name': 'AbdooWebUI - Web Interface Customization',
    'version': '19.0.1.0.0',
    'category': 'Abdoo',
    'summary': 'Custom modifications to the web interface',
    'author': 'SN',
    'website': 'https://www.example.com',
    'license': 'LGPL-3',
    'depends': [
        'abdoo',
        'website',
    ],
    'data': [
        'views/shop_filters.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'webui/static/src/css/webui.css',
            'webui/static/src/xml/cart_notification_patch.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
