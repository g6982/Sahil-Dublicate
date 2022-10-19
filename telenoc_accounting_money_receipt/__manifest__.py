# -*- coding: utf-8 -*-
{
    'name': 'Telenoc Accounting Money Receipts Pay/Receive',
    'summary': 'New Features for accounting journal entries to force for partner type',
    'version': '0.1',
    'license': "AGPL-3",
    'author': 'Telenoc, Ahmed Salama',
    'category': 'Accounting',
    'depends': ['account_accountant', 'hr', 'hr_employee_partner_rel'],
    'website': 'http://www.telenoc.org',
    'data': [
        'data/money_receipt_data.xml',
        
        'security/money_receipt_security.xml',
        'security/ir.model.access.csv',
        
        'reports/reports.xml',
        'reports/money_receipt_report.xml',

        'views/money_receipt_view.xml',
        'views/account_move_view_changes.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
