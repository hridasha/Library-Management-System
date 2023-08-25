from odoo import fields, models, api
from odoo.exceptions import ValidationError

class LibraryOrder(models.Model):
    _name = 'library.order'
    _description = 'Library order'
    _rec_name = 'name_id'

    oid = fields.Integer(string='Order id', required=True, copy=False)
    name_id = fields.Many2one('libray.management.system', string='Book name', domain=[('num', '<', 10)])
    num = fields.Integer(string="No. of books available", required=True, related='name_id.num')
    state = fields.Selection(
        [('ordered', 'Ordered'), ('pending', 'Pending'), ('received', 'Received'), ('cancelled', 'Cancelled')],
        string="Status",
        default='pending'
    )

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'

    def action_rec(self):
        for rec in self:
            rec.state = 'received'

    def action_pending(self):
        for rec in self:
            rec.state = 'pending'

    def unlink(self):
        if len(self) > 1:
            raise ValidationError("More than one record cannot be deleted")
        if self.state == 'received':
            raise ValidationError("Order has been received, record cannot be deleted!!")
        res = super().unlink()
        return res

    def o_dform(self):
        for rec in self:
            rec.state = 'ordered'
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


class LibraryOrderdetails(models.Model):
    _name = 'library.order.details'
    _description = 'Order details'
    _rec_name = 'name'

    name_id = fields.Many2one('libray.management.system', string='Book Name')
    name = fields.Char(string='Book name', related='name_id.name')
    num_b = fields.Integer(string='Number of books')
    state = fields.Selection([('pending', 'Pending'), ('cancelled', 'Cancelled')], default='pending', string="Status")

    def action_pending(self):
        for rec in self:
            rec.state = 'pending'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'

    def write(self, values):
        if self.num_b == 0:
            values['num_b'] = 10
            print("WRITE METHOD", values)
            res = super().write(values)
            return res
