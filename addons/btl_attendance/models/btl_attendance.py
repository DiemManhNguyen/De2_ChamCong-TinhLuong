# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, time
from odoo.exceptions import ValidationError
from pytz import timezone, UTC

class BtlAttendance(models.Model):
    _name = 'btl.attendance'
    _description = 'Bảng Chấm Công BTL'
    _rec_name = 'display_name'

    employee_id = fields.Many2one('hr.employee', string="Nhân viên", required=True)
    check_date = fields.Date("Ngày chấm công", required=True, default=fields.Date.context_today)
    
    display_name = fields.Char(string="Tên hiển thị", compute="_compute_display_name", store=True)

    @api.depends('employee_id', 'check_date')
    def _compute_display_name(self):
        for record in self:
            if record.employee_id and record.check_date:
                record.display_name = f"{record.employee_id.name} - {record.check_date}"
            else:
                record.display_name = "Mới"

    # Ca làm việc (Kế thừa logic K15)
    shift_type = fields.Selection([
        ('morning', 'Sáng'),
        ('afternoon', 'Chiều'),
        ('full', 'Cả ngày')
    ], string="Ca làm", default='full')

    # Giờ thực tế
    check_in = fields.Datetime("Giờ vào thực tế")
    check_out = fields.Datetime("Giờ ra thực tế")

    # Giờ lý thuyết (Tùy biến theo ca)
    planned_in = fields.Datetime("Giờ vào kế hoạch", compute='_compute_planned_hours', store=True)
    planned_out = fields.Datetime("Giờ ra kế hoạch", compute='_compute_planned_hours', store=True)

    @api.depends('shift_type', 'check_date', 'employee_id')
    def _compute_planned_hours(self):
        for record in self:
            if not record.check_date or not record.employee_id:
                record.planned_in = False
                record.planned_out = False
                continue

            calendar = record.employee_id.resource_calendar_id
            if not calendar:
                # Fallback to hardcoded if no calendar (optional)
                record.planned_in = False
                record.planned_out = False
                continue

            # Tìm ca làm việc trong Resource Calendar cho ngày này
            dayofweek = str(record.check_date.weekday())
            work_hours = calendar.attendance_ids.filtered(lambda a: a.dayofweek == dayofweek)
            
            if work_hours:
                # Lấy giờ sớm nhất và muộn nhất trong ngày (cho ca gãy)
                h_in = min(work_hours.mapped('hour_from'))
                h_out = max(work_hours.mapped('hour_to'))
                
                tz = timezone(self.env.user.tz or 'Asia/Ho_Chi_Minh')
                
                t_in = time(int(h_in), int((h_in % 1) * 60))
                t_out = time(int(h_out), int((h_out % 1) * 60))

                dt_in = tz.localize(datetime.combine(record.check_date, t_in)).astimezone(UTC).replace(tzinfo=None)
                dt_out = tz.localize(datetime.combine(record.check_date, t_out)).astimezone(UTC).replace(tzinfo=None)
                
                record.planned_in = dt_in
                record.planned_out = dt_out
            else:
                record.planned_in = False
                record.planned_out = False

    # Đơn từ liên quan
    leave_id = fields.Many2one('btl.leave', string="Đơn từ/Giải trình", 
                               domain="[('employee_id', '=', employee_id), ('apply_date', '=', check_date), ('state', '=', 'approve')]")

    # Tính toán muộn/sớm
    minutes_late = fields.Float("Phút đi muộn", compute="_compute_late_early", store=True)
    minutes_early = fields.Float("Phút về sớm", compute="_compute_late_early", store=True)

    @api.depends('check_in', 'check_out', 'planned_in', 'planned_out', 'leave_id')
    def _compute_late_early(self):
        for record in self:
            late = 0.0
            early = 0.0
            if record.check_in and record.planned_in:
                if record.check_in > record.planned_in:
                    late = (record.check_in - record.planned_in).total_seconds() / 60
            
            if record.check_out and record.planned_out:
                if record.check_out < record.planned_out:
                    early = (record.planned_out - record.check_out).total_seconds() / 60
            
            # Trừ thời gian nếu có đơn giải trình (giả sử đơn giải trình bù 100% thời gian xin)
            if record.leave_id and record.leave_id.leave_type == 'late_early':
                # Trong mô hình thực tế, thời gian xin thường được ghi nhận cụ thể
                # Ở đây ta giả định nếu có đơn được duyệt thì tính là hợp lệ (late = 0)
                late = 0.0
                early = 0.0
            
            record.minutes_late = late
            record.minutes_early = early

    status = fields.Selection([
        ('on_time', 'Đúng giờ'),
        ('late', 'Đi muộn'),
        ('early', 'Về sớm'),
        ('both', 'Muộn & Sớm'),
        ('absent', 'Vắng mặt')
    ], string="Trạng thái", compute="_compute_status", store=True)

    @api.depends('minutes_late', 'minutes_early', 'check_in', 'check_out')
    def _compute_status(self):
        for record in self:
            if not record.check_in and not record.check_out:
                record.status = 'absent'
            elif record.minutes_late > 0 and record.minutes_early > 0:
                record.status = 'both'
            elif record.minutes_late > 0:
                record.status = 'late'
            elif record.minutes_early > 0:
                record.status = 'early'
            else:
                record.status = 'on_time'
