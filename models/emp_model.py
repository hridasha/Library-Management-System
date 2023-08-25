from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    attendance_ids = fields.One2many('hr.attendance', 'employee_id', string='Attendance Records')
