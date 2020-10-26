# -*- coding: utf-8 -*-

from odoo import models, fields, api


class l10n_hn_payrollbase(models.Model):
    _name = 'l10n_hn.payrollbase'
    _order = 'id desc'
    _description = 'Honduras Configuration'

    name = fields.Char(string='Número Refencia', default="Gaceta Nro.", size=64, required=True,
                       help="Basis for honduras payroll adjustments")
    date = fields.Date(
        string='Date',
        default=fields.Date.context_today,
        help="Date on which goes into effect the new minimum salary")
    ceiling_salary_eym = fields.Float(string='Sueldo Techo EYM ', default=9380.67, required=True)
    ceiling_salary_ivm = fields.Float(string="Sueldo Techo IVM", default=9792.74, required=True)
    ceiling_salary_conf = fields.Float(string="Sueldo Techo Conf", default=9792.74, required=True)
    ceiling_salary_risk= fields.Float(string="Sueldo Techo Conf", default=9792.74, required=True)
    porc_eym = fields.Float(string="Empleado EYM % ", digits=(2, 4), default=0.025, required=True)
    porc_ivm = fields.Float(string="Empleado IVM % ", digits=(2, 4), default=0.025, required=True)
    porc_rap = fields.Float(string="Empleado RAP % ", digits=(2, 4), default=0.015, required=True)
    porc_eym_patrono = fields.Float(string="Patrono EYM % ", digits=(2, 4), default=0.050, required=True)
    porc_ivm_patrono = fields.Float(string="PatronoIVM % ", digits=(2, 4), default=0.035, required=True)
    porc_rap_patrono = fields.Float(string="Patrono RAP % ", digits=(2, 4), default=0.015, required=True)
    porc_risk_patrono = fields.Float(string="Patrono RP/SCL % ", digits=(2, 4), default=0.015, required=True)
    min_salary = fields.Float(string="Salario Mínimo", default=12029.47, required=True)
    months = fields.Float(string="Dto. mes ISR", digits=(2, 0), default=12)
    aexpenses1 = fields.Float(string="Dto. Gastos Medicos", default=40000.00)
    age_exp1 = fields.Integer(string='1| Edad límite', default=59)
    age_exp2 = fields.Integer(string='2| Edad límite', default=64)
    age_exp3 = fields.Integer(string='3| Edad límite', default=65)
    mdex_exp1 = fields.Float(string="Dto. Gastos Medicos", default=40000.00)
    mdex_exp2 = fields.Float(string="Dto. Gastos Medicos Mayor", default=70000.00)
    mdex_exp3 = fields.Float(string="Dto. Gastos Medicos Mayor 2", default=80000.00)
    mdex_exp4 = fields.Float(string="Descuento Adulto Mayor", default=350000.00)
    isrihss = fields.Float(string="Deducciones IHSS ", digits=(2, 2), default=9380.27, required=True)
    isrihssp = fields.Float(string="Deducciones IHSS%", digits=(2, 4), default=0.25, required=True)
    isrrap = fields.Float(string="Deducciones RAP%", digits=(2, 4), default=0.15, required=True)
    porc_islr1 = fields.Float(string="ISR %", digits=(2, 4), default=0.00, required=True)
    basemin1 = fields.Float(string="Base min", default=0.00, required=True)
    basemax1 = fields.Float(string="Base max", default=165482.06, required=True)
    difference1 = fields.Float(string="Diferencia 01", compute="_difference1", store=True)
    porc_islr2 = fields.Float(string="ISR %", digits=(2, 4), default=0.15, required=True)
    basemin2 = fields.Float(string="Base min", default=165482.068856, required=True)
    basemax2 = fields.Float(string="Base max", default=252330.802624, required=True)
    difference2 = fields.Float(string="Diferencia", compute="_difference2")
    porc_islr3 = fields.Float(string="ISR %", digits=(2, 4), default=0.20, required=True)
    basemin3 = fields.Float(string="Base min", default=252330.813032, required=True)
    basemax3 = fields.Float(string="Base max", default=586815.84184, required=True)
    difference3 = fields.Float(string="Diferencia", compute="_difference3")
    porc_islr4 = fields.Float(string="ISR %", digits=(2, 4), default=0.25, required=True)
    basemin4 = fields.Float(string="Base mayor a", default=586815.852248, required=True)
    basemax4 = fields.Float(string="Base max", default=9999999.99, required=True)
    difference4 = fields.Float(string="Diferencia 04")
    dd = fields.Float(string="Otras Deducciones", default=0.00)
    averageparameter = fields.Integer(string='Parámetro Promedio', default=6, required=True)
    sick_days = fields.Float(string='Dias al 100%', digits=(2, 0), default=3, required=True)
    porc_inc = fields.Float(string="% Patronal Incapacidad IHS", digits=(2, 4), default=0.34, required=True)
    daytime_conf = fields.Float(string="Horas Extras Diurnas %", digits=(2, 4), default=1.25, required=True)
    mixtime_conf = fields.Float(string="Horas Extras Mixta %", digits=(2, 4), default=1.50, required=True)
    nighttime_conf = fields.Float(string="Horas Extras Nocturnas %", digits=(2, 4), default=1.75, required=True)






    @api.depends('basemin1', 'basemax1')
    def _difference1(self):
        self.difference1 = float(self.basemax1) - float(self.basemin1)


    @api.depends('basemin2', 'basemax2')
    def _difference2(self):
        self.difference2 = float(self.basemax2) - float(self.basemin2)


    @api.depends('basemin3', 'basemax3')
    def _difference3(self):
        self.difference3 = float(self.basemax3) - float(self.basemin3)
