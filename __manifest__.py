{
    'name': 'Automated purchase order',
    'version': '16.0.1.0.0',
    'sequence': '-4',
    'category': 'purchase',
    'summary': 'Automated purchase order',
    'description': 'Automated purchase order',

    'installation': True,

    'depends': ['base', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/order_wizard.xml',
        'views/automated_purchase_order.xml',
    ]
}
