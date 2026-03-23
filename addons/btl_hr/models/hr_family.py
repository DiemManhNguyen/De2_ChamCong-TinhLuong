# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class HrFamily(models.Model):
    _name = 'hr.family'
    _description = 'Thân nhân & Giới thiệu Gia cảnh'
    
    name = fields.Char("Họ và Tên", required=True)
    employee_id = fields.Many2one('hr.employee', string="Nhân viên", required=True, ondelete='cascade')
    
    relationship = fields.Selection([
        ('spouse', 'Vợ / Chồng'),
        ('child', 'Con cái'),
        ('parent', 'Bố / Mẹ'),
        ('other', 'Khác')
    ], string="Mối quan hệ", required=True)
    
    birth_date = fields.Date("Ngày sinh")
    is_dependent = fields.Boolean("Người phụ thuộc (NPT)", compute="_compute_dependent", store=True, readonly=False)

    @api.depends('birth_date', 'relationship')
    def _compute_dependent(self):
        for record in self:
            if record.relationship == 'child' and record.birth_date:
                age = date.today().year - record.birth_date.year
                if age < 18:
                    record.is_dependent = True
                else:
                    record.is_dependent = False
            else:
                # User can manually set for parents/spouse
                record.is_dependent = record.is_dependent or False
