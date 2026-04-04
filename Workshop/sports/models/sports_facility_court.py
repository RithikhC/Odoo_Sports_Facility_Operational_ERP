from odoo import api, models, fields   

class SportsFacilityCourt(models.Model):
    _name = 'sports.facility.court'
    _description = 'Sports Facility Resource'

    name = fields.Char(string='Court Name', required=True)
    surface_type = fields.Char(string='Surface Material')
    hourly_rate = fields.Float(string='Hourly Rate')
    maintenance_threshold = fields.Integer(string='Usage Limit (Hours)', default=100)
    accumulated_hours = fields.Integer(string='Accumulated Usage', default=0)