#from odoo import api, models, fields   

#class SportsFacilityCourt(models.Model):
   # _name = 'sports.facility.court'
   # _description = 'Sports Facility Resource'

   # name = fields.Char(string='Court Name', required=True)
   # surface_type = fields.Char(string='Surface Material')
   # hourly_rate = fields.Float(string='Hourly Rate')
   # maintenance_threshold = fields.Integer(string='Usage Limit (Hours)', default=100)
   # accumulated_hours = fields.Integer(string='Accumulated Usage', default=0)

   # -*- coding: utf-8 -*-
from odoo import models, fields


class SportsFacilityCourt(models.Model):
    _name = 'sports.facility.court'
    _description = 'Sports Court'
    _order = 'name'

    name = fields.Char(string='Court Name', required=True)

    sport_type_id         = fields.Many2one('sports.type', string='Sport Type', ondelete='restrict')
    surface_type          = fields.Char(string='Surface Material')
    hourly_rate           = fields.Float(string='Hourly Rate', digits=(10, 2))
    maintenance_threshold = fields.Integer(string='Usage Limit (Hours)', default=100)
    accumulated_hours     = fields.Integer(string='Accumulated Usage (Hours)', default=0)

    state = fields.Selection(
        selection=[
            ('available',   'Available'),
            ('maintenance', 'Maintenance'),
        ],
        string='Status',
        default='available',
        required=True,
    )

    facility_id = fields.Many2one('sports.facility', string='Facility', ondelete='cascade')

    amenity_ids = fields.Many2many(
        'sports.amenity',
        relation='sports_court_amenity_rel',
        column1='court_id',
        column2='amenity_id',
        string='Amenities',
    )

    def action_reset_maintenance(self):
        """Reset court after maintenance is done."""
        for record in self:
            record.write({
                'state':             'available',
                'accumulated_hours': 0,
            })
    # def write(self, vals):
    #     res = super().write(vals)
    #     if 'state' in vals:
    #             for record in self:
    #                 record.facility_id._check_facility_court_states()
    #     return res

    def write(self, vals):
        res = super().write(vals)
        if 'state' in vals:
            facilities = self.mapped('facility_id')
            facilities._check_facility_court_states()
        return res