from odoo import models, fields


class SportsCoach(models.Model):
    _name = 'sports.coach'
    _description = 'Sports Coach'
    _order = 'name'

    name          = fields.Char(string='Coach Name', required=True)
    sport_type_id = fields.Many2one('sports.type', string='Sport Speciality')
    hourly_fee    = fields.Float(string='Hourly Fee', digits=(10, 2))
    facility_id   = fields.Many2one(
        'sports.facility',
        string='Facility',
        required=True,
        ondelete='cascade',
    )

    _check_hourly_fee = models.Constraint(
        'CHECK(hourly_fee >= 0)',
        'Hourly fee cannot be negative!'
    )