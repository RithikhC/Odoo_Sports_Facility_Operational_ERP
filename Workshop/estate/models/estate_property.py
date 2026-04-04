from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Properties"

    name = fields.Char()
    description = fields.Text()
    expected_price = fields.Float()
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    has_garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_compute_total_area")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer Price")
    state = fields.Selection(selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')])
    _check_expected_price = models.Constraint('CHECK(expected_price > 0)', 'The expected price must be positive!')
    _check_selling_price = models.Constraint('CHECK(selling_price >= 0)', 'The selling price cannot be negative!')
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    def sell_property(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold.")
            else:
                record.state = "sold"

    def cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be cancelled.")
            else:
                record.state = "cancelled"

    @api.constrains("selling_price", "expected_price")
    def _check_valid_selling_price(self):
        for record in self:
            if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0 and not float_is_zero(record.selling_price, precision_digits=2):
                raise ValidationError("Selling price cannot be lower than 90% of the expected price!")