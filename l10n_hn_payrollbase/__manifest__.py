# -*- coding: utf-8 -*-
{
    'name': "Honduras - Payroll Rules",

    'summary': """
        Nómina de Honduras
        Wages for calculating payroll""",

    'description': """
        Basis for honduras payroll adjustments
    """,

    'author': "D2i Solutions",
    'website': "http://www.d2i-solutions.com",
    'category': 'Localization',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'hr_payroll',
    ],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/employee_category_data.xml',
        'data/honduras_structure_base.xml',
        'data/contract_frecuency_data.xml',
        'views/payrollbase_views.xml',
        'views/res_company_view.xml',
        'views/hr_employee_view.xml',
        'views/hr_contrac_view.xml',
        'views/hr_payslip_views.xml',
        'views/hr_payslip_run_views.xml',
        'views/hr_attendance.xml',
        'views/hr_assignments_views.xml',
        'views/hr_commissions_views.xml',
        'views/hr_deductions_views.xml',



            ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
