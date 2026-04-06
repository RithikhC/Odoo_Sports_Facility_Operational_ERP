from odoo import models, fields


class SportsType(models.Model):
    _name = 'sports.type'
    _description = 'Sport Type'
    _order = 'name'

    name = fields.Char(string='Sport Name', required=True)