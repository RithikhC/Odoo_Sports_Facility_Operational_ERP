# from odoo import api, models, fields, _
# from odoo.exceptions import UserError, ValidationError
 
 
# DURATION_OPTIONS = [
#     ('1', '1 Hour'),
#     ('2', '2 Hours'),
#     ('3', '3 Hours'),
#     ('4', '4 Hours'),
#     ('5', '5 Hours'),
# ]
 
 
# class SportsFacilityBooking(models.Model):
#     _name = 'sports.facility.booking'
#     _description = 'Court Reservation'
#     _order = 'start_time desc'
 
#     name = fields.Char(
#         string='Booking Reference',
#         copy=False,
#         readonly=True,
#         default='New',
#     )
 
#     partner_id = fields.Many2one('res.partner', string='Athlete / Customer', required=True)
#     court_id   = fields.Many2one('sports.facility.court', string='Assigned Court', required=True)
#     facility_id = fields.Many2one(
#         'sports.facility',
#         string='Facility',
#         related='court_id.facility_id',
#         store=True,
#         readonly=True,
#     )
#     coach_id = fields.Many2one('sports.coach', string='Coach (Optional)')
 
#     start_time = fields.Datetime(string='Start Time', required=True)
#     duration   = fields.Selection(
#         selection=DURATION_OPTIONS,
#         string='Duration',
#         required=True,
#         default='1',
#     )
#     end_time = fields.Datetime(
#         string='End Time',
#         compute='_compute_end_time',
#         store=True,
#         readonly=True,
#     )
 
#     # ── Membership ────────────────────────────
#     membership_id = fields.Many2one(
#         'sports.membership',
#         string='Membership Plan',
#         related='partner_id.membership_id',
#         readonly=True,
#         store=True,
#     )
#     discount_percentage = fields.Float(
#         string='Discount (%)',
#         related='partner_id.discount_percentage',
#         readonly=True,
#         store=True,
#     )
 
#     # ── Equipment ─────────────────────────────
#     equipment_line_ids = fields.One2many(
#         'sports.equipment.line', 'booking_id', string='Equipment'
#     )
 
#     # ── Pricing ───────────────────────────────
#     price_multiplier = fields.Float(
#         string='Price Multiplier',
#         compute='_compute_price_multiplier',
#         store=True,
#         digits=(4, 2),
#     )
#     applied_rule     = fields.Char(string='Applied Pricing Rule', readonly=True)
#     court_price      = fields.Float(string='Court Cost',      compute='_compute_total_price', store=True, digits=(10, 2))
#     coach_cost       = fields.Float(string='Coach Cost',      compute='_compute_total_price', store=True, digits=(10, 2))
#     equipment_cost   = fields.Float(string='Equipment Cost',  compute='_compute_total_price', store=True, digits=(10, 2))
#     discount_amount  = fields.Float(string='Discount Amount', compute='_compute_total_price', store=True, digits=(10, 2))
#     total_price      = fields.Float(string='Total Price',     compute='_compute_total_price', store=True, digits=(10, 2))
 
#     state = fields.Selection(
#         selection=[
#             ('draft',      'Draft'),
#             ('confirmed',  'Confirmed'),
#             ('done',       'Done'),
#             ('cancelled',  'Cancelled'),
#         ],
#         string='Status',
#         default='draft',
#         required=True,
#     )
 
#     # ── Sequence ──────────────────────────────
#     @api.model_create_multi
#     def create(self, vals_list):
#         for vals in vals_list:
#             if vals.get('name', 'New') == 'New':
#                 vals['name'] = (
#                     self.env['ir.sequence'].next_by_code('sports.facility.booking') or 'New'
#                 )
#         return super().create(vals_list)
 
#     # ── Compute end time from duration ────────
#     @api.depends('start_time', 'duration')
#     def _compute_end_time(self):
#         from datetime import timedelta
#         for record in self:
#             if record.start_time and record.duration:
#                 record.end_time = record.start_time + timedelta(hours=int(record.duration))
#             else:
#                 record.end_time = False
 
#     # ── Compute price multiplier ──────────────
#     @api.depends('start_time')
#     def _compute_price_multiplier(self):
#         PricingRule = self.env['sports.pricing.rule']
#         for record in self:
#             if record.start_time:
#                 multiplier = PricingRule.get_multiplier_for_datetime(record.start_time)
#                 record.price_multiplier = multiplier
#                 day   = str(record.start_time.weekday())
#                 hour  = record.start_time.hour + record.start_time.minute / 60.0
#                 rule  = PricingRule.search([
#                     ('day_of_week', '=',  day),
#                     ('start_hour',  '<=', hour),
#                     ('end_hour',    '>',  hour),
#                 ], order='price_multiplier desc', limit=1)
#                 record.applied_rule = rule.name if rule else 'Standard Rate'
#             else:
#                 record.price_multiplier = 1.0
#                 record.applied_rule     = 'Standard Rate'
 
#     # ── Compute total price ───────────────────
#     @api.depends(
#         'start_time', 'end_time',
#         'court_id', 'court_id.hourly_rate',
#         'coach_id', 'coach_id.hourly_fee',
#         'equipment_line_ids.subtotal',
#         'discount_percentage',
#         'price_multiplier',
#     )
#     def _compute_total_price(self):
#         for record in self:
#             hours = 0.0
#             if record.start_time and record.end_time:
#                 hours = max(
#                     (record.end_time - record.start_time).total_seconds() / 3600.0, 0
#                 )
#             base_rate      = record.court_id.hourly_rate if record.court_id else 0
#             multiplier     = record.price_multiplier or 1.0
#             court_price    = hours * base_rate * multiplier
#             coach_cost     = hours * (record.coach_id.hourly_fee if record.coach_id else 0)
#             equipment_cost = sum(record.equipment_line_ids.mapped('subtotal'))
#             subtotal       = court_price + coach_cost + equipment_cost
#             discount_amount = court_price * (record.discount_percentage / 100)
 
#             record.court_price     = court_price
#             record.coach_cost      = coach_cost
#             record.equipment_cost  = equipment_cost
#             record.discount_amount = discount_amount
#             record.total_price     = subtotal - discount_amount
 
#     # ── Court overlap constraint ──────────────
#     @api.constrains('start_time', 'end_time', 'court_id')
#     def _check_no_overlap(self):
#         for record in self:
#             if not record.start_time or not record.end_time:
#                 continue
#             overlapping = self.search([
#                 ('id',         '!=', record.id),
#                 ('court_id',   '=',  record.court_id.id),
#                 ('state',      'in', ['confirmed', 'draft']),
#                 ('start_time', '<',  record.end_time),
#                 ('end_time',   '>',  record.start_time),
#             ])
#             if overlapping:
#                 raise ValidationError(_(
#                     "This booking overlaps with reservation '%s' on court '%s'.",
#                     overlapping[0].name,
#                     record.court_id.name,
#                 ))
 
#     # ── Coach constraint: max 1 court at a time
#     @api.constrains('start_time', 'end_time', 'coach_id')
#     def _check_coach_availability(self):
#         for record in self:
#             if not record.coach_id or not record.start_time or not record.end_time:
#                 continue
#             overlapping = self.search([
#                 ('id',         '!=', record.id),
#                 ('coach_id',   '=',  record.coach_id.id),
#                 ('state',      'in', ['confirmed', 'draft']),
#                 ('start_time', '<',  record.end_time),
#                 ('end_time',   '>',  record.start_time),
#             ])
#             if overlapping:
#                 raise ValidationError(_(
#                     "Coach '%s' is already assigned to booking '%s' during this time. "
#                     "A coach can only be at one court at a time.",
#                     record.coach_id.name,
#                     overlapping[0].name,
#                 ))
 
#     # ── Membership validity check ─────────────
#     @api.constrains('partner_id', 'membership_id')
#     def _check_membership_validity(self):
#         for record in self:
#             if record.partner_id and record.partner_id.membership_expiry:
#                 if record.partner_id.membership_expiry < fields.Date.today():
#                     raise ValidationError(
#                         f"Customer '{record.partner_id.name}' has an expired membership. "
#                         f"Please renew before applying the discount."
#                     )
 
#     # ── Maintenance constraint ────────────────
#     @api.constrains('court_id', 'start_time', 'end_time')
#     def _check_court_maintenance(self):
#         for record in self:
#             if not record.court_id or not record.start_time or not record.end_time:
#                 continue
#             if record.court_id.state == 'maintenance':
#                 raise ValidationError(
#                     f"Court '{record.court_id.name}' is currently under maintenance."
#                 )
#             booking_hours    = (record.end_time - record.start_time).total_seconds() / 3600.0
#             projected_hours  = record.court_id.accumulated_hours + booking_hours
#             if projected_hours > record.court_id.maintenance_threshold:
#                 remaining = record.court_id.maintenance_threshold - record.court_id.accumulated_hours
#                 raise ValidationError(
#                     f"Court '{record.court_id.name}' only has {remaining:.1f} hours remaining "
#                     f"before maintenance. This booking requires {booking_hours:.1f} hours."
#                 )
 
#     # ── Workflow ──────────────────────────────
#     def action_confirm(self):
#         for record in self:
#             if record.state != 'draft':
#                 raise UserError("Only draft bookings can be confirmed.")
#             record.state = 'confirmed'
 
#     def action_done(self):
#         for record in self:
#             if record.state != 'confirmed':
#                 raise UserError("Only confirmed bookings can be marked as done.")
#             if record.start_time and record.end_time:
#                 hours = (record.end_time - record.start_time).total_seconds() / 3600.0
#                 record.court_id.accumulated_hours += int(hours)
#                 if record.court_id.accumulated_hours >= record.court_id.maintenance_threshold:
#                     record.court_id.state = 'maintenance'
#             record.state = 'done'
 
#     def action_reset_draft(self):
#         for record in self:
#             if record.state == 'done':
#                 raise UserError("Done bookings cannot be reset to draft.")
#             record.state = 'draft'
 
#     # ── Invoice generation ────────────────────
#     def action_create_invoice(self):
#         self.ensure_one()
#         if self.state not in ['confirmed', 'done']:
#             raise UserError("You can only invoice confirmed or done bookings.")
 
#         invoice_lines = []
 
#         # Court line
#         invoice_lines.append((0, 0, {
#             'name':          f"Court: {self.court_id.name} x {self.duration} hr(s) "
#                              f"[Multiplier: {self.price_multiplier}x — {self.applied_rule}]",
#             'quantity':      int(self.duration),
#             'price_unit':    self.court_id.hourly_rate * self.price_multiplier,
#         }))
 
#         # Coach line
#         if self.coach_id:
#             invoice_lines.append((0, 0, {
#                 'name':       f"Coach: {self.coach_id.name} x {self.duration} hr(s)",
#                 'quantity':   int(self.duration),
#                 'price_unit': self.coach_id.hourly_fee,
#             }))
 
#         # Equipment lines
#         for line in self.equipment_line_ids:
#             invoice_lines.append((0, 0, {
#                 'name':       f"Equipment: {line.equipment_id.name}",
#                 'quantity':   line.quantity,
#                 'price_unit': line.rental_price,
#             }))
 
#         # Discount line
#         if self.discount_amount > 0:
#             invoice_lines.append((0, 0, {
#                 'name':       f"Membership Discount ({self.discount_percentage}% — {self.membership_id.name})",
#                 'quantity':   1,
#                 'price_unit': -self.discount_amount,
#             }))
 
#         invoice = self.env['account.move'].create({
#             'move_type':            'out_invoice',
#             'partner_id':           self.partner_id.id,
#             'invoice_date':         fields.Date.today(),
#             'invoice_line_ids':     invoice_lines,
#             'narration':            f"Booking Reference: {self.name}",
#         })
 
#         return {
#             'type':      'ir.actions.act_window',
#             'name':      'Invoice',
#             'res_model': 'account.move',
#             'res_id':    invoice.id,
#             'view_mode': 'form',
#         }
 
#     @api.onchange('court_id')
#     def _onchange_court_id(self):
#         # Clear equipment lines when court changes
#         # since equipment is facility-specific
#         self.equipment_line_ids = [(5, 0, 0)]
#         self.facility_id = self.court_id.facility_id if self.court_id else False
 
#     @api.model
#     def _cron_auto_close_bookings(self):
#         now = fields.Datetime.now()
 
#         # Auto-done: confirmed bookings whose end time has passed
#         confirmed_ended = self.search([
#             ('state',    '=', 'confirmed'),
#             ('end_time', '<', now),
#         ])
#         confirmed_ended.write({'state': 'done'})
 
#         # Auto-cancelled: draft bookings whose end time has passed
#         draft_ended = self.search([
#             ('state',    '=', 'draft'),
#             ('end_time', '<', now),
#         ])
#         draft_ended.write({'state': 'cancelled'})

from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError


DURATION_OPTIONS = [
    ('1', '1 Hour'),
    ('2', '2 Hours'),
    ('3', '3 Hours'),
    ('4', '4 Hours'),
    ('5', '5 Hours'),
]


class SportsFacilityBooking(models.Model):
    _name = 'sports.facility.booking'
    _description = 'Court Reservation'
    _order = 'start_time desc'

    name = fields.Char(
        string='Booking Reference',
        copy=False,
        readonly=True,
        default='Sports Facility Booking',
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Athlete / Customer',
        required=True,
    )

    # ── Step 1: Sport selection ───────────────
    sport_type_id = fields.Many2one(
        'sports.type',
        string='Sport',
        required=True,
    )

    # ── Step 2: Facility (filtered by sport) ─
    facility_id = fields.Many2one(
        'sports.facility',
        string='Facility',
        required=True,
    )

    # ── Step 3: Court (filtered by sport+facility)
    court_id = fields.Many2one(
        'sports.facility.court',
        string='Court',
        required=True,
    )

    # ── Step 4: Coach (filtered by sport+facility)
    coach_id = fields.Many2one(
        'sports.coach',
        string='Coach (Optional)',
    )

    # ── Schedule ──────────────────────────────
    start_time = fields.Datetime(string='Start Time', required=True)
    duration   = fields.Selection(
        selection=DURATION_OPTIONS,
        string='Duration',
        required=True,
        default='1',
    )
    end_time = fields.Datetime(
        string='End Time',
        compute='_compute_end_time',
        store=True,
        readonly=True,
    )

    # ── Membership ────────────────────────────
    membership_id = fields.Many2one(
        'sports.membership',
        string='Membership Plan',
        related='partner_id.membership_id',
        readonly=True,
        store=True,
    )
    discount_percentage = fields.Float(
        string='Discount (%)',
        related='partner_id.discount_percentage',
        readonly=True,
        store=True,
    )

    # ── Equipment ─────────────────────────────
    equipment_line_ids = fields.One2many(
        'sports.equipment.line',
        'booking_id',
        string='Equipment',
    )

    # ── Pricing ───────────────────────────────
    price_multiplier = fields.Float(
        string='Price Multiplier',
        compute='_compute_price_multiplier',
        store=True,
        digits=(4, 2),
    )
    applied_rule    = fields.Char(string='Applied Pricing Rule', readonly=True)
    court_price     = fields.Float(string='Court Cost',      compute='_compute_total_price', store=True, digits=(10, 2))
    coach_cost      = fields.Float(string='Coach Cost',      compute='_compute_total_price', store=True, digits=(10, 2))
    equipment_cost  = fields.Float(string='Equipment Cost',  compute='_compute_total_price', store=True, digits=(10, 2))
    discount_amount = fields.Float(string='Discount Amount', compute='_compute_total_price', store=True, digits=(10, 2))
    total_price     = fields.Float(string='Total Price',     compute='_compute_total_price', store=True, digits=(10, 2))

    state = fields.Selection(
        selection=[
            ('draft',     'Draft'),
            ('confirmed', 'Confirmed'),
            ('done',      'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        required=True,
    )

    # ── Sequence ──────────────────────────────
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = (
                    self.env['ir.sequence'].next_by_code('sports.facility.booking') or 'New'
                )
        return super().create(vals_list)

    # ── Onchange: sport selected → reset downstream
    @api.onchange('sport_type_id')
    def _onchange_sport_type_id(self):
        self.facility_id       = False
        self.court_id          = False
        self.coach_id          = False
        self.equipment_line_ids = [(5, 0, 0)]

    # ── Onchange: facility selected → reset court/coach/equipment
    @api.onchange('facility_id')
    def _onchange_facility_id(self):
        self.court_id          = False
        self.coach_id          = False
        self.equipment_line_ids = [(5, 0, 0)]

    # ── Onchange: court selected → reset equipment
    @api.onchange('court_id')
    def _onchange_court_id(self):
        self.equipment_line_ids = [(5, 0, 0)]

    # ── Compute end time ──────────────────────
    @api.depends('start_time', 'duration')
    def _compute_end_time(self):
        from datetime import timedelta
        for record in self:
            if record.start_time and record.duration:
                record.end_time = record.start_time + timedelta(hours=int(record.duration))
            else:
                record.end_time = False

    # ── Compute price multiplier ──────────────
    @api.depends('start_time')
    def _compute_price_multiplier(self):
        PricingRule = self.env['sports.pricing.rule']
        for record in self:
            if record.start_time:
                day  = str(record.start_time.weekday())
                hour = record.start_time.hour + record.start_time.minute / 60.0
                rule = PricingRule.search([
                    ('day_of_week', '=',  day),
                    ('start_hour',  '<=', hour),
                    ('end_hour',    '>',  hour),
                ], order='price_multiplier desc', limit=1)
                record.price_multiplier = rule.price_multiplier if rule else 1.0
                record.applied_rule     = rule.name if rule else 'Standard Rate'
            else:
                record.price_multiplier = 1.0
                record.applied_rule     = 'Standard Rate'

    # ── Compute total price ───────────────────
    @api.depends(
        'start_time', 'end_time',
        'court_id', 'court_id.hourly_rate',
        'coach_id', 'coach_id.hourly_fee',
        'equipment_line_ids.subtotal',
        'discount_percentage',
        'price_multiplier',
    )
    def _compute_total_price(self):
        for record in self:
            hours = 0.0
            if record.start_time and record.end_time:
                hours = max(
                    (record.end_time - record.start_time).total_seconds() / 3600.0, 0
                )
            base_rate      = record.court_id.hourly_rate if record.court_id else 0
            multiplier     = record.price_multiplier or 1.0
            court_price    = hours * base_rate * multiplier
            coach_cost     = hours * (record.coach_id.hourly_fee if record.coach_id else 0)
            equipment_cost = sum(record.equipment_line_ids.mapped('subtotal'))
            subtotal       = court_price + coach_cost + equipment_cost
            discount_amount = court_price * (record.discount_percentage / 100)

            record.court_price     = court_price
            record.coach_cost      = coach_cost
            record.equipment_cost  = equipment_cost
            record.discount_amount = discount_amount
            record.total_price     = subtotal - discount_amount

    # ── Constraints ───────────────────────────
    @api.constrains('sport_type_id', 'court_id')
    def _check_court_sport_match(self):
        for record in self:
            if record.court_id and record.sport_type_id:
                if record.court_id.sport_type_id != record.sport_type_id:
                    raise ValidationError(
                        f"Court '{record.court_id.name}' is not set up for "
                        f"'{record.sport_type_id.name}'. Please select a matching court."
                    )

    @api.constrains('sport_type_id', 'coach_id')
    def _check_coach_sport_match(self):
        for record in self:
            if record.coach_id and record.sport_type_id:
                if record.coach_id.sport_type_id != record.sport_type_id:
                    raise ValidationError(
                        f"Coach '{record.coach_id.name}' specialises in "
                        f"'{record.coach_id.sport_type_id.name}', not "
                        f"'{record.sport_type_id.name}'."
                    )

    @api.constrains('facility_id', 'court_id')
    def _check_court_facility_match(self):
        for record in self:
            if record.court_id and record.facility_id:
                if record.court_id.facility_id != record.facility_id:
                    raise ValidationError(
                        f"Court '{record.court_id.name}' does not belong to "
                        f"facility '{record.facility_id.name}'."
                    )

    @api.constrains('facility_id', 'coach_id')
    def _check_coach_facility_match(self):
        for record in self:
            if record.coach_id and record.facility_id:
                if record.coach_id.facility_id != record.facility_id:
                    raise ValidationError(
                        f"Coach '{record.coach_id.name}' is not assigned to "
                        f"facility '{record.facility_id.name}'."
                    )

    @api.constrains('start_time', 'end_time', 'court_id')
    def _check_no_overlap(self):
        for record in self:
            if not record.start_time or not record.end_time:
                continue
            overlapping = self.search([
                ('id',         '!=', record.id),
                ('court_id',   '=',  record.court_id.id),
                ('state',      'in', ['confirmed', 'draft']),
                ('start_time', '<',  record.end_time),
                ('end_time',   '>',  record.start_time),
            ])
            if overlapping:
                raise ValidationError(_(
                    "This booking overlaps with reservation '%s' on court '%s'.",
                    overlapping[0].name,
                    record.court_id.name,
                ))

    @api.constrains('start_time', 'end_time', 'coach_id')
    def _check_coach_availability(self):
        for record in self:
            if not record.coach_id or not record.start_time or not record.end_time:
                continue
            overlapping = self.search([
                ('id',         '!=', record.id),
                ('coach_id',   '=',  record.coach_id.id),
                ('state',      'in', ['confirmed', 'draft']),
                ('start_time', '<',  record.end_time),
                ('end_time',   '>',  record.start_time),
            ])
            if overlapping:
                raise ValidationError(_(
                    "Coach '%s' is already assigned to booking '%s' during this time.",
                    record.coach_id.name,
                    overlapping[0].name,
                ))

    @api.constrains('partner_id', 'membership_id')
    def _check_membership_validity(self):
        for record in self:
            if record.partner_id and record.partner_id.membership_expiry:
                if record.partner_id.membership_expiry < fields.Date.today():
                    raise ValidationError(
                        f"Customer '{record.partner_id.name}' has an expired membership. "
                        f"Please renew before applying the discount."
                    )

    @api.constrains('court_id', 'start_time', 'end_time')
    def _check_court_maintenance(self):
        for record in self:
            if not record.court_id or not record.start_time or not record.end_time:
                continue
            if record.court_id.state == 'maintenance':
                raise ValidationError(
                    f"Court '{record.court_id.name}' is currently under maintenance "
                    f"and cannot be booked."
                )
            booking_hours   = (record.end_time - record.start_time).total_seconds() / 3600.0
            projected_hours = record.court_id.accumulated_hours + booking_hours
            if projected_hours > record.court_id.maintenance_threshold:
                remaining = record.court_id.maintenance_threshold - record.court_id.accumulated_hours
                raise ValidationError(
                    f"Court '{record.court_id.name}' only has {remaining:.1f} hours remaining "
                    f"before maintenance. This booking requires {booking_hours:.1f} hours."
                )

    # ── Workflow ──────────────────────────────
    def action_confirm(self):
        for record in self:
            if record.state != 'draft':
                raise UserError("Only draft bookings can be confirmed.")
            record.state = 'confirmed'

    def action_done(self):
        for record in self:
            if record.state != 'confirmed':
                raise UserError("Only confirmed bookings can be marked as done.")
            record._mark_done()

    def _mark_done(self):
        """Internal method used by both manual and cron done marking."""
        for record in self:
            if record.start_time and record.end_time:
                hours = (record.end_time - record.start_time).total_seconds() / 3600.0
                record.court_id.accumulated_hours += int(hours)
                if record.court_id.accumulated_hours >= record.court_id.maintenance_threshold:
                    record.court_id.state = 'maintenance'
            record.state = 'done'

    def action_reset_draft(self):
        for record in self:
            if record.state in ['done', 'cancelled']:
                raise UserError("Done or cancelled bookings cannot be reset to draft.")
            record.state = 'draft'


    def action_cancel(self):
        for record in self:
            if record.state == 'done':
                raise UserError("Cannot cancel a completed booking.")
            record.state = 'cancelled'

    def action_reset_draft(self):
        for record in self:
            if record.state == 'done':
                raise UserError("Done bookings cannot be reset to draft.")
            record.state = 'draft'

   