# -*- coding: utf-8 -*-

from openerp import models, fields


class AccountTax(models.Model):
    _inherit = 'account.tax'

    payability = fields.Selection([
        ('I', 'VAT payable immediately'),
        ('D', 'unrealized VAT'),
        ('S', 'split payments'),
    ], string="VAT payability")
