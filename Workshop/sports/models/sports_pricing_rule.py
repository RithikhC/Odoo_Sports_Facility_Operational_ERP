from odoo import models, fields
from odoo.exceptions import ValidationError


class SportsPricingRule(models.Model):
    _name = 'sports.pricing.rule'
    _description = 'Dynamic Pricing Rule'
    _order = 'day_of_week, start_hour'

    name = fields.Char(string='Rule Name', required=True)

    day_of_week = fields.Selection(
        selection=[
            ('0', 'Monday'),
            ('1', 'Tuesday'),
            ('2', 'Wednesday'),
            ('3', 'Thursday'),
            ('4', 'Friday'),
            ('5', 'Saturday'),
            ('6', 'Sunday'),
        ],
        string='Day of Week',
        required=True,
    )

    start_hour       = fields.Float(string='Start Hour (24h)', digits=(4, 2))
    end_hour         = fields.Float(string='End Hour (24h)',   digits=(4, 2))
    price_multiplier = fields.Float(string='Price Multiplier', default=1.0, digits=(4, 2))

    _check_hours = models.Constraint(
        'CHECK(end_hour > start_hour)',
        'End hour must be after start hour!'
    )
    _check_multiplier = models.Constraint(
        'CHECK(price_multiplier > 0)',
        'Price multiplier must be positive!'
    )

    def get_multiplier_for_datetime(self, dt):
        """Return the highest multiplier rule matching the given datetime."""
        if not dt:
            return 1.0
        day   = str(dt.weekday())
        hour  = dt.hour + dt.minute / 60.0
        rules = self.search([
            ('day_of_week', '=',  day),
            ('start_hour',  '<=', hour),
            ('end_hour',    '>',  hour),
        ], order='price_multiplier desc', limit=1)
        return rules.price_multiplier if rules else 1.0