# Copyright 2016 Tecnativa - Pedro M. Baeza
# Copyright 2024 Tecnativa - Carolina Fernandez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.tools import SQL


class BasePartnerMergeAutomaticWizard(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    group_by_website = fields.Boolean("Website")

    def _generate_query(self, fields, maximum_group=100):
        """Inject the additional criteria 'website IS NOT NULL' when needed.
        There's no better way to do it, as there are no hooks for adding
        this criteria regularly.
        """
        query = super()._generate_query(fields, maximum_group=maximum_group)
        if "website" in fields:
            code, params, to_flush = query._sql_tuple
            index_where = code.find("WHERE")
            index_group_by = code.find("GROUP BY")
            criteria = code[index_where + 5 : index_group_by].strip()
            criteria = (
                f"website IS NOT NULL AND {criteria}"
                if criteria
                else "website IS NOT NULL"
            )
            code = f"{code[: index_where + 5]} {criteria}\n{code[index_group_by:]}"
            query = SQL(code, *params, to_flush=to_flush)
        return query
