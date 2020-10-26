# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class HrWorkEntryType(models.Model):
    _inherit = 'hr.work.entry.type'

    honduras_law_bond = fields.Boolean(
        string="Bono de Incapacidad", default=False,
        help="Activar el Bono de Ausencia por Incapacidad. Ley de Honduras")
    honduras_disc = fields.Boolean(
        string="Descontar la Ausencia", default=False,
        help="Activar Descuento de la ausencia al salario")
    daytime = fields.Boolean(
        string="Horas Extras Diurnas", default=False,
        help="Activar Calcula Horas Extras Diurnas")
    mixtime = fields.Boolean(
        string="Horas Extras Mixtas", default=False,
        help="Activar Calcula Horas Extras Mixtas")
    nighttime = fields.Boolean(
        string="Horas Extras Nocturnas", default=False,
        help="Activar Calcula Horas Extras Nocturnas")
    natholidays = fields.Boolean(
        string="Dias Feriados Laborados", default=False,
        help="Activar Dias Feriados Laborados")
    holidays = fields.Boolean(
        string="Vacaciones", default=False,
        help="Activar Vacaciones")


#

#
# class HrAttendance(models.Model):
#     _inherit = "hr.attendance"
#     _description = 'Attendance'
#
#     # def _default_employee(self):
#     #     return self.env.user.employee_id
#     #
#     # employee_id = fields.Many2one('hr.employee', string="Employee", default=_default_employee, required=True, ondelete='cascade', index=True)
#     # department_id = fields.Many2one('hr.department', string="Department", related="employee_id.department_id",
#     #     readonly=True)
#     # check_in = fields.Datetime(string="Check In", default=fields.Datetime.now, required=True)
#     # check_out = fields.Datetime(string="Check Out")
#     # worked_hours = fields.Float(string='Worked Hours', compute='_compute_worked_hours', store=True, readonly=True)
#
#     # payslip_id = fields.Many2one(
#     #     'hr.payslip', string="Payslip", required=False )
#     # final_hours = fields.Float(string="Final Hours",  required=False,)
#     # observation = fields.Text(string="Observation",
#     #                           required=False, default="Daily attendance")
#     # absences = fields.Selection(string="Ausencias", selection=[
#     #     ('01', 'Ausencia no Remunerada'),
#     #     ('02', 'Ausencia por Enfermedad'),
#     #     ('03', 'Ausencia por Enfermedad Largo Plazo') ], required=False, )
#     # extra_hours = fields.Selection(string="Extra hours", selection=[
#     #     ('daytime', 'Diurna'),
#     #     ('nightly', 'Nocturna'), ], required=False, )
#     #
#
# class HrPayslipWorkedDays(models.Model):
#     _inherit = 'hr.payslip.worked_days'
#
#     # name = fields.Char(string='Description', required=True)
#     # payslip_id = fields.Many2one('hr.payslip', string='Pay Slip', required=True, ondelete='cascade', index=True, help="Payslip")
#     # sequence = fields.Integer(required=True, index=True, default=10, help="Sequence")
#     # code = fields.Char(required=True, help="The code that can be used in the salary rules")
#     # number_of_days = fields.Float(string='Number of Days', help="Number of days worked")
#     # number_of_hours = fields.Float(string='Number of Hours', help="Number of hours worked")
#     # contract_id = fields.Many2one('hr.contract', string='Contract', required=True,
#     #                               help="The contract for which applied this input")
#     final_hours = fields.Float(string="Final Hours", required=False )
#
#


