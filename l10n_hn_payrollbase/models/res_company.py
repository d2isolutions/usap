# -*- coding: utf-8 -*-

from odoo import fields, models, api


class res_company(models.Model):
    _inherit = 'res.company'

    payrollbase_id = fields.Many2one('l10n_hn.payrollbase', 'Base para honduras', help="Select, the current Configuration of the Honduran labor law.")