# -*- coding: utf-8 -*-
from odoo import models, fields, api
from calendar import monthrange

class BtlPayroll(models.Model):
    _name = 'btl.payroll'
    _description = 'Phiếu lương BTL'
    _rec_name = 'display_name'

    employee_id = fields.Many2one('hr.employee', string="Nhân viên", required=True)
    month = fields.Selection([
        ('1', 'Tháng 1'), ('2', 'Tháng 2'), ('3', 'Tháng 3'),
        ('4', 'Tháng 4'), ('5', 'Tháng 5'), ('6', 'Tháng 6'),
        ('7', 'Tháng 7'), ('8', 'Tháng 8'), ('9', 'Tháng 9'),
        ('10', 'Tháng 10'), ('11', 'Tháng 11'), ('12', 'Tháng 12')
    ], string="Tháng", required=True, default=str(fields.Date.today().month))
    
    year = fields.Integer("Năm", required=True, default=fields.Date.today().year)
    
    display_name = fields.Char(string="Tên phiếu lương", compute="_compute_display_name")

    @api.depends('employee_id', 'month', 'year')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"Lương {record.employee_id.name} - T{record.month}/{record.year}"

    # Dữ liệu từ Hợp đồng
    contract_id = fields.Many2one('hr.contract', string="Hợp đồng", compute="_compute_contract", store=True)
    wage = fields.Monetary(related='contract_id.wage', string="Lương cơ bản", currency_field='currency_id')
    
    phu_cap_an_trua = fields.Monetary(related='contract_id.phu_cap_an_trua', string="Phụ cấp ăn trưa")
    phu_cap_xang_xe = fields.Monetary(related='contract_id.phu_cap_xang_xe', string="Phụ cấp xăng xe")
    phu_cap_dien_thoai = fields.Monetary(related='contract_id.phu_cap_dien_thoai', string="Phụ cấp điện thoại")
    
    currency_id = fields.Many2one('res.currency', related='employee_id.company_id.currency_id')

    @api.depends('employee_id')
    def _compute_contract(self):
        for record in self:
            contract = self.env['hr.contract'].search([
                ('employee_id', '=', record.employee_id.id),
                ('state', '=', 'open')
            ], limit=1)
            record.contract_id = contract.id if contract else False

    # Dữ liệu từ Chấm công
    total_work_days = fields.Float("Số ngày công thực tế", compute="_compute_attendance_data")
    total_late_penalty = fields.Monetary("Tiền phạt đi muộn", compute="_compute_attendance_data", currency_field='currency_id')
    
    # Bảo hiểm & Thuế (Lấy từ hợp đồng)
    has_insurance = fields.Boolean(related='contract_id.has_insurance', string="Tham gia bảo hiểm")
    insurance_base = fields.Monetary(related='contract_id.insurance_base', string="Lương đóng BH")
    num_dependents = fields.Integer(related='contract_id.num_dependents', string="Số người phụ thuộc")

    # Các khoản giảm trừ
    bh_deduction = fields.Monetary("Khấu trừ BH (10.5%)", compute="_compute_net_salary")
    tax_deduction = fields.Monetary("Thuế TNCN", compute="_compute_net_salary")
    
    net_salary = fields.Monetary("Lương thực nhận", compute="_compute_net_salary", currency_field='currency_id')

    # AI Evaluation (Mức 3)
    ai_evaluation = fields.Text("AI Đánh giá Năng lực", readonly=True)

    def action_generate_ai_evaluation(self):
        for record in self:
            try:
                # Do API Key OpenAI bạn cung cấp bị lỗi hết tài khoản (Insufficient Quota)
                # Dưới đây là đoạn code Demo Mô phỏng kết quả của AI để dùng đi báo cáo với Giảng viên:
                
                penalty_str = f"{record.total_late_penalty:,.0f} VND" if record.total_late_penalty > 0 else "0 VND"
                
                if record.total_late_penalty > 0:
                    mock_response = f"Dựa trên dữ liệu, nhân viên {record.employee_id.name} đã đi làm {record.total_work_days} ngày trong tháng. Tuy nhiên, việc bị phạt {penalty_str} cho thấy nhân viên cần chú ý hơn về việc tuân thủ giờ giấc. Đề nghị nhân viên cố gắng đi làm đúng giờ để cải thiện hiệu suất chung."
                else:
                    mock_response = f"Nhân viên {record.employee_id.name} có thái độ làm việc tuyệt vời, đảm bảo {record.total_work_days} ngày công và không bị phạt đi muộn/về sớm nào ({penalty_str}). Đề nghị tuyên dương và tiếp tục phát huy tinh thần trách nhiệm này."
                
                record.ai_evaluation = f"[MÔ PHỎNG AI] {mock_response}"
                
            except Exception as e:
                record.ai_evaluation = f"Error generating AI evaluation: {str(e)}"


    @api.depends('employee_id', 'month', 'year')
    def _compute_attendance_data(self):
        for record in self:
            if not record.employee_id or not record.month or not record.year:
                record.total_work_days = 0
                record.total_late_penalty = 0
                continue
                
            first_day = f"{record.year}-{int(record.month):02d}-01"
            last_day = f"{record.year}-{int(record.month):02d}-{monthrange(record.year, int(record.month))[1]}"
            
            attendances = self.env['btl.attendance'].search([
                ('employee_id', '=', record.employee_id.id),
                ('check_date', '>=', first_day),
                ('check_date', '<=', last_day),
                ('status', '!=', 'absent')
            ])
            
            # Tính ngày công (mỗi bản ghi chấm công là 1/2 hoặc 1 ngày tùy shift_type)
            days = 0
            late_penalty = 0
            for att in attendances:
                val = 1.0 if att.shift_type == 'full' else 0.5
                days += val
                # Phạt 10k cho mỗi phút đi muộn (giả định doanh nghiệp thực tế)
                late_penalty += (att.minutes_late + att.minutes_early) * 1000
                
            record.total_work_days = days
            record.total_late_penalty = late_penalty

    @api.depends('wage', 'phu_cap_an_trua', 'phu_cap_xang_xe', 'phu_cap_dien_thoai', 'total_work_days', 'total_late_penalty', 'has_insurance', 'insurance_base', 'num_dependents')
    def _compute_net_salary(self):
        for record in self:
            # Giả định tháng có 24 ngày công chuẩn
            standard_days = 24
            if standard_days > 0:
                salary_per_day = record.wage / standard_days
                earned = salary_per_day * record.total_work_days
                
                # Tổng phụ cấp tương ứng với số ngày đi làm (Giả định phụ cấp ăn trưa miễn thuế)
                allowances = (record.phu_cap_an_trua + record.phu_cap_xang_xe + record.phu_cap_dien_thoai) / standard_days * record.total_work_days
                
                gross_income = earned + allowances - record.total_late_penalty
                
                # 1. Tính bảo hiểm (10.5%: 8% BHXH, 1.5% BHYT, 1% BHTN)
                insurance = 0.0
                if record.has_insurance and record.insurance_base > 0:
                    # Tính tỉ lệ theo ngày công thực tế
                    insurance = (record.insurance_base * 0.105) / standard_days * record.total_work_days
                
                record.bh_deduction = insurance
                
                # 2. Tính thuế TNCN (Giả định cơ bản)
                # Thu nhập chịu thuế = Gross - BH (Ăn trưa thuộc nhóm miễn thuế nhưng ở đây gộp chung cho đơn giản)
                # Giảm trừ gia cảnh: Bản thân 11tr, Người phụ thuộc 4.4tr
                taxable_income = gross_income - insurance - 11000000 - (record.num_dependents * 4400000)
                
                pit = 0.0
                if taxable_income > 0:
                    # Bậc thang thuế rút gọn (5%, 10%, 15%...)
                    if taxable_income <= 5000000:
                        pit = taxable_income * 0.05
                    elif taxable_income <= 10000000:
                        pit = taxable_income * 0.1 - 250000
                    else:
                        pit = taxable_income * 0.15 - 750000
                
                record.tax_deduction = pit
                
                # 3. Lương thực nhận
                record.net_salary = gross_income - insurance - pit
            else:
                record.bh_deduction = 0
                record.tax_deduction = 0
                record.net_salary = 0
