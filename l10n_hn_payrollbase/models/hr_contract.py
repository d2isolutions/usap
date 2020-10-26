# -*- coding: utf-8 -*-
import time
import datetime
import logging
_logger = logging.getLogger(__name__)

from odoo import api, fields, models, _


class Contract(models.Model):
    _inherit = 'hr.contract'

    contract_type = fields.Selection(
        selection=[('01', 'Permanente'),
                   ('02', 'Temporal'),
                   ('03', 'Servicio'),
                    ],
        string=_('Tipo de Contrato'),
    )
    frequency = fields.Selection(
        selection=[('01', 'Diario'),
                   ('02', 'Semanal'),
                   ('03', 'Quincenal'),
                   ('04', 'Mensual'),
                   ],
        string=_('Frecuencia de Pago'), required=True)
    payrollbase_id = fields.Many2one('l10n_hn.payrollbase', related='company_id.payrollbase_id', string='Base para honduras')
    afp = fields.Float(string="Descuento por AFP")
    formmedexpenses = fields.Float(string="Descuento Gastos Médicos", compute='_get_formmedexpenses')
    age = fields.Integer(string='Edad', related='employee_id.age', readonly=True)
    division_id = fields.Many2one('hr_employe.division', related='employee_id.division_id', string='Tipo de Planilla')
    frequency_id = fields.Many2one('payment.frequency', string='Frecuencia de Pago')
    # Tabla de Comisiones
    commissions_ids = fields.One2many(comodel_name='hr.commissions', inverse_name='contract_id')
    #Tiene Comision
    havecommission = fields.Boolean(string='Tiene Comision')
    # Parametro de Configuracion
    averageparameter = fields.Integer(string='Parámetro Promedio', related='company_id.payrollbase_id.averageparameter', readonly=True)
    # Calculo de Comisiones
    lastcommission = fields.Float(string='Ultima Comision', default=0.00, compute='_get_lastcommission')
    averagecommission = fields.Float(string='Comision Promedio', default=0.00, compute='_get_averagecommission')

    holidays = fields.Float(string='Dias de Vacaciones', compute='_get_holidays')


    def _get_holidays(self):
        for record in self:
            today_date = datetime.date.today()
            if record.contract_type == '01':
                tiempo = (int((today_date - record.date_start).days/365))
                if tiempo == 0:
                    record.holidays = 0
                elif tiempo == 1:
                    record.holidays = 10
                elif tiempo == 2:
                    record.holidays = 12
                elif tiempo == 3:
                    record.holidays = 15
                elif tiempo >= 4:
                    record.holidays = 20
            else:
                record.holidays = 0


    @api.depends("date_ing")
    def _get_antique_employee(self):
        today_date = datetime.date.today()
        for employee in self:
            if employee.date_ing:
                date_ing = fields.Datetime.to_datetime(employee.date_ing).date()
                total_antique = str(int((today_date - date_ing).days / 365))
                employee.antique = total_antique
            else:
                employee.antique = 0





    @api.depends('commissions_ids', 'havecommission', 'lastcommission')
    def _get_averagecommission(self):
        if not self.commissions_ids: self.averagecommission = 0
        for record in self:
            for line in record.commissions_ids[0: record.averageparameter]:
                record.averagecommission += line.montocommission / record.averageparameter
            return


    @api.depends('commissions_ids', 'havecommission', 'averagecommission' )
    def _get_lastcommission(self):
        today_date = datetime.date.today()
        if not self.commissions_ids: self.lastcommission = 0
        for record in self:
            for line in record.commissions_ids[0:1]:
                if str(int((today_date - line.datecomisiones).days)) <= '30':
                    record.lastcommission = line.montocommission
                    #print('Prueba dias:', str(int((today_date - line.datecomisiones).days)))
                else:
                    record.lastcommission = 0


    @api.depends('age')
    def _get_formmedexpenses(self):
        for record in self:
            if record.age <= record.payrollbase_id.age_exp1:
                record.formmedexpenses = record.payrollbase_id.mdex_exp1
            elif record.age <= record.payrollbase_id.age_exp2:
                record.formmedexpenses = record.payrollbase_id.mdex_exp2
            elif record.age >= record.payrollbase_id.age_exp3:
                record.formmedexpenses = record.payrollbase_id.mdex_exp3
        return




class frequency(models.Model):
    _name = 'payment.frequency'
    _description = 'Payment Frequency'

    name = fields.Char(string='Nombre')


