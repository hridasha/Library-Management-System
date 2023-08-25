from odoo import fields, models, api
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError


class LibraryRent(models.Model):
    _name = 'library.rent'
    _description = 'LibraryRent'
    _rec_name="name_id"

    name_id = fields.Many2one('libray.management.system', string="Book name")
    rent = fields.Integer(string="Rent count", compute="_compute_name_id")
    avab=fields.Integer(string="No of books available", compute="_compute_ava")
    state = fields.Selection([('order', 'Order'),('available', 'Available')], compute="_compute_state")

    @api.depends('name_id')
    def _compute_name_id(self):
        for rec in self:
            if rec.name_id:
                rec.rent = rec.name_id.rent_count
            else:
                rec.rent = 0

    @api.depends('name_id')
    def _compute_ava(self):
        for rec in self:
            if rec.name_id:
                rec.avab = rec.name_id.num
            else:
                rec.avab = 0
    
    @api.depends('name_id')
    def _compute_state(self):
        for rec in self:
            if rec.rent +5 >  rec.avab :
                rec.state='order'
            else:
                rec.state="available"


    def o_dform(self):
        view_id = self.env.ref('proj.view_orderdetails_form').id
        x = {
            'name': 'Order Details',
            'type': 'ir.actions.act_window',
            'res_model': 'library.order.details',
            'view_mode': 'form',
            'view_type': 'form',
            'views': [(view_id, 'form')],
            'target': 'new',
            'context': {
                
                'default_name_id': self.name_id.id,
                'default_name': self.name_id.name,
            },
            'domain': [('name_id', '=', self.name_id.id)],
        }

        return x
    