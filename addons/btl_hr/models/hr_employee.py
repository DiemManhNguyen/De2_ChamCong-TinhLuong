# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Cải tiến Thông tin Nhân viên'

    # Sử dụng các trường chuẩn của Odoo (name, birthday, gender, work_email, etc.)
    # Bổ sung các trường đặc thù của Việt Nam/Doanh nghiệp cụ thể
    
    ma_dinh_danh = fields.Char("Mã nhân viên", required=True, copy=False, help="Mã nhân viên duy nhất trong công ty")
    ho_ten_dem = fields.Char("Họ và tên đệm")
    ten_nhan_vien = fields.Char("Tên")
    que_quan = fields.Char("Quê quán")
    
    # Thông tin bổ sung cho Giai đoạn 1 (Mô hình thực tế)
    bank_account = fields.Char("Số tài khoản ngân hàng")
    bank_name = fields.Char("Tại ngân hàng")
    vat_code = fields.Char("Mã số thuế cá nhân")
    
    # Giai đoạn 2: Gia đình
    family_ids = fields.One2many('hr.family', 'employee_id', string="Thân nhân")
    
    # Tính toán lại họ tên tự động nếu cần (Odoo mặc định dùng trường 'name')
    @api.onchange('ho_ten_dem', 'ten_nhan_vien')
    def _onchange_name_vietnam(self):
        if self.ho_ten_dem or self.ten_nhan_vien:
            full_name = f"{self.ho_ten_dem or ''} {self.ten_nhan_vien or ''}".strip()
            self.name = full_name

    _sql_constraints = [
        ('ma_dinh_danh_unique', 'unique(ma_dinh_danh)', 'Mã nhân viên đã tồn tại trên hệ thống!')
    ]

    @api.constrains('birthday')
    def _check_birthday_vietnam(self):
        for record in self:
            if record.birthday:
                year_now = date.today().year
                if year_now - record.birthday.year < 18:
                    raise ValidationError("Nhân viên phải từ 18 tuổi trở lên!")

    btl_state = fields.Selection([
        ('probation', 'Thử việc'),
        ('official', 'Chính thức'),
        ('resigned', 'Nghỉ việc')
    ], string="Trạng thái công việc", default='probation', tracking=True)

    def action_update_state(self):
        """Logic cập nhật trạng thái dựa trên hợp đồng mới nhất"""
        for record in self:
            contract = self.env['hr.contract'].search([
                ('employee_id', '=', record.id),
                ('state', '=', 'open')
            ], limit=1, order='date_start desc')
            
            if contract:
                # Giả sử nếu lương (wage) > 0 và đã vào Odoo 'open' state thì là chính thức
                # Hoặc dựa vào tên hợp đồng / loại hợp đồng
                if 'thử việc' in (contract.name or '').lower():
                    record.btl_state = 'probation'
                else:
                    record.btl_state = 'official'
            else:
                # Kiểm tra xem có hợp đồng cũ nào đã hết hạn (close/cancel) không
                past_contract = self.env['hr.contract'].search([
                    ('employee_id', '=', record.id),
                    ('state', 'in', ['close', 'cancel'])
                ], limit=1)
                if past_contract:
                    record.btl_state = 'resigned'
