from odoo import models, fields, api
from odoo.exceptions import UserError


class Attendance(models.Model):
    _name = 'my_attendance.attendance'
    _description = 'Attendance'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    check_in = fields.Datetime(string='Check In')
    check_out = fields.Datetime(string='Check Out')
    hours_worked = fields.Float(
        string='Hours Worked', compute='_compute_hours_worked', store=True)

    @api.depends('check_in', 'check_out')
    def _compute_hours_worked(self):
        for attendance in self:
            if attendance.check_in and attendance.check_out:
                check_in = fields.Datetime.from_string(attendance.check_in)
                check_out = fields.Datetime.from_string(attendance.check_out)
                diff = check_out - check_in
                attendance.hours_worked = diff.total_seconds() / 3600
            else:
                attendance.hours_worked = 0.0

    def action_check_in(self):
        current_user = self.env.user
        employee = self.env['hr.employee'].search(
            [('user_id', '=', current_user.id)], limit=1)
        if not employee:
            raise UserError('No employee found for the current user.')

        self.employee_id = employee.id
        self.check_in = fields.Datetime.now()

    def action_check_out(self):
        if not self.check_in:
            raise UserError('Cannot check out without a check-in time.')

        self.check_out = fields.Datetime.now()
