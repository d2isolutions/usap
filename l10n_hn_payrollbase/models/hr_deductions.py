# -*- coding: utf-8 -*-
import time
import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HRdeductions(models.Model):
    _name = 'hr.deductions'
    _order = 'datede desc'


    name = fields.Char(related='employee_id.name')
    employee_id = fields.Many2one('hr.employee', string='Empleado', required=True)
    contract_id = fields.Many2one('hr.contract', related='employee_id.contract_id', string='Contract' )
    state = fields.Selection([('draft', 'Borrador'), ('done', 'Hecho'), ('cancel', 'Cancelado')],
                             readonly=True, string='Estado', default='draft')

    datede = fields.Date(string='Fecha Deducción', default=fields.Date.context_today, required=True)
    type_id = fields.Many2one('hr.deductions.type', string='Tipo de Deducción')
    montode = fields.Float(string='Monto Fijo', states={'draft': [('readonly', False)]}, required=True)
    have_porc = fields.Boolean(string='Por % Salario', required=True)
    porc_de = fields.Float(string="% Deducción del Salario (0-100)", digits=(3, 0), default=10, required=True)
    amount = fields.Float(string='Monto Total', compute='_get_amount' )

    @api.depends('have_porc', 'montode', 'porc_de')
    def _get_amount(self):
        for record in self:
            if record.have_porc == True:
                record.amount = record.contract_id.wage * (record.porc_de/100)
            else:
                record.amount = record.montode
            return



    def action_validar(self):
        self.write({'state':'done'})

    def action_cancelar(self):
        self.write({'state':'cancel'})

    def action_draft(self):
        self.write({'state':'draft'})



class HrDeductionsType(models.Model):
    _name = 'hr.deductions.type'
    _description = 'hr.deductions.type'

    name = fields.Char(string='Nombre')
    code = fields.Char(string='Código')
    description = fields.Char(string='Descripción')

