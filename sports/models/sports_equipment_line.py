# from odoo import models, fields, api
# from odoo.exceptions import ValidationError


# class SportsEquipmentLine(models.Model):
#     _name = 'sports.equipment.line'
#     _description = 'Booking Equipment Line'

#     booking_id   = fields.Many2one('sports.facility.booking', string='Booking', ondelete='cascade')
#     equipment_id = fields.Many2one('sports.equipment', string='Equipment', required=True)
#     quantity     = fields.Integer(string='Quantity', default=1)
#     rental_price = fields.Float(string='Unit Price', related='equipment_id.rental_price', readonly=True, store=True)
#     subtotal     = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True, digits=(10, 2))

#     @api.depends('quantity', 'rental_price')
#     def _compute_subtotal(self):
#         for line in self:
#             line.subtotal = line.quantity * line.rental_price

#     @api.constrains('quantity', 'equipment_id', 'booking_id')
#     def _check_stock_availability(self):
#         for line in self:
#             if line.quantity <= 0:
#                 raise ValidationError("Quantity must be at least 1.")

#             # Equipment must belong to the same facility as the court
#             booking_facility = line.booking_id.court_id.facility_id
#             if line.equipment_id.facility_id != booking_facility:
#                 raise ValidationError(
#                     f"Equipment '{line.equipment_id.name}' does not belong to facility "
#                     f"'{booking_facility.name}'. You can only use equipment from the same facility as the court."
#                 )

#             # Find all overlapping bookings at the same facility
#             # excluding the current booking
#             overlapping_bookings = self.env['sports.facility.booking'].search([
#                 ('id',         '!=', line.booking_id.id),
#                 ('state',      'in', ['confirmed', 'draft']),
#                 ('start_time', '<',  line.booking_id.end_time),
#                 ('end_time',   '>',  line.booking_id.start_time),
#                 ('court_id.facility_id', '=', booking_facility.id),
#             ])

#             already_reserved = sum(
#                 ol.quantity
#                 for ol in self.search([
#                     ('booking_id',   'in', overlapping_bookings.ids),
#                     ('equipment_id', '=',  line.equipment_id.id),
#                 ])
#             )

#             available = line.equipment_id.stock_quantity - already_reserved
#             if line.quantity > available:
#                 raise ValidationError(
#                     f"Not enough stock for '{line.equipment_id.name}' "
#                     f"at facility '{booking_facility.name}' during this time slot.\n"
#                     f"Total stock: {line.equipment_id.stock_quantity}\n"
#                     f"Already reserved: {already_reserved}\n"
#                     f"Available: {available}\n"
#                     f"Requested: {line.quantity}"
#                 )

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SportsEquipmentLine(models.Model):
    _name = 'sports.equipment.line'
    _description = 'Booking Equipment Line'

    booking_id   = fields.Many2one('sports.facility.booking', string='Booking', ondelete='cascade')
    equipment_id = fields.Many2one('sports.equipment', string='Equipment', required=True)
    quantity     = fields.Integer(string='Quantity', default=1)
    rental_price = fields.Float(string='Unit Price', related='equipment_id.rental_price', readonly=True, store=True)
    subtotal     = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True, digits=(10, 2))

    @api.depends('quantity', 'rental_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.rental_price

    @api.constrains('quantity', 'equipment_id', 'booking_id')
    def _check_stock_availability(self):
        for line in self:
            if line.quantity <= 0:
                raise ValidationError("Quantity must be at least 1.")

            # Must match the booking's facility
            booking_facility   = line.booking_id.facility_id
            booking_sport_type = line.booking_id.sport_type_id

            if line.equipment_id.facility_id != booking_facility:
                raise ValidationError(
                    f"Equipment '{line.equipment_id.name}' does not belong to "
                    f"facility '{booking_facility.name}'."
                )

            # Must match the booking's sport type
            if line.equipment_id.sport_type_id != booking_sport_type:
                raise ValidationError(
                    f"Equipment '{line.equipment_id.name}' is for "
                    f"'{line.equipment_id.sport_type_id.name}', not "
                    f"'{booking_sport_type.name}'."
                )

            # Stock check across overlapping bookings at same facility
            overlapping_bookings = self.env['sports.facility.booking'].search([
                ('id',          '!=', line.booking_id.id),
                ('facility_id', '=',  booking_facility.id),
                ('state',       'in', ['confirmed', 'draft']),
                ('start_time',  '<',  line.booking_id.end_time),
                ('end_time',    '>',  line.booking_id.start_time),
            ])

            already_reserved = sum(
                ol.quantity
                for ol in self.search([
                    ('booking_id',   'in', overlapping_bookings.ids),
                    ('equipment_id', '=',  line.equipment_id.id),
                ])
            )

            available = line.equipment_id.stock_quantity - already_reserved
            if line.quantity > available:
                raise ValidationError(
                    f"Not enough stock for '{line.equipment_id.name}' "
                    f"at '{booking_facility.name}' during this time slot.\n"
                    f"Total: {line.equipment_id.stock_quantity} | "
                    f"Reserved: {already_reserved} | "
                    f"Available: {available} | "
                    f"Requested: {line.quantity}"
                )