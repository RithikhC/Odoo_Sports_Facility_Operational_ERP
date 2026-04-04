from odoo import api, models, fields

class SportsFacility(models.Model):
    _name = 'sports.facility'
    _description = 'Sports Facility'

    name = fields.Char(required=True)