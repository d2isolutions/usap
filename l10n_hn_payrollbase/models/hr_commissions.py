# -*- coding: utf-8 -*-
import time
import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HRCommissions(models.Model):
    _name = 'hr.commissions'
    _order = 'datecomisiones desc'


    name = fields.Char(related='employee_id.name')
    employee_id = fields.Many2one('hr.employee', string='Empleado', required=True)
    contract_id = fields.Many2one('hr.contract', related='employee_id.contract_id', string='Contract' )
    state = fields.Selection([('draft', 'Borrador'), ('done', 'Hecho'), ('cancel', 'Cancelado')],
                             readonly=True, string='Estado', default='draft')

    datecomisiones = fields.Date(string='Fecha Comision', default=fields.Date.context_today, required=True)
    montocommission = fields.Float(string='Comision del Mes', states={'draft': [('readonly', False)]}, required=True)
    mescomisiones = fields.Selection(
        selection=[('01', 'Enero'),
                   ('02', 'Febrero'),
                   ('03', 'Marzo'),
                   ('04', 'Abril'),
                   ('05', 'Mayo'),
                   ('06', 'Junio'),
                   ('07', 'Julio'),
                   ('08', 'Agosto'),
                   ('09', 'Septiembre'),
                   ('10', 'Octubre'),
                   ('11', 'Noviembre'),
                   ('12', 'Diciembre'),
                   ],
        string=('Mes'), required=True)

    _sql_constraints = [
        ('unique_employee_mescomisiones', 'unique (employee_id, mescomisiones)',
         'Verifique la Lista del Empleado, solo debe tener un Monto Total de Comision por mes')
    ]


    # @api.model
    # def create(self, vals):
    #     res = super(HRCommissions, self).create(vals)
    #     if not self.mescomisiones or self.mescomisiones != (datetime.strptime(datecomisiones, "%m")):
    #         print('1', self.mescomisiones)
    #         print('2', datetime.strptime(datecomisiones, "%m"))
    #         raise UserError(_("Mes no corresponde a la Fecha"))
    #     return res

    def action_validar(self):
        self.write({'state':'done'})

    def action_cancelar(self):
        self.write({'state':'cancel'})

    def action_draft(self):
        self.write({'state':'draft'})

    # def unlink(self):
    #     raise UserError("Los registros no se pueden borrar, solo cancelar.")
