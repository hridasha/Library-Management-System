from odoo import fields, models, api
from datetime import date, datetime, timedelta


class LibraryGenre(models.Model):
    _name = "libray.genre"
    _description = "library.genre"

    name = fields.Char(string="Genre name", required=True)
    color = fields.Integer(string='color')
    # w_color = fields.Char(string='color')

    _sql_constraints = [
        (
            'uniq_name',
            'unique (name)',
            'Duplicate data entered'
        ),
    ]