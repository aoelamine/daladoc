{
    'name': 'Daladoc Visit',
    'version': '20.0.1.0.0',
    'summary': 'Medical Visit Workflow – from Check-in to Closure',
    'description': 'Manage the complete medical visit lifecycle: check-in & vitals, anamnesis, examination, prescriptions & referrals, summary & billing.',
    'author': 'Daladoc',
    'category': 'Custom',
    'depends': ['daladoc_main'],
    'data': [
        # Security
        'security/ir.access.csv',

        # Views
        'views/daladoc_visit.xml',
        'views/daladoc_prescription.xml',
        'views/daladoc_lab_test.xml',
        'views/daladoc_referrals.xml',

        # Menus
        'views/menus.xml',
    ],
    'installable': True,
    'application': False,
}