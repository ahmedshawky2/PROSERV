# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import datetime
from datetime import date
import logging
_logger = logging.getLogger(__name__)



# class hrEmployeeSalaryActions(models.Model):
#
#      _name = "hr.employee.salary.ext"
#
#      employee_id = fields.Integer(string="Employee Id", store=True, index=True,
#                                   help="Employee Id",copy=True,track_visibility='always')
#
#      action_desc = fields.Text(string="Description", store=True, index=True,
#                                   help="Description",track_visibility='always', required=True)
#
#      action_date = fields.Date(string="Action Date", help="Action Date", store=True, index=True,
#                                copy=True, required=True,track_visibility='always')
#
#      status_flag = fields.Boolean(string="Action Status", help="Action Status",track_visibility='always'
#                                   ,index=True,store=True, required=True)
#
#      amount = fields.Float('Amount', digits=(16, 2), track_visibility="always",
#                             help="Amount",index=True,store=True)
#
#      number_of_days = fields.Float(string='No. of days', help="No. of days", track_visibility="always",
#                                                    index=True,store=True)


class hrEmployeeSalaryActions2(models.Model):

    _name = "hr.employee.salary.extend"

    def getEmployeeId(self):
        return self.env.context.get('employeeId')

    employee_id = fields.Integer(string="Employee Id", store=True, index=True,
                                 help="Employee Id",copy=True,track_visibility='always')

    action_desc = fields.Text(string="Description", store=True, index=True,
                                 help="Description",track_visibility='always', required=True)

    action_date = fields.Date(string="Action Date", help="Action Date", store=True, index=True,
                              copy=True, required=True,track_visibility='always')

    status_flag = fields.Boolean(string="Action Status", help="Action Status",track_visibility='always'
                                 ,index=True,store=True, required=True)

    amount = fields.Float('Amount', digits=(16, 2), track_visibility="always",
                           help="Amount",index=True,store=True)

    number_of_days = fields.Float(string='No. of days', help="No. of days", track_visibility="always",
                                                  index=True,store=True)

    contract_id = fields.Many2one('hr.contract', string='Contract',index=True,store=True,
                                  help="The contract for which applied this input",
                                  domain=[('state','=','open')])

    is_executed = fields.Boolean(string="Is Executed", help="Is Executed", track_visibility='always'
                                 , index=True, store=True, default=False)

    # @api.model
    # def create(self, values):
    #
    #     record = super(hrEmployeeSalaryActions2, self).create(values)
    #
    #     _logger.debug('record maged ! "%s"' % (str(record)))
    #
    #     contract = self.env['hr.contract'].search([('employee_id', '=', values.get('employee_id')),
    #                                                ('active', '=', True),
    #                                                ('state', 'in', ('open', 'pending'))])
    #
    #     values.update({'contract_id': contract[0]['id']})
    #
    #     return record


class hrEmployeeSalaryFixedRules(models.Model):

    _name = "hr.salary.fixed.rules"

    employee_id = fields.Integer(string="Employee Id", store=True, index=True,
                                 help="Employee Id",copy=True,track_visibility='always')

    reason = fields.Text(string="Reason", store=True, index=True,
                                 help="Reason",track_visibility='always')

    rule_start_date = fields.Date(string="Rule Start Date", help="Rule Start Date", store=True, index=True,
                              copy=True, track_visibility='always')

    rule_end_date = fields.Date(string="Rule End Date", help="Rule End Date", store=True, index=True,
                                  copy=True, track_visibility='always')

    status_rule_flag = fields.Boolean(string="Rule Status", help="Rule Status",track_visibility='always'
                                 ,index=True,store=True, required=True)

    rule = fields.Many2one('hr.salary.rule', string='Rule', index=True, track_visibility='always',required=True,store=True,ondelete='cascade')

    salary_structure = fields.Many2one('hr.payroll.structure', string='Employee Salary Structure', index=True,
                                   track_visibility='always',store=True,help='Employee Salary Structure',ondelete='cascade')

    @api.model
    def create(self, values):

        contract = self.env['hr.contract'].search([('employee_id', '=', values.get('employee_id')),
                                                      ('active','=',True),
                                                      ('state','in',('open','pending'))])

        salaryStructure = contract[0]['struct_id']

        _logger.debug('salaryStructure maged ! "%s"' % (str(int(salaryStructure))))
        _logger.debug('int(values.get(rule)) maged ! "%s"' % (str(int(values.get('rule')))))

        self.env.cr.execute('insert into hr_structure_salary_rule_rel (struct_id,rule_id) '
                            'values(%d,%d)' % (int(salaryStructure),int(values.get('rule'))))
        self.env.cr.commit()

        values.update({'salary_structure': int(salaryStructure)})

        record = super(hrEmployeeSalaryFixedRules, self).create(values)

        return record


class hrEmployeeSalaryExtend(models.Model):

    _inherit = "hr.employee"

    employee_salary_actions = fields.One2many('hr.employee.salary.extend', 'employee_id',
                                              string='Employee Salary Actions',
                                              help="Employee Salary Actions",index=True,store=True,track_visibility="always")

    employee_fixed_salary_rules = fields.One2many('hr.salary.fixed.rules', 'employee_id',
                                              string='Employee Fixed Salary Rules',
                                              help="Employee Fixed Salary Rules", index=True, store=True,track_visibility="always")

    #rule_ids = fields.Many2many('hr.salary.rule', 'hr_structure_salary_rule_rel', 'struct_id', 'rule_id',
                                #string='Salary Rules')




