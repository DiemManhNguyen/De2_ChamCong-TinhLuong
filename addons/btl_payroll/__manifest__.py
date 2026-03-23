# -*- coding: utf-8 -*-
{
    'name': "BTL - Quản lý Tiền lương",
    'summary': "Module tính lương dựa trên dữ liệu Chấm công và Hợp đồng",
    'description': """
        Module tính lương tự động tích hợp:
        - Lấy lương cơ bản từ hr.contract (btl_hr).
        - Lấy công thực tế và phạt đi muộn từ btl_attendance.
        - Kết quả xuất ra Phiếu lương (Payslip).
    """,
    'author': "BTL Team",
    'category': 'Human Resources/Payroll',
    'version': '15.0.1.0.0',
    'depends': ['btl_hr', 'btl_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'views/btl_payroll_views.xml',
        'report/btl_payroll_report.xml',
        'report/btl_payroll_templates.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
