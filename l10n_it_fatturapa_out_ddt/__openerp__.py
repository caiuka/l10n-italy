# -*- coding: utf-8 -*-
# Copyright 2018 Lorenzo Battistini
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# Copyright 2019 Sergio Corato
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    'name': 'ITA - Fattura elettronica - Integrazione DDT',
    "summary": "Modulo ponte tra emissione fatture elettroniche e DDT",
    "version": "8.0.2.0.0",
    "development_status": "Beta",
    "category": "Hidden",
    'website': 'https://github.com/OCA/l10n-italy/tree/10.0/'
               'l10n_it_fatturapa_out_ddt',
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "maintainers": [],
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "l10n_it_fatturapa_out",
        "l10n_it_ddt",
        "l10n_it_ddt_delivery",
        "stock_picking_invoice_link",
    ],
    "data": [
        "wizard/wizard_export_fatturapa_view.xml"
    ],
}
