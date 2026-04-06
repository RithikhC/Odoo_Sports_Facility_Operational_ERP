# from odoo import api, models, fields
# from odoo.exceptions import UserError, ValidationError
# from odoo.tools import float_is_zero, float_compare


# class SportsFacility(models.Model):
#     _name = 'sports.facility'
#     _description = 'Sports Facility'
#     _order = 'name'

#     name     = fields.Char(string='Facility Name', required=True)
#     location = fields.Text(string='Location')
#     image    = fields.Binary(string='Facility Image', attachment=True)

#     court_ids = fields.One2many('sports.facility.court', 'facility_id', string='Courts')
#     equipment_ids = fields.One2many('sports.equipment', 'facility_id',string='Equipment')

#     total_courts     = fields.Integer(compute='_compute_court_stats', string='Total Courts')
#     available_courts = fields.Integer(compute='_compute_court_stats', string='Available Courts')
#     avg_hourly_rate  = fields.Float(compute='_compute_avg_hourly_rate', string='Avg. Hourly Rate')

#     state = fields.Selection(
#         selection=[
#             ('active',    'Active'),
#             ('suspended', 'Suspended'),
#             ('closed',    'Closed'),
#         ],
#         default='active',
#         string='Status',
#         required=True,
#     )

#     _check_name = models.Constraint(
#         'CHECK(name IS NOT NULL AND name != \'\')',
#         'Facility name cannot be empty!',
#     )

#     @api.depends('court_ids', 'court_ids.state')
#     def _compute_court_stats(self):
#         for record in self:
#             record.total_courts     = len(record.court_ids)
#             record.available_courts = len(
#                 record.court_ids.filtered(lambda c: c.state == 'available')
#             )

#     @api.depends('court_ids.hourly_rate')
#     def _compute_avg_hourly_rate(self):
#         for record in self:
#             if record.court_ids:
#                 record.avg_hourly_rate = (
#                     sum(record.court_ids.mapped('hourly_rate')) / len(record.court_ids)
#                 )
#             else:
#                 record.avg_hourly_rate = 0.0

#     def suspend_facility(self):
#         for record in self:
#             if record.state == 'closed':
#                 raise UserError("Closed facilities cannot be suspended.")
#             record.state = 'suspended'

#     def close_facility(self):
#         for record in self:
#             if record.state == 'suspended':
#                 raise UserError("Suspended facilities must be reactivated before closing.")
#             record.state = 'closed'

#     def reactivate_facility(self):
#         for record in self:
#             if record.state == 'active':
#                 raise UserError("This facility is already active.")
#             record.state = 'active'

#     @api.constrains('court_ids')
#     def _check_has_at_least_one_court(self):
#         for record in self:
#             if record.state == 'active' and not record.court_ids:
#                 raise ValidationError(
#                     "An active facility must have at least one court assigned."
#                 )

#     @api.constrains('avg_hourly_rate')
#     def _check_avg_hourly_rate(self):
#         for record in self:
#             if (
#                 not float_is_zero(record.avg_hourly_rate, precision_digits=2)
#                 and float_compare(record.avg_hourly_rate, 0.0, precision_digits=2) < 0
#             ):
#                 raise ValidationError(
#                     "The average hourly rate across courts cannot be negative."
#                 )

# from odoo import api, models, fields
# from odoo.exceptions import UserError, ValidationError
# from odoo.tools import float_is_zero, float_compare


# class SportsFacility(models.Model):
#     _name = 'sports.facility'
#     _description = 'Sports Facility'
#     _order = 'name'

#     name     = fields.Char(string='Facility Name', required=True)
#     location = fields.Text(string='Location')
#     image    = fields.Binary(string='Facility Image', attachment=True)

#     court_ids     = fields.One2many('sports.facility.court', 'facility_id', string='Courts')
#     equipment_ids = fields.One2many('sports.equipment', 'facility_id', string='Equipment')

#     total_courts     = fields.Integer(compute='_compute_court_stats', string='Total Courts')
#     available_courts = fields.Integer(compute='_compute_court_stats', string='Available Courts')
#     avg_hourly_rate  = fields.Float(compute='_compute_avg_hourly_rate', string='Avg. Hourly Rate')

#     state = fields.Selection(
#         selection=[
#             ('active',    'Active'),
#             ('suspended', 'Suspended'),
#             ('closed',    'Closed'),
#         ],
#         default='active',
#         string='Status',
#         required=True,
#     )

#     _check_name = models.Constraint(
#         'CHECK(name IS NOT NULL AND name != \'\')',
#         'Facility name cannot be empty!',
#     )

#     @api.depends('court_ids', 'court_ids.state')
#     def _compute_court_stats(self):
#         for record in self:
#             record.total_courts     = len(record.court_ids)
#             record.available_courts = len(
#                 record.court_ids.filtered(lambda c: c.state == 'available')
#             )

#     @api.depends('court_ids.hourly_rate')
#     def _compute_avg_hourly_rate(self):
#         for record in self:
#             if record.court_ids:
#                 record.avg_hourly_rate = (
#                     sum(record.court_ids.mapped('hourly_rate')) / len(record.court_ids)
#                 )
#             else:
#                 record.avg_hourly_rate = 0.0

#     def suspend_facility(self):
#         for record in self:
#             if record.state == 'closed':
#                 raise UserError("Closed facilities cannot be suspended.")
#             record.state = 'suspended'

#     def close_facility(self):
#         for record in self:
#             if record.state == 'suspended':
#                 raise UserError("Suspended facilities must be reactivated before closing.")
#             record.state = 'closed'

#     def reactivate_facility(self):
#         for record in self:
#             if record.state == 'active':
#                 raise UserError("This facility is already active.")
#             record.state = 'active'

#     @api.constrains('court_ids')
#     def _check_has_at_least_one_court(self):
#         for record in self:
#             if record.state == 'active' and not record.court_ids:
#                 raise ValidationError(
#                     "An active facility must have at least one court assigned."
#                 )

#     @api.constrains('avg_hourly_rate')
#     def _check_avg_hourly_rate(self):
#         for record in self:
#             if (
#                 not float_is_zero(record.avg_hourly_rate, precision_digits=2)
#                 and float_compare(record.avg_hourly_rate, 0.0, precision_digits=2) < 0
#             ):
#                 raise ValidationError(
#                     "The average hourly rate across courts cannot be negative."
#                 )

# from odoo import api, models, fields
# from odoo.exceptions import UserError, ValidationError
# from odoo.tools import float_is_zero, float_compare


# class SportsFacility(models.Model):
#     _name = 'sports.facility'
#     _description = 'Sports Facility'
#     _order = 'name'

#     name     = fields.Char(string='Facility Name', required=True)
#     location = fields.Text(string='Location')

#     court_ids     = fields.One2many('sports.facility.court', 'facility_id', string='Courts')
#     locker_ids = fields.One2many('sports.locker', 'facility_id', string='Lockers')
#     equipment_ids = fields.One2many('sports.equipment', 'facility_id', string='Equipment')
#     coach_ids     = fields.One2many('sports.coach', 'facility_id', string='Coaches')

#     total_courts          = fields.Integer(compute='_compute_court_stats', string='Total Courts', store=True)
#     available_courts      = fields.Integer(compute='_compute_court_stats', string='Available Courts', store=True)
#     courts_in_maintenance = fields.Integer(compute='_compute_court_stats', string='Courts in Maintenance', store=True)
#     avg_hourly_rate       = fields.Float(compute='_compute_avg_hourly_rate', string='Avg. Hourly Rate', store=True)

#     state = fields.Selection(
#         selection=[
#             ('active',    'Active'),
#             ('suspended', 'Suspended'),
#             ('closed',    'Closed'),
#         ],
#         default='active',
#         string='Status',
#         required=True,
#     )

#     _check_name = models.Constraint(
#         'CHECK(name IS NOT NULL AND name != \'\')',
#         'Facility name cannot be empty!',
#     )

#     @api.depends('court_ids', 'court_ids.state')
#     def _compute_court_stats(self):
#         for record in self:
#             record.total_courts          = len(record.court_ids)
#             record.available_courts      = len(record.court_ids.filtered(lambda c: c.state == 'available'))
#             record.courts_in_maintenance = len(record.court_ids.filtered(lambda c: c.state == 'maintenance'))

#     @api.depends('court_ids.hourly_rate')
#     def _compute_avg_hourly_rate(self):
#         for record in self:
#             if record.court_ids:
#                 record.avg_hourly_rate = (
#                     sum(record.court_ids.mapped('hourly_rate')) / len(record.court_ids)
#                 )
#             else:
#                 record.avg_hourly_rate = 0.0

#     def suspend_facility(self):
#         for record in self:
#             if record.state == 'closed':
#                 raise UserError("Closed facilities cannot be suspended.")
#             record.state = 'suspended'

#     def close_facility(self):
#         for record in self:
#             if record.state == 'suspended':
#                 raise UserError("Suspended facilities must be reactivated before closing.")
#             record.state = 'closed'

#     def reactivate_facility(self):
#         for record in self:
#             if record.state == 'active':
#                 raise UserError("This facility is already active.")
#             record.state = 'active'

#     @api.constrains('court_ids')
#     def _check_has_at_least_one_court(self):
#         for record in self:
#             if record.state == 'active' and not record.court_ids:
#                 raise ValidationError(
#                     "An active facility must have at least one court assigned."
#                 )

#     @api.constrains('avg_hourly_rate')
#     def _check_avg_hourly_rate(self):
#         for record in self:
#             if (
#                 not float_is_zero(record.avg_hourly_rate, precision_digits=2)
#                 and float_compare(record.avg_hourly_rate, 0.0, precision_digits=2) < 0
#             ):
#                 raise ValidationError(
#                     "The average hourly rate across courts cannot be negative."
#                 )
#     # def _check_facility_court_states(self):
#     #     for record in self:
#     #         if not record.court_ids:
#     #             continue
#     #             all_maintenance = all(
#     #             c.state == 'maintenance' for c in record.court_ids
#     #             )
#     #         if all_maintenance and record.state == 'active':
#     #             record.state = 'suspended'
#     #         elif not all_maintenance and record.state == 'suspended':
#     #             record.state = 'active'

#     def _check_facility_court_states(self):
#         for record in self:
#             courts = record.court_ids
#             if not courts:
#                 continue
#                 all_maintenance = all(c.state == 'maintenance' for c in courts)
#                 any_available   = any(c.state == 'available'   for c in courts)
#             if all_maintenance and record.state == 'active':
#                 record.state = 'suspended'
#             elif any_available and record.state == 'suspended':
#                 record.state = 'active'

from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class SportsFacility(models.Model):
    _name = 'sports.facility'
    _description = 'Sports Facility'
    _order = 'name'

    name     = fields.Char(string='Facility Name', required=True)
    location = fields.Text(string='Location')

    court_ids     = fields.One2many('sports.facility.court', 'facility_id', string='Courts')
    locker_ids    = fields.One2many('sports.locker', 'facility_id', string='Lockers')
    equipment_ids = fields.One2many('sports.equipment', 'facility_id', string='Equipment')
    coach_ids     = fields.One2many('sports.coach', 'facility_id', string='Coaches')

    total_courts          = fields.Integer(compute='_compute_court_stats', string='Total Courts', store=True)
    available_courts      = fields.Integer(compute='_compute_court_stats', string='Available Courts', store=True)
    courts_in_maintenance = fields.Integer(compute='_compute_court_stats', string='Courts in Maintenance', store=True)
    avg_hourly_rate       = fields.Float(compute='_compute_avg_hourly_rate', string='Avg. Hourly Rate', store=True)

    state = fields.Selection(
        selection=[
            ('active',    'Active'),
            ('suspended', 'Suspended'),
            ('closed',    'Closed'),
        ],
        default='active',
        string='Status',
        required=True,
    )

    _check_name = models.Constraint(
        'CHECK(name IS NOT NULL AND name != \'\')',
        'Facility name cannot be empty!',
    )

    @api.depends('court_ids', 'court_ids.state')
    def _compute_court_stats(self):
        for record in self:
            record.total_courts          = len(record.court_ids)
            record.available_courts      = len(record.court_ids.filtered(lambda c: c.state == 'available'))
            record.courts_in_maintenance = len(record.court_ids.filtered(lambda c: c.state == 'maintenance'))

    @api.depends('court_ids.hourly_rate')
    def _compute_avg_hourly_rate(self):
        for record in self:
            if record.court_ids:
                record.avg_hourly_rate = (
                    sum(record.court_ids.mapped('hourly_rate')) / len(record.court_ids)
                )
            else:
                record.avg_hourly_rate = 0.0

    def _check_facility_court_states(self):
        for record in self:
            courts = record.court_ids
            if not courts:
                continue
            all_maintenance = all(c.state == 'maintenance' for c in courts)
            any_available   = any(c.state == 'available'   for c in courts)
            if all_maintenance and record.state == 'active':
                record.state = 'suspended'
            elif any_available and record.state == 'suspended':
                record.state = 'active'

    def suspend_facility(self):
        for record in self:
            if record.state == 'closed':
                raise UserError("Closed facilities cannot be suspended.")
            record.state = 'suspended'

    def close_facility(self):
        for record in self:
            if record.state == 'suspended':
                raise UserError("Suspended facilities must be reactivated before closing.")
            record.state = 'closed'

    def reactivate_facility(self):
        for record in self:
            if record.state == 'active':
                raise UserError("This facility is already active.")
            record.state = 'active'

    @api.constrains('court_ids')
    def _check_has_at_least_one_court(self):
        for record in self:
            if record.state == 'active' and not record.court_ids:
                raise ValidationError(
                    "An active facility must have at least one court assigned."
                )

    @api.constrains('avg_hourly_rate')
    def _check_avg_hourly_rate(self):
        for record in self:
            if (
                not float_is_zero(record.avg_hourly_rate, precision_digits=2)
                and float_compare(record.avg_hourly_rate, 0.0, precision_digits=2) < 0
            ):
                raise ValidationError(
                    "The average hourly rate across courts cannot be negative."
                )