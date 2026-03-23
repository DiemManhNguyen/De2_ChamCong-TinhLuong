# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class BtlAttendanceWizard(models.TransientModel):
    _name = 'btl.attendance.wizard'
    _description = 'Chốt công và Tạo lương'

    month = fields.Selection([
        ('1', 'Tháng 1'), ('2', 'Tháng 2'), ('3', 'Tháng 3'),
        ('4', 'Tháng 4'), ('5', 'Tháng 5'), ('6', 'Tháng 6'),
        ('7', 'Tháng 7'), ('8', 'Tháng 8'), ('9', 'Tháng 9'),
        ('10', 'Tháng 10'), ('11', 'Tháng 11'), ('12', 'Tháng 12')
    ], string="Tháng", required=True, default=str(fields.Date.today().month))
    
    year = fields.Integer("Năm", required=True, default=fields.Date.today().year)
    
    employee_ids = fields.Many2many('hr.employee', string="Nhân viên", default=lambda self: self.env['hr.employee'].search([]))

    def action_generate_payroll(self):
        """Trigger tự động tạo phiếu lương cho các nhân viên đã chọn"""
        Payroll = self.env['btl.payroll']
        created_count = 0
        
        for employee in self.employee_ids:
            # Kiểm tra xem đã có phiếu lương chưa
            existing = Payroll.search([
                ('employee_id', '=', employee.id),
                ('month', '=', self.month),
                ('year', '=', self.year)
            ])
            
            if not existing:
                Payroll.create({
                    'employee_id': employee.id,
                    'month': self.month,
                    'year': self.year
                })
                created_count += 1
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công',
                'message': f'Đã tạo {created_count} phiếu lương cho tháng {self.month}/{self.year}',
                'type': 'success',
                'sticky': False,
            }
        }
