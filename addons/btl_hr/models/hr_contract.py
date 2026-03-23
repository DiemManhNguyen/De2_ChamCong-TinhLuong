# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HrContract(models.Model):
    _inherit = 'hr.contract'
    _description = 'Hợp đồng Lao động Cải tiến'

    # Các loại phụ cấp (Mô hình doanh nghiệp thực tế Việt Nam)
    phu_cap_an_trua = fields.Monetary(string="Phụ cấp ăn trưa", currency_field='currency_id', help="Mức phụ cấp ăn trưa hàng tháng")
    phu_cap_xang_xe = fields.Monetary(string="Phụ cấp xăng xe", currency_field='currency_id')
    phu_cap_dien_thoai = fields.Monetary(string="Phụ cấp điện thoại", currency_field='currency_id')
    
    # Bảo hiểm & Thuế (Mô hình Việt Nam)
    insurance_base = fields.Monetary(string="Mức đóng Bảo hiểm", currency_field='currency_id', help="Lương đóng BHXH/BHYT/BHTN")
    has_insurance = fields.Boolean(string="Tham gia Bảo hiểm", default=True)
    num_dependents = fields.Integer(string="Số NPT (Tự động tính)", compute="_compute_dependents", store=True, readonly=False)

    @api.depends('employee_id.family_ids.is_dependent')
    def _compute_dependents(self):
        for record in self:
            if record.employee_id:
                count = len(record.employee_id.family_ids.filtered(lambda f: f.is_dependent))
                record.num_dependents = count
            else:
                record.num_dependents = 0
    
    # Tổng lương và phụ cấp
    tong_thu_nhap_du_kien = fields.Monetary(string="Tổng thu nhập dự kiến", compute="_compute_tong_thu_nhap", store=True)

    @api.depends('wage', 'phu_cap_an_trua', 'phu_cap_xang_xe', 'phu_cap_dien_thoai')
    def _compute_tong_thu_nhap(self):
        for record in self:
            record.tong_thu_nhap_du_kien = record.wage + record.phu_cap_an_trua + record.phu_cap_xang_xe + record.phu_cap_dien_thoai

    @api.model
    def create(self, vals):
        res = super(HrContract, self).create(vals)
        if res.employee_id:
            res.employee_id.action_update_state()
        return res

    def write(self, vals):
        res = super(HrContract, self).write(vals)
        for record in self:
            if record.employee_id:
                record.employee_id.action_update_state()
        return res
