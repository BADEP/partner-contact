# Copyright 2026 Roofing Industries Ltd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    company_group_id = fields.Many2one("res.partner", readonly=True)

    def _select_list(self, table):
        return [*super()._select_list(table), table.move_id.company_group_id]
