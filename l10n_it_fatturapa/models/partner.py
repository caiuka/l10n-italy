# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio <davide.corio@abstract.it>
# Copyright 2018 Gianmarco Conte, Marco Calcagni - Dinamiche Aziendali srl
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import fields, models, api, _
from openerp.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    eori_code = fields.Char('EORI Code', size=20)
    license_number = fields.Char('License Code', size=20)
    # 1.2.6 RiferimentoAmministrazione
    pa_partner_code = fields.Char('PA Code for partner', size=20)
    # 1.2.1.4
    register = fields.Char('Professional Register', size=60)
    # 1.2.1.5
    register_province = fields.Many2one(
        'res.country.state', string='Register Province')
    # 1.2.1.6
    register_code = fields.Char('Register Registration Number', size=60)
    # 1.2.1.7
    register_regdate = fields.Date('Register Registration Date')
    # 1.2.1.8
    register_fiscalpos = fields.Many2one(
        'fatturapa.fiscal_position',
        string="Register Fiscal Position")
    # 1.1.4
    codice_destinatario = fields.Char(
        "Addressee Code",
        help="The code, 7 characters long, assigned by ES to subjects with an "
             "accredited channel; if the addressee didn't accredit a channel "
             "to ES and invoices are received by PEC, the field must be "
             "filled with zeros ('0000000').",
        default='0000000')
    # 1.1.6
    pec_destinatario = fields.Char(
        "Addressee PEC",
        help="PEC to which the Electronic Invoice will be sent. "
             "Must be filled "
             "ONLY when the information element "
             "<CodiceDestinatario> is '0000000'"
    )
    electronic_invoice_subjected = fields.Boolean(
        "Subjected to electronic invoice")

    electronic_invoice_no_contact_update = fields.Boolean(
        "Do not update the contact from Electronic Invoice Details")

    @api.multi
    @api.constrains(
        'is_pa', 'ipa_code', 'codice_destinatario', 'is_company',
        'electronic_invoice_subjected', 'vat', 'fiscalcode', 'lastname',
        'firstname', 'customer', 'street', 'zip', 'city',
        'country_id'
    )
    def _check_ftpa_partner_data(self):
        for partner in self:
            if partner.electronic_invoice_subjected and partner.customer:
                # These checks must be done for customers only, as only
                # needed for XML generation
                if partner.is_pa and \
                        (not partner.ipa_code or len(partner.ipa_code) != 6):
                    raise ValidationError(_(
                        "As a Public Administration, partner %s IPA Code "
                        "must be 6 characters long"
                    ) % partner.name)
                if not partner.is_company and \
                        (not partner.lastname or not partner.firstname):
                    raise ValidationError(_(
                        "As a natural person, partner %s "
                        "must have Name and Surname"
                    ) % partner.name)
                if not partner.country_id:
                    raise ValidationError(_(
                        'Customer %s: country is needed for XML'
                        ' generation.'
                    ) % partner.name)
                if (
                    not partner.is_pa
                    and partner.codice_destinatario
                    and len(partner.codice_destinatario) != 7
                ):
                    raise ValidationError(_(
                        "Partner %s Addressee Code "
                        "must be 7 characters long."
                    ) % partner.name)
                if (
                    not partner.vat and not partner.fiscalcode and
                    partner.country_id.code == 'IT'
                ):
                    raise ValidationError(_(
                        "Italian Partner %s, must have VAT Number or Fiscal"
                        " Code"
                    ) % partner.name)
                if not partner.street:
                    raise ValidationError(_(
                        'Customer %s: street is needed for XML generation.'
                    ) % partner.name)
                if not partner.zip and partner.country_id.code == 'IT':
                    raise ValidationError(_(
                        'Italian Partner %s: ZIP is needed for XML generation.'
                    ) % partner.name)
                if not partner.city:
                    raise ValidationError(_(
                        'Customer %s: city is needed for XML generation.'
                    ) % partner.name)

    @api.onchange('country_id')
    def onchange_country_id_e_inv(self):
        if self.country_id.code == 'IT':
            self.codice_destinatario = '0000000'
        else:
            self.codice_destinatario = 'XXXXXXX'
