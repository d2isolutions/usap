# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models

class Hrpayslip(models.Model):
    _inherit = 'hr.payslip'


    payrollbase_id = fields.Many2one('l10n_hn.payrollbase', related='company_id.payrollbase_id')
    employee_id = fields.Many2one('hr.employee', "Employee", required=True)
    division_id = fields.Many2one('hr_employe.division', string='Tipo de Planilla', related='employee_id.division_id')
    computo_rap = fields.Float(string="Calcula RAP", compute='_get_computo_rap' )
    computo_ivm = fields.Float(string="Calcula IVM", compute='_get_computo_ivm' )
    computo_eym = fields.Float(string="Calcula EYM", compute='_get_computo_eym' )
    computo_isr = fields.Float(string="Calcula ISR", compute='_get_computo_isr' )
    commissions_ids = fields.One2many(comodel_name='hr.commissions', inverse_name='contract_id')
    computo_ajuste = fields.Float(string="Calcular Ajuste Sueldo minimo", default=0.00, compute='_get_computo_ajuste')
    # Bruto menos el Total de Ausencias
    computo_salario = fields.Float(string="Calcula Salario", compute='_get_computo_salario')
    computo_bruto = fields.Float(string="Salario Bruto", compute='_get_computo_bruto')
    # Total de Ausencias
    computo_ausencias = fields.Float(string="Calcula Ausencias", compute='_get_computo_ausencias')
    computo_incapacidad = fields.Float(string="Calcula Incapacidad", compute='_get_computo_incapacidad')
    # Calcular Incapacidad Menor a tres dias # Calcular Incapacidad Mayor a tres dias
    computo_incabono = fields.Float(string="Calcula Bono de Incapacidad", compute='_get_computo_incabono')
    computo_extrahours = fields.Float(string="Calcula Horas Extras", compute='_get_computo_extrahours')
    # Calculo de Asignaciones
    assignments_ids = fields.One2many(comodel_name='hr.assignments', inverse_name='contract_id')
    computo_assignments = fields.Float(string='Asignaciones', compute='_get_assignments')
    # Calculo de Deducion
    deductions_ids = fields.One2many(comodel_name='hr.deductions', inverse_name='contract_id')
    computo_deductions = fields.Float(string='Deducción', compute='_get_deductions')
    # Calculo de Feriados
    computo_feriados = fields.Float(string='Feriados', compute='_get_computo_feriados')
    # Calculo de Vacaciones
    computo_holidays = fields.Float(string='Vacaciones', compute='_get_computo_holidays')
    # Calcular comisiones
    computo_commission = fields.Float(string='Commission', compute='_get_commission')


    # Bien Funcionando --- Verificado
    def _get_commission(self):
        for record in self:
            commission = self.env['hr.commissions'].search([
                ('contract_id', '=', record.contract_id.id),
                ('datecomisiones', '>=', record.date_from),
                ('datecomisiones', '<=', record.date_to)])
            if record.contract_id.havecommission == True:
                for line in commission:
                    record.computo_commission += line.montocommission
        return record.computo_commission


    # Bien Funcionando --- Verificado
    def _get_computo_holidays(self):
        for record in self:
            for line in record.worked_days_line_ids:
                if line.work_entry_type_id.holidays == True:
                    salario = (record.contract_id.wage/30/8)
                    comision = (record.contract_id.averagecommission/30/8)
                    valorhora = salario + comision
                    record.computo_holidays = line.number_of_hours * valorhora
            return record.computo_holidays


    # Bien Funcionando --- Verificado
    def _get_computo_feriados(self):
        for record in self:
            for line in record.worked_days_line_ids:
                if line.work_entry_type_id.natholidays == True:
                    valorhora = (record.contract_id.wage/30/8)*2
                    record.computo_feriados = line.number_of_hours * valorhora
            return record.computo_feriados

    # Bien Funcionando --- Verificado
    def _get_deductions(self):
        for record in self:
            deductions = self.env['hr.deductions'].search([
                ('contract_id', '=', record.contract_id.id),
                ('datede', '>=', record.date_from),
                ('datede', '<=', record.date_to)])
            for line in deductions:
                record.computo_deductions += line.amount
            return record.computo_deductions

    # Bien Funcionando --- Verificado
    def _get_assignments(self):
        for record in self:
            assignments = self.env['hr.assignments'].search([
                ('contract_id', '=', record.contract_id.id),
                ('dateassig', '>=', record.date_from),
                ('dateassig', '<=', record.date_to)])
            for line in assignments:
                record.computo_assignments += line.amount
            return record.computo_assignments

    # Bien Funcionando --- Verificado
    def _get_computo_extrahours(self):
        for record in self:
            for line in record.worked_days_line_ids:
                if line.work_entry_type_id.daytime == True:
                    valorhora = (record.contract_id.wage/30/8)*record.payrollbase_id.daytime_conf
                    record.computo_extrahours += line.number_of_hours * valorhora
                elif line.work_entry_type_id.mixtime == True:
                    valorhora = (record.contract_id.wage/30/8) * record.payrollbase_id.mixtime_conf
                    record.computo_extrahours += line.number_of_hours * valorhora
                elif line.work_entry_type_id.nighttime == True:
                    valorhora = (record.contract_id.wage/30/8) * record.payrollbase_id.nighttime_conf
                    record.computo_extrahours += line.number_of_hours * valorhora
            return record.computo_extrahours

    # Bien Funcionando
    def _get_computo_incapacidad(self):
        for record in self:
            for line in record.worked_days_line_ids:
                if line.work_entry_type_id.honduras_law_bond == True:
                    if line.number_of_days <= record.payrollbase_id.sick_days :
                        record.computo_incapacidad = ((record.payrollbase_id.ceiling_salary_eym/30) * line.number_of_days)
                        # Calcular Incapacidad Menor a tres dias
                    elif line.number_of_days > record.payrollbase_id.sick_days:
                        diasrestante = (line.number_of_days - record.payrollbase_id.sick_days)
                        ptresd = ((record.payrollbase_id.ceiling_salary_eym/30) * record.payrollbase_id.sick_days)
                        pmasd = (((record.payrollbase_id.ceiling_salary_eym/30) * record.payrollbase_id.porc_inc) * diasrestante)
                        record.computo_incapacidad = (ptresd + pmasd)
                        # Calcular Incapacidad Mayor a tres dias
            return record.computo_incapacidad


    # Bien Funcionando
    def _get_computo_incabono(self):
        for record in self:
            for line in record.worked_days_line_ids:
                if line.work_entry_type_id.honduras_law_bond == True:
                    if line.number_of_days > 1:
                        valordia = (record.contract_id.wage / 30)
                        montodias = line.number_of_days * valordia
                        bono = (montodias - record.computo_incapacidad)
                        if bono > 1:
                            record.computo_incabono = bono
            return record.computo_incabono

    # Bien Funcionando
    def _get_computo_ausencias(self):
        for record in self:
            for line in record.worked_days_line_ids:
                if line.work_entry_type_id.honduras_disc == True:
                    if line.number_of_hours > 1:
                        valorhora = ((record.contract_id.wage/30)/8)
                        record.computo_ausencias += line.number_of_hours * valorhora
                    # elif line.number_of_days > 2:
                    #     valordia = (record.contract_id.wage / 30)
                    #     record.computo_ausencias = line.number_of_days * valordia
            return record.computo_ausencias


    # result = payslip.computo_salario
    def _get_computo_salario(self):
        for record in self:
            paid_amount = record.contract_id.wage
            ausencia = (record.computo_ausencias - (record.computo_feriados/2))
            frequency = record.contract_id.frequency
            salario = record.computo_salario
            contract = self.env['hr.contract'].search([
                ('id', '=', record.contract_id.id),])
            if contract.date_start >= record.date_from:
                dias = (int((record.date_to - contract.date_start).days)) + 1
                record.computo_salario = (((paid_amount/30) * dias)  - ausencia)
            elif frequency == '01':
                record.computo_salario = ((paid_amount/30) - ausencia) # Diario
            elif frequency == '02':
                record.computo_salario = ((paid_amount/4) - ausencia)  # Semanal
            elif frequency == '03':
                record.computo_salario = ((paid_amount/2) - ausencia)  # Quincenal
            else:
                record.computo_salario = ((paid_amount) - ausencia) # Mesual
        return

        # result = payslip.computo_bruto
    def _get_computo_bruto(self):
        for record in self:
            paid_amount = record.contract_id.wage
            frequency = record.contract_id.frequency
            if frequency == '01': record.computo_bruto = paid_amount / 30 # Diario
            elif frequency == '02': record.computo_bruto = paid_amount / 4 # Semanal
            elif frequency == '03': record.computo_bruto = paid_amount / 2 # Quincenal
            else: record.computo_bruto = paid_amount
        return

    # Bien Funcionando
    def _get_computo_ajuste(self):
        for record in self:
            paid_amount = record.contract_id.wage
            semanal = record.contract_id.wage / 4
            quincenal = record.contract_id.wage / 2
            asignaciones = (record.computo_assignments + record.computo_assignments)
            frequency = record.contract_id.frequency
            if (paid_amount + asignaciones) < record.payrollbase_id.min_salary:
                if frequency == '02':
                    record.computo_ajuste = (record.payrollbase_id.min_salary - (paid_amount + asignaciones)) / 4  # Semanal
                elif frequency == '03':
                    record.computo_ajuste = (record.payrollbase_id.min_salary - (paid_amount + asignaciones)) / 2  # Quincenal
                else:
                    record.computo_ajuste = (record.payrollbase_id.min_salary - (paid_amount + asignaciones))
        return record.computo_ajuste


    #result = payslip.computo_rap
    def _get_computo_rap(self):
        for record in self:
            salario = record.contract_id.wage + record.computo_commission + record.computo_assignments
            if  salario <= record.payrollbase_id.ceiling_salary_conf:
                record.computo_rap = 0
            else:
                total = (record.computo_salario +
                         record.computo_commission +
                         record.computo_assignments +
                         record.computo_holidays +
                         record.computo_incapacidad +
                         record.computo_incabono +
                         record.computo_feriados +
                         record.computo_ajuste
                         )
                if record.contract_id.frequency == '02':
                    conf_rap = record.payrollbase_id.ceiling_salary_conf / 4
                    record.computo_rap = ((total - conf_rap) * record.payrollbase_id.porc_rap)
                elif record.contract_id.frequency == '03':
                    conf_rap = record.payrollbase_id.ceiling_salary_conf / 2
                    record.computo_rap = ((total - conf_rap) * record.payrollbase_id.porc_rap)
                else:
                    conf_rap = record.payrollbase_id.ceiling_salary_conf
                    record.computo_rap = ((total - conf_rap) * record.payrollbase_id.porc_rap)



    #result = payslip.computo_ivm
    def _get_computo_ivm(self):
        for record in self:
            ivm = (record.payrollbase_id.ceiling_salary_ivm * record.payrollbase_id.porc_ivm)
            if record.contract_id.frequency == '02':
                record.computo_ivm = ivm / 4
            elif record.contract_id.frequency == '03':
                record.computo_ivm = ivm / 2
            else:
                record.computo_ivm =ivm


    # result = payslip.computo_eym
    def _get_computo_eym(self):
        for record in self:
            eym = (record.payrollbase_id.ceiling_salary_eym * record.payrollbase_id.porc_eym)
            if record.contract_id.frequency == '02':
                record.computo_eym = eym / 4
            elif record.contract_id.frequency == '03':
                record.computo_eym = eym / 2
            else:
                record.computo_eym = eym

    # result = payslip.computo_isr
    def _get_computo_isr(self):
        for record in self:
            paid_amount = (record.contract_id.wage + record.computo_commission) #record.contract_id.averagecommission
            ivm = ((record.payrollbase_id.ceiling_salary_ivm * record.payrollbase_id.porc_ivm) * 12)
            rap = ((((paid_amount) * 12) - (record.payrollbase_id.ceiling_salary_eym * 12)) * record.payrollbase_id.porc_rap)
            gm = record.contract_id.formmedexpenses
            dm= record.payrollbase_id.mdex_exp4
            if record.contract_id.age >= record.payrollbase_id.age_exp3:
                dm = record.payrollbase_id.mdex_exp4
            else:
                dm = 0
            ded = (ivm + rap + gm + dm + record.contract_id.afp)
            bruto = (((paid_amount ) * 12) + record.computo_assignments) # Vacaciones NO record.computo_holidays
            monto = (bruto - ded)
            neto1 = (monto - record.payrollbase_id.difference1)
            neto2 = (neto1 - record.payrollbase_id.difference2)
            neto3 = (neto2 - record.payrollbase_id.difference3)
            dd2 = (record.payrollbase_id.basemax3 - record.payrollbase_id.basemin2)
            if monto < record.payrollbase_id.basemax1:
                record.computo_isr = 0.0
            elif (monto > record.payrollbase_id.basemax1) and (neto1 < record.payrollbase_id.difference2):
                isr = ((neto1 * record.payrollbase_id.porc_islr2) / record.payrollbase_id.months)
                if record.contract_id.frequency == '02':
                    record.computo_isr = isr / 4
                elif record.contract_id.frequency == '03':
                    record.computo_isr = isr / 2
                else:
                    record.computo_isr = isr
            elif (monto > record.payrollbase_id.basemax2) and (neto2 < record.payrollbase_id.difference3):
                grava1 = (record.payrollbase_id.difference2 * record.payrollbase_id.porc_islr2)
                grava2 = (neto2 * record.payrollbase_id.porc_islr3)
                isr = ((grava1 + grava2) / record.payrollbase_id.months)
                if record.contract_id.frequency == '02':
                    record.computo_isr = isr / 4
                elif record.contract_id.frequency == '03':
                    record.computo_isr = isr / 2
                else:
                    record.computo_isr = isr
            elif (monto > record.payrollbase_id.basemax3) and (neto3 < record.payrollbase_id.difference3):
                gravab1 = (record.payrollbase_id.difference2 * record.payrollbase_id.porc_islr2)
                gravab2 = (record.payrollbase_id.difference3 * record.payrollbase_id.porc_islr3)
                gravab3 = (neto3 * record.payrollbase_id.porc_islr4)
                isr = ((gravab1 + gravab2 + gravab3) / record.payrollbase_id.months)
                if record.contract_id.frequency == '02':
                    record.computo_isr = isr / 4
                elif record.contract_id.frequency == '03':
                    record.computo_isr = isr / 2
                else:
                    record.computo_isr = isr
            elif (monto > record.payrollbase_id.basemin4) and (neto3 > record.payrollbase_id.difference3):
                gravabl1 = (record.payrollbase_id.difference2 * record.payrollbase_id.porc_islr2)
                gravabl2 = (record.payrollbase_id.difference3 * record.payrollbase_id.porc_islr3)
                gravabl3 = (neto3 * record.payrollbase_id.porc_islr4)
                isr = ((gravabl1 + gravabl2 + gravabl3) / record.payrollbase_id.months)
                if record.contract_id.frequency == '02':
                    record.computo_isr = isr / 4
                elif record.contract_id.frequency == '03':
                    record.computo_isr = isr / 2
                else:
                    record.computo_isr = isr

