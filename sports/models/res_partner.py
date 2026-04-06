# from odoo import models, fields


# class ResPartner(models.Model):
#     _inherit = 'res.partner'

#     membership_id = fields.Many2one(
#         'sports.membership',
#         string='Membership Plan',
#     )
#     discount_percentage = fields.Float(
#         string='Discount (%)',
#         related='membership_id.discount_percentage',
#         readonly=True,
#     )

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    membership_id     = fields.Many2one('sports.membership', string='Membership Plan')
    discount_percentage = fields.Float(
        string='Discount (%)',
        related='membership_id.discount_percentage',
        readonly=True,
    )
    membership_expiry = fields.Date(string='Membership Valid Until')
    membership_payment_ids = fields.One2many(
        'sports.membership.payment',
        'partner_id',
        string='Membership Payments',
    )