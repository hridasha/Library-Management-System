from odoo import fields, models, api
from datetime import date, datetime, timedelta


class CancelOrderWiz(models.TransientModel):
    _name = 'cancel.order.wiz'
    _description = 'CancelOrderWiz'

    ordername_id = fields.Many2one('library.order', string="Cancelled order")
    
    
    def cancel(self):
        order = self.env['library.order'].browse(self.ordername_id.id)
        if order:
            order.unlink()
            print("Record deleted")
        else:
            print("No record found")

