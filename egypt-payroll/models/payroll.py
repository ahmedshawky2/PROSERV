# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import datetime
from datetime import date
import logging
_logger = logging.getLogger(__name__)


class taxation(models.Model):
    _inherit = 'hr.payslip'

    #@api.multi
    def get_salary_m_taxes(self, emp_id, netgross):

        emp_rec = self.env['hr.contract'].search([('employee_id', '=', int(emp_id))])
        dt_start = emp_rec.date_start
        salary = netgross
        _logger.info('dt_start maged ! "%s"' % (str(dt_start)))
        _logger.info('salary maged ! "%s"' % (str(salary)))
        result = 0.0

        today = date.today()
        _logger.info('today maged ! "%s"' % (str(today)))

        start_month =datetime.strptime(str(dt_start),"%Y-%m-%d").month
        _logger.info('start_month maged ! "%s"' % (str(start_month)))
        start_year =datetime.strptime(str(dt_start),"%Y-%m-%d").year
        _logger.info('start_year maged ! "%s"' % (str(start_year)))

        current_month = today.month
        _logger.info('current_month maged ! "%s"' % (str(current_month)))
        current_year = today.year
        _logger.info('current_year maged ! "%s"' % (str(current_year)))

        #personal_exempt = (1 / 12) * 9000
        #salary = salary - personal_exempt
        annual_netgross_salary = 12*salary


        if annual_netgross_salary < 0:
            return result
        elif 0 <= annual_netgross_salary <= 600000:
            result = taxation.SalaryTaxTo600Layer(self,salary)
            return result
        elif 600001<= annual_netgross_salary <= 700000:
            result = taxation.SalaryTaxFrom601To700Layer(self,salary)
            return result
        elif 700001<= annual_netgross_salary <= 800000:
            result = taxation.SalaryTaxFrom701To800Layer(self,salary)
            return result
        elif 800001<= annual_netgross_salary <= 900000:
            result = taxation.SalaryTaxFrom801To900Layer(self,salary)
            return result
        elif 900001<= annual_netgross_salary <= 1000000:
            result = taxation.SalaryTaxFrom901To1000Layer(self,salary)
            return result
        elif annual_netgross_salary >= 1000001:
            result = taxation.SalaryTaxFrom1001Layer(self,salary)
            return result


    def get_salary_m_wostart_date_taxes(self, emp_id, netgross):

        emp_rec = self.env['hr.contract'].search([('employee_id', '=', int(emp_id))])
        dt_start = emp_rec.date_start
        salary = netgross
        _logger.info('dt_start maged ! "%s"' % (str(dt_start)))
        _logger.info('salary maged ! "%s"' % (str(salary)))
        result = 0.0

        today = date.today()
        _logger.info('today maged ! "%s"' % (str(today)))

        start_month = datetime.strptime(str(dt_start), "%Y-%m-%d").month
        _logger.info('start_month maged ! "%s"' % (str(start_month)))
        start_year = datetime.strptime(str(dt_start), "%Y-%m-%d").year
        _logger.info('start_year maged ! "%s"' % (str(start_year)))

        current_month = today.month
        _logger.info('current_month maged ! "%s"' % (str(current_month)))
        current_year = today.year
        _logger.info('current_year maged ! "%s"' % (str(current_year)))

        exempt_month_slary = (8000 / 12)
        _logger.info('exempt_month_slary maged ! "%s"' % (str(exempt_month_slary)))

        personal_exempt = (1 / 12) * 7000
        _logger.info('personal_exempt maged ! "%s"' % (str(personal_exempt)))

        after_personal_exempt = netgross - personal_exempt

        _logger.info('after_personal_exempt maged ! "%s"' % (str(after_personal_exempt)))

        tax10 = 0.0
        tax15 = 0.0
        tax20 = 0.0
        tax22_5 = 0.0

        net_salary_after_tax = 0.0

        if after_personal_exempt < 0:
            # net_salary_after_tax = salary
            # result = net_salary_after_tax
            result = tax10 + tax15 + tax20 + tax22_5
            _logger.info('after_personal_exempt < 0 ==> result maged ! "%s"' % (str(result)))
            return result

        ##if 0 < after_personal_exempt <= (8000/12):
        if 0 < after_personal_exempt <= exempt_month_slary:
            # net_salary_after_tax = salary
            # result = net_salary_after_tax
            result = tax10 + tax15 + tax20 + tax22_5
            _logger.info('0 < after_personal_exempt <= exempt_month_slary ==> result maged ! "%s"' % (str(result)))
            return result

        else:

            ##after_personal_exempt = after_personal_exempt - (8000/12)
            after_personal_exempt = after_personal_exempt - exempt_month_slary
            _logger.info('after_personal_exempt maged ! "%s"' % (str(after_personal_exempt)))

            if after_personal_exempt < exempt_month_slary:
                _logger.info('after_personal_exempt < exempt_month_slary ==> maged !')
                tax10 = after_personal_exempt * 0.1
                _logger.info(
                    'after_personal_exempt < exempt_month_slary ==> maged ! "%s"' % (str(tax10)))
                result = tax10 + tax15 + tax20 + tax22_5
                _logger.info(
                    'after_personal_exempt < exempt_month_slary ==> maged ! "%s"' % (str(result)))
                return result

            ##if (8000/12) < after_personal_exempt <= (22000/12):
            if exempt_month_slary < after_personal_exempt <= (22000 / 12):
                tax10 = after_personal_exempt * 0.1
                _logger.info(
                    'exempt_month_slary < after_personal_exempt <= (22000/12) ==> tax10 maged ! "%s"' % (str(tax10)))
                # net_salary_after_tax = salary - tax10
                # result = net_salary_after_tax
                result = tax10 + tax15 + tax20 + tax22_5
                _logger.info(
                    'exempt_month_slary < after_personal_exempt <= (22000/12) ==> result maged ! "%s"' % (str(result)))
                return result

            if (22000 / 12) < after_personal_exempt <= (37000 / 12):
                tax10 = (2200 / 12)
                _logger.info('(22000/12) < after_personal_exempt <= (37000/12) ==> tax10 maged ! "%s"' % (str(tax10)))
                after_tax10_salary = after_personal_exempt - (22000 / 12)
                _logger.info('(22000/12) < after_personal_exempt <= (37000/12) ==> after_tax10_salary maged ! "%s"' % (
                    str(after_tax10_salary)))
                tax15 = after_tax10_salary * 0.15
                _logger.info('(22000/12) < after_personal_exempt <= (37000/12) ==> tax15 maged ! "%s"' % (str(tax15)))
                # net_salary_after_tax = salary - tax10 - tax15
                # result = net_salary_after_tax
                result = tax10 + tax15 + tax20 + tax22_5
                _logger.info(
                    '(22000/12) < after_personal_exempt <= (37000/12) ==> result maged ! "%s"' % (str(result)))
                return result

            if (37000 / 12) < after_personal_exempt <= (155000 / 12):
                tax10 = (2200 / 12)
                _logger.info('(37000/12) < after_personal_exempt <= (155000/12) ==> tax10 maged ! "%s"' % (str(tax10)))
                after_tax10_salary = after_personal_exempt - (22000 / 12)
                _logger.info(
                    '(37000/12) < after_personal_exempt <= (155000/12) ==> after_tax10_salary maged ! "%s"' % (
                        str(after_tax10_salary)))
                tax15 = (2250 / 12)
                _logger.info('(37000/12) < after_personal_exempt <= (155000/12) ==> tax15 maged ! "%s"' % (str(tax15)))
                after_tax15_salary = after_tax10_salary - (15000 / 12)
                _logger.info(
                    '(37000/12) < after_personal_exempt <= (155000/12) ==> after_tax15_salary maged ! "%s"' % (
                        str(after_tax15_salary)))
                tax20 = after_tax15_salary * 0.2
                _logger.info('(37000/12) < after_personal_exempt <= (155000/12) ==> tax20 maged ! "%s"' % (str(tax20)))
                # net_salary_after_tax = salary - tax10 - tax15 - tax20
                # result = net_salary_after_tax
                result = tax10 + tax15 + tax20 + tax22_5
                _logger.info(
                    '(37000/12) < after_personal_exempt <= (155000/12) ==> result maged ! "%s"' % (str(result)))
                return result

            if (155000 / 12) < after_personal_exempt:
                tax10 = (2200 / 12)
                _logger.info('(155000/12) < after_personal_exempt ==> tax10 maged ! "%s"' % (str(tax10)))
                after_tax10_salary = after_personal_exempt - (22000 / 12)
                _logger.info('(155000/12) < after_personal_exempt ==> after_tax10_salary maged ! "%s"' % (
                    str(after_tax10_salary)))
                tax15 = (2250 / 12)
                _logger.info('(155000/12) < after_personal_exempt ==> tax15 maged ! "%s"' % (str(tax15)))
                after_tax15_salary = after_tax10_salary - (15000 / 12)
                _logger.info('(155000/12) < after_personal_exempt ==> after_tax15_salary maged ! "%s"' % (
                    str(after_tax15_salary)))
                tax20 = (31000 / 12)
                _logger.info('(155000/12) < after_personal_exempt ==> tax20 maged ! "%s"' % (str(tax20)))
                after_tax20_salary = after_tax15_salary - (155000 / 12)
                _logger.info('(155000/12) < after_personal_exempt ==> after_tax20_salary maged ! "%s"' % (
                    str(after_tax20_salary)))
                tax22_5 = after_tax20_salary * 0.225
                _logger.info('(155000/12) < after_personal_exempt ==> tax22_5 maged ! "%s"' % (str(tax22_5)))
                # net_salary_after_tax = salary - tax10 - tax15 - tax20 - tax22_5
                # result = net_salary_after_tax
                result = tax10 + tax15 + tax20 + tax22_5
                _logger.info('(155000/12) < after_personal_exempt ==> result maged ! "%s"' % (str(result)))
                return result

    def sum_inputs_codes(self, payslip_id, code, contract_id):

        _logger.info('self.id maged ! "%s"' % (str(payslip_id)))
        _logger.info('code maged ! "%s"' % (str(code)))
        _logger.info('contract_id maged ! "%s"' % (str(contract_id)))

        inputs = self.env['hr.payslip.input'].search([('payslip_id','=',payslip_id)])
        _logger.info('inputs maged ! "%s"' % (str(inputs)))

        result = 0.0

        for input in inputs:
            if input[0]['code'] == code and int(input[0]['contract_id'])  == contract_id:
                result = result + input[0]['amount']

        _logger.info('result maged ! "%s"' % (str(result)))

        return result


    def SalaryTaxTo600Layer(self,salary):

        tax0 = 0.0
        tax2_5 = 0.0
        tax10 = 0.0
        tax15 = 0.0
        tax20 = 0.0
        tax22_5 = 0.0
        tax25 = 0.0
        result = 0.0
        personal_exempt = (1 / 12) * 9000
        salary = salary - personal_exempt
        salary_after_deduct_tax = salary

        if salary <= (15000 / 12):
            _logger.info('salary <= (15000 / 12) ==> maged !')
            tax0 = salary * 0
            _logger.info('tax0 = salary * 0 ==> maged ! "%s"' % (str(tax0)))
            result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
            _logger.info('result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (str(result)))
            return result

        else:
            salary_after_deduct_tax = salary_after_deduct_tax - (15000 / 12)
            _logger.info('(15000 / 12) ==> maged ! "%s"' % (str((15000 / 12))))
            _logger.info('salary_after_deduct_tax = salary_after_deduct_tax - (15000 / 12) ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

            if 0 <= salary_after_deduct_tax <= (15000 / 12):
                _logger.info('(0 / 12) <= salary_after_deduct_tax <= (15000 / 12) ==> maged 1 !')
                tax2_5 = salary_after_deduct_tax * 0.025
                _logger.info('tax2_5 = salary_after_deduct_tax * 0.025 ==> maged ! "%s"' % (str(tax2_5)))
                result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                _logger.info('result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (str(result)))
                return result
            else:
                tax2_5 = (15000/12) * 0.025
                _logger.info('(15000 / 12) ==> maged ! "%s"' % (str((15000 / 12))))
                salary_after_deduct_tax = salary_after_deduct_tax - (15000 / 12)
                _logger.info('tax2_5 ==> maged ! "%s"' % (str(tax2_5)))
                _logger.info('salary_after_deduct_tax ==> maged ! "%s"' % (str(salary_after_deduct_tax)))


            if 0 <= salary_after_deduct_tax <= (15000 / 12):
                _logger.info('0 <= salary_after_deduct_tax <= (15000 / 12) ==> maged !')
                tax10= salary_after_deduct_tax * 0.1
                _logger.info('tax10 = salary_after_deduct_tax * 0.1 ==> maged ! "%s"' % (str(tax10)))
                result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                _logger.info('result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (str(result)))
                return result
            else:
                tax10 = (15000 / 12) * 0.1
                _logger.info('(15000 / 12) ==> maged ! "%s"' % (str((15000 / 12))))
                salary_after_deduct_tax = salary_after_deduct_tax - (15000 / 12)
                _logger.info('tax10 ==> maged ! "%s"' % (str(tax10)))
                _logger.info('salary_after_deduct_tax ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

                if 0 <= salary_after_deduct_tax <= (15000 / 12):
                    _logger.info('0 <= salary_after_deduct_tax <= (15000 / 12) ==> maged !')
                    tax15 = salary_after_deduct_tax * 0.15
                    _logger.info('tax15 = salary_after_deduct_tax * 0.15 ==> maged ! "%s"' % (str(tax15)))
                    result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                    _logger.info('result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (
                        str(result)))
                    return result
                else:
                    tax15 = (15000 / 12) * 0.15
                    _logger.info('(15000 / 12) ==> maged ! "%s"' % (str((15000 / 12))))
                    salary_after_deduct_tax = salary_after_deduct_tax - (15000 / 12)
                    _logger.info('tax15 ==> maged ! "%s"' % (str(tax15)))
                    _logger.info('salary_after_deduct_tax ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

                    if 0 <= salary_after_deduct_tax <= (140000 / 12):
                        _logger.info('0 <= salary_after_deduct_tax <= (140000 / 12) ==> maged !')
                        tax20 = salary_after_deduct_tax * 0.2
                        _logger.info('tax20 = salary_after_deduct_tax * 0.20 ==> maged ! "%s"' % (str(tax20)))
                        result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                        _logger.info(
                            'result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (
                                str(result)))
                        return result
                    else:
                        tax20 = (140000 / 12) * 0.2
                        _logger.info('(140000 / 12) ==> maged ! "%s"' % (str((140000 / 12))))
                        salary_after_deduct_tax = salary_after_deduct_tax - (140000 / 12)
                        _logger.info('tax20 ==> maged ! "%s"' % (str(tax20)))
                        _logger.info('salary_after_deduct_tax ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

                        if 0 <= salary_after_deduct_tax <= (200000 / 12):
                            _logger.info('0 <= salary_after_deduct_tax <= (200000 / 12) ==> maged !')
                            tax22_5 = salary_after_deduct_tax * 0.225
                            _logger.info('tax22_5 = salary_after_deduct_tax * 0.225 ==> maged ! "%s"' % (str(tax22_5)))
                            result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                            _logger.info(
                                'result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (
                                    str(result)))
                            return result
                        else:
                            tax22_5 = (200000 / 12) * 0.225
                            _logger.info('(200000 / 12) ==> maged ! "%s"' % (str((200000 / 12))))
                            salary_after_deduct_tax = salary_after_deduct_tax - (200000 / 12)
                            _logger.info('tax22_5 ==> maged ! "%s"' % (str(tax22_5)))
                            _logger.info('salary_after_deduct_tax ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

                            if salary_after_deduct_tax >= (200001 / 12):
                                _logger.info('salary_after_deduct_tax >= (200001 / 12) ==> maged !')
                                tax25 = salary_after_deduct_tax * 0.25
                                _logger.info('tax25 = salary_after_deduct_tax * 0.25 ==> maged ! "%s"' % (str(tax25)))
                                result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                                _logger.info(
                                    'result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (
                                        str(result)))
                                return result




    def SalaryTaxFrom601To700Layer(self):

        return True

    def SalaryTaxFrom701To800Layer(self):

        return True

    def SalaryTaxFrom801To900Layer(self):

        return True

    def SalaryTaxFrom901To1000Layer(self):

        return True

    def SalaryTaxFrom1001Layer(self):

        return True