from odoo import api, models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tags'

    name = fields.Char(required=True)
    _unique_name = models.Constraint('UNIQUE(name)', 'A property tag must be unique!')