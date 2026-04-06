# -*- coding: utf-8 -*-
from odoo import models, fields


class SportsAmenity(models.Model):
    _name = 'sports.amenity'
    _description = 'Court Amenity'
    _order = 'name'

    name = fields.Char(string='Amenity', required=True)