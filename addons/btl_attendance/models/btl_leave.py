# -*- coding: utf-8 -*-
from odoo import models, fields, api

class BtlLeave(models.Model):
    _name = 'btl.leave'
    _description = 'Đơn xin nghỉ / Giải trình'
    _rec_name = 'employee_id'

    name = fields.Char("Mã văn bản", required=True, copy=False, readonly=True, default='Mới')
    employee_id = fields.Many2one('hr.employee', string="Nhân viên", required=True)
    apply_date = fields.Date("Ngày áp dụng", required=True, default=fields.Date.context_today)
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'Mới') == 'Mới':
            vals['name'] = self.env['ir.sequence'].next_by_code('btl.leave') or 'Mới'
        return super(BtlLeave, self).create(vals)
    
    leave_type = fields.Selection([
        ('full_day', 'Nghỉ cả ngày'),
        ('morning', 'Nghỉ sáng'),
        ('afternoon', 'Nghỉ chiều'),
        ('late_early', 'Xin đi muộn/về sớm')
    ], string="Loại đơn", required=True)

    reason = fields.Text("Lý do", required=True)
    
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('confirm', 'Chờ duyệt'),
        ('approve', 'Đã duyệt'),
        ('refuse', 'Từ chối')
    ], string="Trạng thái", default='draft')

    def action_confirm(self):
        self.write({'state': 'confirm'})

    def action_approve(self):
        self.write({'state': 'approve'})
        # Giai đoạn 2: Trigger tự động hóa
        # Tìm bản ghi chấm công tương ứng để gắn đơn từ vào
        for record in self:
            attendance = self.env['btl.attendance'].search([
                ('employee_id', '=', record.employee_id.id),
                ('check_date', '=', record.apply_date)
            ], limit=1)
            if attendance:
                # Gán đơn từ vào bảng công để kích hoạt tính toán lại minutes_late/early
                attendance.write({'leave_id': record.id})

    def action_refuse(self):
        self.write({'state': 'refuse'})
