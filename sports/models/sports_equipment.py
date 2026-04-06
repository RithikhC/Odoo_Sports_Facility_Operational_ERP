

# from odoo import models, fields
# from odoo.exceptions import ValidationError


# class SportsEquipment(models.Model):
#     _name = 'sports.equipment'
#     _description = 'Sports Equipment'
#     _order = 'name'

#     name           = fields.Char(string='Equipment Name', required=True)
#     rental_price   = fields.Float(string='Rental Price per Session', digits=(10, 2))
#     stock_quantity = fields.Integer(string='Stock Quantity', default=0)
#     facility_id    = fields.Many2one(
#         'sports.facility',
#         string='Facility',
#         required=True,
#         ondelete='cascade',
#     )

#     _check_stock = models.Constraint(
#         'CHECK(stock_quantity >= 0)',
#         'Stock quantity cannot be negative!'
#     )
#     _check_rental_price = models.Constraint(
#         'CHECK(rental_price >= 0)',
#         'Rental price cannot be negative!'
#     )

from odoo import models, fields


class SportsEquipment(models.Model):
    _name = 'sports.equipment'
    _description = 'Sports Equipment'
    _order = 'name'

    name          = fields.Char(string='Equipment Name', required=True)
    rental_price  = fields.Float(string='Rental Price per Session', digits=(10, 2))
    stock_quantity = fields.Integer(string='Stock Quantity', default=0)
    facility_id   = fields.Many2one(
        'sports.facility',
        string='Facility',
        required=True,
        ondelete='cascade',
    )
    sport_type_id = fields.Many2one(
        'sports.type',
        string='Sport Type',
        required=True,
    )

    _check_stock = models.Constraint(
        'CHECK(stock_quantity >= 0)',
        'Stock quantity cannot be negative!'
    )
    _check_rental_price = models.Constraint(
        'CHECK(rental_price >= 0)',
        'Rental price cannot be negative!'
    )