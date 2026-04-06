from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class SportsMembership(models.Model):
    _name = 'sports.membership'
    _description = 'Membership Plan'
    _order = 'name'

    name                = fields.Char(string='Plan Name', required=True)
    discount_percentage = fields.Float(string='Discount (%)', digits=(5, 2))
    annual_fee          = fields.Float(string='Annual Fee', digits=(10, 2))
    member_ids          = fields.One2many('res.partner', 'membership_id', string='Members')


class PartnerMembershipPayment(models.Model):
    _name = 'sports.membership.payment'
    _description = 'Membership Payment'
    _order = 'payment_date desc'

    partner_id    = fields.Many2one('res.partner', string='Member', required=True, ondelete='cascade')
    membership_id = fields.Many2one('sports.membership', string='Plan', required=True)
    payment_date  = fields.Date(string='Payment Date', default=fields.Date.today)
    expiry_date   = fields.Date(string='Valid Until', compute='_compute_expiry_date', store=True)
    amount_paid   = fields.Float(string='Amount Paid', digits=(10, 2), required=True)

    state = fields.Selection(
        selection=[
            ('active',  'Active'),
            ('expired', 'Expired'),
        ],
        default='active',
        string='Status',
        required=True,
    )

    @api.depends('payment_date')
    def _compute_expiry_date(self):
        for record in self:
            if record.payment_date:
                record.expiry_date = record.payment_date + relativedelta(years=1)
            else:
                record.expiry_date = False

    @api.constrains('amount_paid', 'membership_id')
    def _check_amount(self):
        for record in self:
            if record.amount_paid <= 0:
                raise ValidationError("Amount paid must be greater than zero.")
            if record.amount_paid < record.membership_id.annual_fee:
                raise ValidationError(
                    f"Amount paid ({record.amount_paid}) is less than the "
                    f"annual fee ({record.membership_id.annual_fee}) "
                    f"for plan '{record.membership_id.name}'."
                )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            # Immediately link membership and expiry to the partner
            record.partner_id.write({
                'membership_id':     record.membership_id.id,
                'membership_expiry': record.expiry_date,
            })
        return records

    @api.model
    def _cron_expire_memberships(self):
        expired = self.search([
            ('state',       '=',  'active'),
            ('expiry_date', '<',  fields.Date.today()),
        ])
        expired.write({'state': 'expired'})










# from odoo import models, fields, api
# from odoo.exceptions import ValidationError
# from datetime import date
# from dateutil.relativedelta import relativedelta


# class SportsMembership(models.Model):
#     _name = 'sports.membership'
#     _description = 'Membership Plan'
#     _order = 'name'

#     name                = fields.Char(string='Plan Name', required=True)
#     discount_percentage = fields.Float(string='Discount (%)', digits=(5, 2))
#     annual_fee          = fields.Float(string='Annual Fee', digits=(10, 2))
#     member_ids          = fields.One2many('res.partner', 'membership_id', string='Members')


# class PartnerMembershipPayment(models.Model):
#     _name = 'sports.membership.payment'
#     _description = 'Membership Payment'
#     _order = 'payment_date desc'

#     partner_id    = fields.Many2one('res.partner', string='Member', required=True, ondelete='cascade')
#     membership_id = fields.Many2one('sports.membership', string='Plan', required=True)
#     payment_date  = fields.Date(string='Payment Date', default=fields.Date.today)
#     expiry_date   = fields.Date(string='Valid Until', compute='_compute_expiry_date', store=True)
#     amount_paid   = fields.Float(string='Amount Paid', digits=(10, 2))
#     state         = fields.Selection(
#         selection=[
#             ('pending',  'Pending'),
#             ('paid',     'Paid'),
#             ('expired',  'Expired'),
#         ],
#         default='pending',
#         string='Status',
#     )

#     @api.depends('payment_date')
#     def _compute_expiry_date(self):
#         for record in self:
#             if record.payment_date:
#                 record.expiry_date = record.payment_date + relativedelta(years=1)
#             else:
#                 record.expiry_date = False

#     @api.constrains('amount_paid', 'membership_id')
#     def _check_amount(self):
#         for record in self:
#             if record.amount_paid <= 0:
#                 raise ValidationError("Amount paid must be greater than zero.")
#             if record.amount_paid < record.membership_id.annual_fee:
#                 raise ValidationError(
#                     f"Amount paid ({record.amount_paid}) is less than the annual fee "
#                     f"({record.membership_id.annual_fee}) for plan '{record.membership_id.name}'."
#                 )

#     def action_mark_paid(self):
#         for record in self:
#             record.state = 'paid'
#             record.partner_id.membership_expiry = record.expiry_date

#     # ── Cron: expire memberships ──────────────
#     @api.model
#     def _cron_expire_memberships(self):
#         expired = self.search([
#             ('state',       '=',  'paid'),
#             ('expiry_date', '<',  fields.Date.today()),
#         ])
#         expired.write({'state': 'expired'})






# from odoo import models, fields, api
# from odoo.exceptions import ValidationError
# from datetime import date
# from dateutil.relativedelta import relativedelta


# class SportsMembership(models.Model):
#     _name = 'sports.membership'
#     _description = 'Membership Plan'
#     _order = 'name'

#     name                = fields.Char(string='Plan Name', required=True)
#     discount_percentage = fields.Float(string='Discount (%)', digits=(5, 2))
#     annual_fee          = fields.Float(string='Annual Fee', digits=(10, 2))
#     member_ids          = fields.One2many('res.partner', 'membership_id', string='Members')


# class PartnerMembershipPayment(models.Model):
#     _name = 'sports.membership.payment'
#     _description = 'Membership Payment'
#     _order = 'payment_date desc'

#     partner_id    = fields.Many2one('res.partner', string='Member', required=True, ondelete='cascade')
#     membership_id = fields.Many2one('sports.membership', string='Plan', required=True)
#     payment_date  = fields.Date(string='Payment Date', default=fields.Date.today)
#     expiry_date   = fields.Date(string='Valid Until', compute='_compute_expiry_date', store=True)
#     amount_paid   = fields.Float(string='Amount Paid', digits=(10, 2))
#     state         = fields.Selection(
#         selection=[
#             ('pending',  'Pending'),
#             ('paid',     'Paid'),
#             ('expired',  'Expired'),
#         ],
#         default='pending',
#         string='Status',
#     )

#     @api.depends('payment_date')
#     def _compute_expiry_date(self):
#         for record in self:
#             if record.payment_date:
#                 record.expiry_date = record.payment_date + relativedelta(years=1)
#             else:
#                 record.expiry_date = False


#     @api.constrains('amount_paid', 'membership_id', 'state')
#     def _check_amount(self):
#         for record in self:
#             if record.state == 'paid':
#                 if record.amount_paid <= 0:
#                     raise ValidationError("Amount paid must be greater than zero.")
#                 if record.amount_paid < record.membership_id.annual_fee:
#                     raise ValidationError(
#                         f"Amount paid ({record.amount_paid}) is less than the annual fee "
#                         f"({record.membership_id.annual_fee}) for plan '{record.membership_id.name}'."
#                     )
#     def action_mark_paid(self):
#         for record in self:
#             record.state = 'paid'
#             record.partner_id.membership_expiry = record.expiry_date

#     # ── Cron: expire memberships ──────────────
#     @api.model
#     def _cron_expire_memberships(self):
#         expired = self.search([
#             ('state',       '=',  'paid'),
#             ('expiry_date', '<',  fields.Date.today()),
#         ])
#         expired.write({'state': 'expired'})

# from odoo import models, fields, api
# from odoo.exceptions import ValidationError
# from dateutil.relativedelta import relativedelta


# class SportsMembership(models.Model):
#     _name = 'sports.membership'
#     _description = 'Membership Plan'
#     _order = 'name'

#     name                = fields.Char(string='Plan Name', required=True)
#     discount_percentage = fields.Float(string='Discount (%)', digits=(5, 2))
#     annual_fee          = fields.Float(string='Annual Fee', digits=(10, 2))
#     member_ids          = fields.One2many('res.partner', 'membership_id', string='Members')


# class PartnerMembershipPayment(models.Model):
#     _name = 'sports.membership.payment'
#     _description = 'Membership Payment'
#     _order = 'payment_date desc'

#     partner_id    = fields.Many2one('res.partner', string='Member', required=True, ondelete='cascade')
#     membership_id = fields.Many2one('sports.membership', string='Plan', required=True)
#     payment_date  = fields.Date(string='Payment Date', default=fields.Date.today)
#     expiry_date   = fields.Date(string='Valid Until', compute='_compute_expiry_date', store=True)
#     amount_paid   = fields.Float(string='Amount Paid', digits=(10, 2))
#     state         = fields.Selection(
#         selection=[
#             ('pending', 'Pending'),
#             ('paid',    'Paid'),
#             ('expired', 'Expired'),
#         ],
#         default='pending',
#         string='Status',
#     )

#     @api.depends('payment_date')
#     def _compute_expiry_date(self):
#         for record in self:
#             if record.payment_date:
#                 record.expiry_date = record.payment_date + relativedelta(years=1)
#             else:
#                 record.expiry_date = False

#     @api.constrains('amount_paid', 'membership_id', 'state')
#     def _check_amount(self):
#         for record in self:
#             if record.state == 'paid':
#                 if record.amount_paid <= 0:
#                     raise ValidationError("Amount paid must be greater than zero.")
#                 if record.amount_paid < record.membership_id.annual_fee:
#                     raise ValidationError(
#                         f"Amount paid ({record.amount_paid}) is less than the annual fee "
#                         f"({record.membership_id.annual_fee}) for plan '{record.membership_id.name}'."
#                     )

#     def action_mark_paid(self):
#         for record in self:
#             record.state = 'paid'
#             record.partner_id.membership_expiry = record.expiry_date

#     @api.model
#     def _cron_expire_memberships(self):
#         expired = self.search([
#             ('state',       '=',  'paid'),
#             ('expiry_date', '<',  fields.Date.today()),
#         ])
#         expired.write({'state': 'expired'})