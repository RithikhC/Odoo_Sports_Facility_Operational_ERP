from odoo import api, models, fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Types'

    name = fields.Char(required=True)
    _unique_name = models.Constraint('UNIQUE(name)', 'The property type name must be unique!')