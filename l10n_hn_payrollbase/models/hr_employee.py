# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _


class Employee(models.Model):
    _inherit = 'hr.employee'

    ref_code = fields.Char(string='Código de Referencia', required=False)
    division_id = fields.Many2one('hr_employe.division', string='División')
    grupo = fields.Char(string='Grupo', required=False)
    date_ing = fields.Date(string="Fecha de Ingreso", required=True)
    date_hist = fields.Date(string='Fecha Histórica' )
    antique = fields.Integer(string='Antigüedad', compute='_get_antique_employee', readonly=True)
    age = fields.Integer(string='Edad', compute='_get_birthday_employee', readonly=True)
    driverlic = fields.Char(string='Licencia de Conducir', required=False)
    socialsecurity = fields.Char(string='Seguro Social', required=False)
    phone = fields.Char(string='Teléfono', required=False)
    cellphone = fields.Char(string='Celular', required=False)
    bloodtype = fields.Char(string='Tipo de Sangre', required=False)
    instruction = fields.Char(string='Grado de Instrucción', required=False)
    holidays = fields.Float(string='Dias de Vacaciones', related='contract_id.holidays',)
    certificat = fields.Selection(
        selection=[('Incomplete Elementary', 'Primaria Incompleta'),
                   ('Elementary', 'Primaria'),
                   ('Incomplete High School', 'Secundaria Incompleta'),
                   ('High School', 'Secundaria'),
                   ('Bachelor', 'Licenciatura'),
                   ('Master', 'Maestría'),
                   ('Doctorate', 'Doctorado'),
                   ('Other', 'Otro'),
                   ],
        string=_('Nivel de Certificado'),
    )


    def button_holidays(self):
        # print('vacaciones 1', self.leave_manager_id)
        # print('vacaciones 2', self.show_leaves)
        # print('vacaciones 3', self.allocation_used_count)
        # print('vacaciones 4', self.allocation_count)
        # print('vacaciones 5', self.leave_date_to)
        # print('vacaciones 6', self.is_absent)
        # print('vacaciones 7', self.allocation_used_display)
        # print('vacaciones 8', self.allocation_display)

        if self.allocation_display == '0': self.env['hr.leave.allocation'].create({
            'name': 'Vacaciones',
            'holiday_status_id': 1,
            'allocation_type':'regular',
            'employee_id' : self.id,
            'number_of_days': self.holidays,
            'holiday_type': 'employee',
            'state': 'validate',
            })
        return

    @api.onchange('antique')
    def _onchange_category_ids(self):
        if self.antique == 0:
            categ_id = self.env.ref('l10n_hn_payrollbase.category_nuevo_a')
        elif self.antique == 1:
            categ_id = self.env.ref('l10n_hn_payrollbase.category_antique_b')
        elif self.antique == 2:
            categ_id = self.env.ref('l10n_hn_payrollbase.category_antique_c')
        elif self.antique == 3:
            categ_id = self.env.ref('l10n_hn_payrollbase.category_antique_d')
        elif self.antique >= 3:
            categ_id = self.env.ref('l10n_hn_payrollbase.category_antique_e')
        self.update({'category_ids': [(6, 0, [categ_id.id])]})


    @api.depends("birthday")
    def _get_birthday_employee(self):
        today_date = datetime.date.today()
        for employee in self:
            if employee.birthday:
                birthday = fields.Datetime.to_datetime(employee.birthday).date()
                total_age = str(int((today_date - birthday).days / 365))
                employee.age = total_age
            else:
                employee.age = 0


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




class division(models.Model):
    _name = 'hr_employe.division'
    _description = 'division'

    name = fields.Char(string='Nombre')
    code = fields.Char(string='Código')
    description = fields.Char(string='Descripción')
    

