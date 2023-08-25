from odoo import fields, models, api
from datetime import date, datetime, timedelta
from odoo.exceptions import UserError, AccessError, ValidationError, AccessDenied


class LibraryCustomer(models.Model):
    _name = "library.customer"
    _description = "Customer"
    _rec_name = 'custid'

    name = fields.Char(string="Customer Name")
    custid = fields.Char(
        string="Customer ID",
        readonly=True,
        default=lambda self: self._generate_sequence() if self._is_new() else False
    )
    custom_groups_id = fields.Many2many('res.groups', string='Groups', default=lambda self: self.env.ref(
        'proj.group_lib_customer'))

    user_id = fields.Many2one('res.users', string="User")
    membership = fields.Selection(
        [('3 months', '3 Months'), ('6 months', '6 Months'),
         ('12 months', '12 Months')],
        string='Membership period'
    )
    d_mem = fields.Date(string="Membership date", default=date.today())
    expiry = fields.Date(string="Membership expiry date",
                         compute="_compute_expiry_date", store=True)

    rented_book_ids = fields.Many2many(
        'libray.management.system',
        string="Book rented",
        domain=[('avability', '=', True)],
    )

    bookids = fields.Char(string="book ids ori")
    rented_book_date = fields.Date(string="Books rented on ")
    return_book_date = fields.Date(string="Books returned on ")
    penalty = fields.Float(string="Penalty amount",
                           compute="compute_penalty", store=True)

    def _generate_sequence(self):
        if self._is_new():
            previous_value = self.env['library.customer'].search(
                [], order='custid desc', limit=1).custid
            if previous_value:
                numeric_part = int(previous_value[1:])
                return previous_value[0] + str(numeric_part + 1)
        return self.env['ir.sequence'].next_by_code('library.customer.sequence')

    def _is_new(self):
        return not bool(self._origin)

    @api.constrains('rented_book_ids')
    def check_rented_book_limit(self):
        max_books = 3
        if len(self.rented_book_ids) > max_books:
            raise ValidationError(
                "You can only rent up to {} books.".format(max_books))

    @api.constrains('groups_id')
    def check_group_limit(self):
        max_group = 1
        if len(self.groups_id) > max_group:
            raise ValidationError(
                "Only 1 group can be added")

    def write(self, vals):
        print("\n vals -----------", vals)

        if 'rented_book_ids' in vals:
            lb = self.env['libray.management.system']
            # rented= all the ids of the rented record
            rented = self.rented_book_ids.browse(vals['rented_book_ids'][0][2])
            print("\n rented -----", rented)
            # new books ids will have the newly added records id
            new_books = rented - self.rented_book_ids
            new_book_ids = new_books.ids

            print("-------------book-------------------", rented)
            print("-------------newwbook-------------------", new_book_ids)
            print("-------------newwbook-------------------", type(new_book_ids))

            # counts is a dictionary of record id and its record count
            counts = {book_id: lb.browse(
                [book_id]).rent_count for book_id in new_book_ids}
            if new_book_ids:

                for rec_id in new_book_ids:
                    book = lb.browse([rec_id])
                    book.write({'rent_count': book.rent_count + 1})
                    self.bookids = new_book_ids

                # decreasee the rent count if the record is being removed
                rem = self.env['libray.management.system'].browse(
                    list(set(self._origin.rented_book_ids.ids) - set(rented.ids)))
                print("------------rem------------", rem)
                for book in rem:
                    lb.browse([book.id]).write(
                        {'rent_count': lb.browse([book.id]).rent_count - 1})

                    self.bookids = new_book_ids
            else:

                rem = self.env['libray.management.system'].browse(
                    list(set(self._origin.rented_book_ids.ids) - set(rented.ids)))
                print("------------rem------------", rem)
                for book in rem:
                    lb.browse([book.id]).write(
                        {'rent_count': lb.browse([book.id]).rent_count - 1})
                    self.bookids = new_book_ids

        res = super().write(vals)
        return res

    @api.model
    def create(self, vals):
        if 'custid' not in vals:
            sequence = self.env['ir.sequence'].next_by_code(
                'library.customer.sequence')
            vals['custid'] = sequence

        customer = super(LibraryCustomer, self).create(vals)

        
        if 'rented_book_ids' in vals:
            lb = self.env['libray.management.system']
            rented = customer.rented_book_ids.browse(
                vals['rented_book_ids'][0][2])
            books = rented.ids

            counts = {book_id: lb.browse(
                [book_id]).rent_count + 1 for book_id in books}

            for rec in rented:
                rec.write({'rent_count': rec.rent_count + 1})

            customer.write({'bookids': books})

        return customer

    @api.depends('rented_book_date', 'return_book_date')
    def compute_penalty(self):
        for rec in self:
            if rec.rented_book_date and rec.return_book_date:
                diff = rec.return_book_date - rec.rented_book_date
                if diff.days > 14:
                    rec.penalty = 10 * diff.days
                else:
                    rec.penalty = 0
            else:
                rec.penalty = 0

    @api.depends('membership', 'd_mem')
    def _compute_expiry_date(self):
        for record in self:
            if record.membership and record.d_mem:
                membership_durations = {
                    '3 months': 90,
                    '6 months': 180,
                    '12 months': 365
                }
                duration = membership_durations.get(record.membership)
                if duration:
                    expiry_date = record.d_mem + timedelta(days=duration)
                    record.expiry = expiry_date
                else:
                    record.expiry = False
            else:
                record.expiry = False

    _sql_constraints = [
        (
            'custid_uniq_name',
            'unique(custid)',
            'Duplicate id created'
        ),
    ]
