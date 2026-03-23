# -*- coding: utf-8 -*-
{
    'name': "BTL - Quản lý Chấm công",
    'summary': "Module quản lý chấm công, ca làm và đơn từ (Kế thừa K15)",
    'description': """
        Module quản lý chấm công tích hợp thông tin nhân sự từ btl_hr.
        Bao gồm tính năng: Đăng ký ca làm, Xử lý đơn từ, Tính toán đi muộn/về sớm.
    """,
    'author': "BTL Team",
    'category': 'Human Resources/Attendance',
    'version': '15.0.1.0.0',
    'depends': ['btl_hr', 'hr_attendance', 'resource'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'wizard/btl_attendance_wizard_views.xml',
        'views/btl_attendance_views.xml',
        'views/btl_leave_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
