# -*- coding: utf-8 -*-
{
    'name': "BTL - Quản lý Nhân sự (HRM)",
    'summary': "Module quản lý nhân sự cốt lõi cho hệ thống ERP",
    'description': """
        Module này là 'Source of Truth' cho thông tin nhân viên, chức vụ, phòng ban và hợp đồng lao động.
        Được phát triển dựa trên chuẩn Odoo 15.0.
    """,
    'author': "BTL Team",
    'category': 'Human Resources',
    'version': '15.0.1.0.0',
    'depends': ['base', 'hr', 'hr_contract', 'hr_skills'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        'views/hr_contract_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
