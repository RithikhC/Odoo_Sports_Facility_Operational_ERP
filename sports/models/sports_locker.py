from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class SportsLocker(models.Model):
    _name = 'sports.locker'
    _description = 'Sports Locker'
    _order = 'name'

    name = fields.Char(string='Locker Name', required=True)

    locker_type = fields.Selection(
        selection=[
            ('small', 'Small'),
            ('large', 'Large'),
        ],
        string='Locker Type',
        required=True,
    )

    state = fields.Selection(
        selection=[
            ('available', 'Available'),
            ('rented',    'Rented'),
        ],
        string='Status',
        default='available',
        required=True,
    )

    facility_id = fields.Many2one(
        'sports.facility',
        string='Facility',
        required=True,
        ondelete='cascade',
    )

    renter_id   = fields.Many2one('res.partner', string='Renter')
    expiry_date = fields.Date(string='Rental Expiry Date')
    monthly_fee = fields.Float(string='Monthly Fee', digits=(10, 2))

    @api.constrains('state', 'renter_id', 'expiry_date')
    def _check_rented_fields(self):
        for record in self:
            if record.state == 'rented':
                if not record.renter_id:
                    raise ValidationError("A rented locker must have a renter assigned.")
                if not record.expiry_date:
                    raise ValidationError("A rented locker must have an expiry date.")
                if record.expiry_date < date.today():
                    raise ValidationError("Expiry date cannot be in the past.")

    @api.constrains('monthly_fee')
    def _check_monthly_fee(self):
        for record in self:
            if record.monthly_fee < 0:
                raise ValidationError("Monthly fee cannot be negative.")

    def action_release(self):
        for record in self:
            record.write({
                'state':       'available',
                'renter_id':   False,
                'expiry_date': False,
            })

    def action_rent(self):
        for record in self:
            if record.state == 'rented':
                raise ValidationError(
                    f"Locker '{record.name}' is already rented."
                )
            record.state = 'rented'

    @api.model
    def _cron_release_expired_lockers(self):
        expired = self.search([
            ('state',       '=',  'rented'),
            ('expiry_date', '<=', fields.Date.today()),
        ])
        expired.action_release()
