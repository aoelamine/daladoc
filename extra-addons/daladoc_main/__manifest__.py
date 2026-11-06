{
    'name': 'Daladoc main',
    'version': '20.0.1.0.0',
    'summary': '//',
    'description': '//',
    'author': 'Daladoc',
    'category': 'Custom',
    'depends': ['base', 'contacts'],
    'data': [
        #security
        'security/ir.access.csv',

        # Views
        'views/res_partner.xml',
        'views/daladoc_maladie.xml',
        'views/daladoc_treatments.xml',
        'views/daladoc_metrics.xml',
        'views/daladoc_historique_medical.xml',

        # Menus
        'views/menus.xml',

        # reports
    ],
    'installable': True,
    'application': False,
}