{
    'name': 'Custom Batch',
    'version': '17.0.1.0',
    'summary': 'Module to manage custom batches by sales orders',
    'author': 'Abdulrahman Elsharef',
    'website': 'https://github.com/AbdulrahmanElsharef',
    'category': 'Sales',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/batch_sequence.xml',
        'views/sales_order.xml',
        'views/batch_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',  
    'icon': 'custom_batch\static\description\icon.png',  # Path to the module icon
}