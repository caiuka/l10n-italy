# -*- coding: utf-8 -*-
# Copyright 2019 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models
from openerp.tools.float_utils import float_round
from openerp.addons.l10n_it_fatturapa.bindings.fatturapa import (
    ScontoMaggiorazioneType
)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def setDettaglioLinea(
            self, line_no, line, body, price_precision, uom_precision):
        res = super(WizardExportFatturapa, self).setDettaglioLinea(
            line_no, line, body, price_precision, uom_precision)
        if line.discount2 or line.discount3:
            DettaglioLinea = body.DatiBeniServizi.DettaglioLinee[-1]
            if line.discount2:
                DettaglioLinea.ScontoMaggiorazione.append(
                    ScontoMaggiorazioneType(
                        Tipo='SC',
                        Percentuale='%.2f' % float_round(line.discount2, 2)
                    ))
            if line.discount3:
                DettaglioLinea.ScontoMaggiorazione.append(
                    ScontoMaggiorazioneType(
                        Tipo='SC',
                        Percentuale='%.2f' % float_round(line.discount3, 2)
                    ))
        return res
