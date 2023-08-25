from odoo import fields, models, api
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError


class LibraryManagement(models.Model):
    _name = "libray.management.system"
    _description = "Library.management.System"

    name_id = fields.Many2one('libray.author', string='Author name')

    book = fields.Char(string="Other books", readonly=True,
                       compute='_compute_book')

    name = fields.Char(string="Book name", required=True)
    num = fields.Integer(string="No. of books available", required=True)
    avability = fields.Boolean(string="Available", default=False)
    publication = fields.Selection(
        [('Scholastic Press', 'Scholastic Press'), ('Atria Books', 'Atria Books')], string="publication")
    summary = fields.Html()
    r_reader = fields.Selection([('zero', 'no reviews'), ('one', 'very low'), ('two', 'low'), (
        'three', 'avg'), ('four', 'good'), ('five', 'very good')], string="Ratings by readers")
    price = fields.Float(string="price")
    pdate = fields.Date(string="publishing date",
                        default=datetime.today()
                        )
    dpub_s = fields.Char(string="Days since published", readonly=True)
    dpub = fields.Char(string="Days since published ",
                       compute='_compute_dpub',  readonly=True)
    ratings = fields.Float(string="ratings", required=True, default="3.0")
    genre_ids = fields.Many2many(
        'libray.genre', string="other genre by author", related='name_id.genre_ids')

    genre = fields.Selection([('narrative', "Narrative"), ('fiction', 'Fiction'), (
        'novel', 'Novel')], string="genre", default="novel", required=True)

    image = fields.Image(string="Image")
    rent_count=fields.Integer(string="Rent count",default="0")

    


    _sql_constraints = [
        (
            'uniq_name',
            'unique (name)',
            'Duplicate data'
        ),
    ]
    # @api.model
    # def create(self, values):
    #     values['price']=5000
    #     result = super().create(values)
    #     return result

    # @api.model
    # def default_get(self, fields):

    #     res = super(LibraryManagement, self).default_get(fields)
    #     print("RES",res)
    #     res['ratings']='3.25'
    #     return res
    

    
    # @api.returns('self', lambda value: value.id)
    # def copy(self, default=None):
    #     default = dict(default or {}, price='0.02')
    #     return super().copy(default)

    @api.depends('pdate')
    def _compute_dpub(self):
        for record in self:

            d = date.today()
            if not record.pdate:
                raise ValidationError("Publishing date is empty")
            else:
                if d > record.pdate:
                    d1 = d-record.pdate
                    record.dpub = d1.days
                    record.dpub_s = record.dpub
                else:
                    record.dpub = "Not published yet"
                    record.dpub_s = record.dpub

    @api.onchange('num')
    def onchange_num(self):
        if self.num >= 1:
            self.avability = True
        else:
            self.avability = False

    @api.depends('name_id')
    def _compute_book(self):
        lines = []
        for line in self.name_id.name_ids:
            d = {
                'name': line.name
            }
            lines.append(d)
        self.book = '  '.join(line['name'] for line in lines)

class LibraryAuthor(models.Model):
    _name = "libray.author"
    _description = "library.author"

    name_ids = fields.One2many(
        'libray.management.system', 'name_id', string="Books")

    name = fields.Char(string="Author name", required=True, store=True)
    genre_ids = fields.Many2many(
        'libray.genre', string="other genre by author")
    
    _sql_constraints = [
        (
            'zx',
            'unique (name)',
            'Duplicate data'
        ),
    ]

