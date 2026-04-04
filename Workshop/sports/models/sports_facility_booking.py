from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero

class SportsFacilityBooking(models.Model):
    _name = 'sports.facility.booking'
    _description = 'Court Reservation'

    name = fields.Char(string='Booking Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Athlete/Customer', required=True)
    court_id = fields.Many2one('sports.facility.court', string='Assigned Court', required=True)
    
    start_time = fields.Datetime(string='Start Time', required=True)
    end_time = fields.Datetime(string='End Time', required=True)
