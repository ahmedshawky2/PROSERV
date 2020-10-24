# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import datetime
from datetime import date
import logging
_logger = logging.getLogger(__name__)



class herPayslipInputsExtend(models.Model):
    _inherit = 'hr.payslip'

    @api.model
    def create(self, values):
        record = super(herPayslipInputsExtend, self).create(values)

        _logger.debug('res record ! "%s"' % (str(record)))

        payslip = self.env['hr.payslip'].browse(int(record))

        self.env['hr.payslip.input'].create({
            'name': 'DUMMY DED',
            'payslip_id': payslip[0]['id'],
            'code': 'DED',
            'amount': 0.0,
            'contract_id': int(payslip[0]['contract_id']),
        })

        self.env.cr.commit()

        self.env['hr.payslip.input'].create({
            'name': 'DUMMY ALW',
            'payslip_id': payslip[0]['id'],
            'code': 'ALW',
            'amount': 0.0,
            'contract_id': int(payslip[0]['contract_id']),
        })

        self.env.cr.commit()

        self.compute_sheet()

        return record

    @api.one
    def write(self, vals):
        res = super(herPayslipInputsExtend, self).write(vals)

        _logger.debug('vals maged ! "%s"' % (str(vals)))
        _logger.debug('self.id maged ! "%s"' % (str(self.id)))
        _logger.debug('res maged ! "%s"' % (str(res)))

        payslip = self.env['hr.payslip'].browse(self.id)

        _logger.debug('vals maged ! "%s"' % (str(payslip)))

        payslipDateFrom = payslip[0]['date_from']
        _logger.debug('payslipDateFrom maged ! "%s"' % (str(payslipDateFrom)))
        payslipDateTo =  payslip[0]['date_to']
        _logger.debug('payslipDateTo maged ! "%s"' % (str(payslipDateTo)))

        _logger.debug('contract_id maged ! "%s"' % (str(payslip[0]['contract_id'])))


        salary = self.env['hr.contract'].browse(int(payslip[0]['contract_id']))
        wage = salary[0]['wage']
        _logger.debug('wage maged ! "%s"' % (str(wage)))


        paySlipInputs = self.env['hr.employee.salary.extend'].search([('employee_id', '=', int(payslip[0]['employee_id'])),
                                                                      ('is_executed','=',False),
                                                                      ('status_flag','=',True),
                                                                      ('action_date', '<=', payslipDateTo)])

        _logger.debug('paySlipInputs maged ! "%s"' % (str(paySlipInputs)))

        for paySlipInput in paySlipInputs:

            code = 'ALW'
            amount = 0.0

            if paySlipInput[0]['amount'] < 0 or paySlipInput[0]['number_of_days']:
                code = 'DED'

            if paySlipInput[0]['number_of_days'] < 0:
                code = 'DED'

            if paySlipInput[0]['number_of_days'] > 0:
                code = 'ALW'

            if paySlipInput[0]['amount'] < 0 or paySlipInput[0]['amount'] > 0:
                amount = paySlipInput[0]['amount']

            if paySlipInput[0]['number_of_days'] > 0 or paySlipInput[0]['number_of_days'] < 0:
                amount = (wage / 30) * paySlipInput[0]['number_of_days']

            _logger.debug('code maged ! "%s"' % (str(code)))
            _logger.debug('amount maged ! "%s"' % (str(amount)))
            _logger.debug('payslip_id maged ! "%s"' % (str(payslip[0]['id'])))
            _logger.debug('contract_id maged ! "%s"' % (str(int(payslip[0]['contract_id']))))

            paySlipInputs[0]['is_executed'] = True

            self.env['hr.payslip.input'].create({
                'name': paySlipInput[0]['action_desc'],
                'payslip_id': payslip[0]['id'],
                'code': code,
                'amount': amount,
                'contract_id': int(payslip[0]['contract_id']),
            })

            self.env.cr.commit()

            paySlipInput[0]['is_executed'] = True

        return res