# -*- coding: utf-8 -*-
import time
import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HRAssignments(models.Model):
    _name = 'hr.assignments'
    _order = 'dateassig desc'


    name = fields.Char(related='employee_id.name')
    employee_id = fields.Many2one('hr.employee', string='Empleado', required=True)
    contract_id = fields.Many2one('hr.contract', related='employee_id.contract_id', string='Contract' )
    state = fields.Selection([('draft', 'Borrador'), ('done', 'Hecho'), ('cancel', 'Cancelado')],
                             readonly=True, string='Estado', default='draft')

    dateassig = fields.Date(string='Fecha Asignación', default=fields.Date.context_today, required=True)
    type_id = fields.Many2one('hr.assignments.type', string='Tipo de Asignaciones')
    montoassig = fields.Float(string='Monto Fijo', states={'draft': [('readonly', False)]}, required=True)
    have_porc = fields.Boolean(string='Por % Salario', required=True)
    porc_assig = fields.Float(string="% Asignacion del Salario (0-100)", digits=(3, 0), default=10, required=True)
    amount = fields.Float(string='Monto Total', compute='_get_amount' )

    @api.depends('have_porc', 'montoassig', 'porc_assig')
    def _get_amount(self):
        for record in self:
            if record.have_porc == True:
                record.amount = record.contract_id.wage * (record.porc_assig/100)
            else:
                record.amount = record.montoassig
            return



    def action_validar(self):
        self.write({'state':'done'})

    def action_cancelar(self):
        self.write({'state':'cancel'})

    def action_draft(self):
        self.write({'state':'draft'})



class HrAssignmentsType(models.Model):
    _name = 'hr.assignments.type'
    _description = 'hr.assignments.type'

    name = fields.Char(string='Nombre')
    code = fields.Char(string='Código')
    description = fields.Char(string='Descripción')



