# -*- coding: utf-8 -*-

from odoo import models, fields, api



class HrPayslipEmployeesExt(models.TransientModel):
    _inherit = 'hr.payslip.employees'

    division_id = fields.Many2one('hr_employe.division', string='Tipo de Planilla')

    @api.onchange('division_id')
    def _onchange_division_id(self):
        if not self.division_id:
            return
        employee_ids = self.env['hr.employee'].search([('division_id', '=', self.division_id.id )])
        self.employee_ids = employee_ids