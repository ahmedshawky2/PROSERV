# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import datetime
from datetime import date
import logging
_logger = logging.getLogger(__name__)


class payslipbatchrun(models.Model):
    _inherit = 'hr.payslip.run'

    payslips_basics = fields.Monetary('Payslips Basics', digits=(16, 2), track_visibility="always",help="Payslips Basics.",index=True,store=True)
    payslips_insurance = fields.Monetary('Payslips Social Insurances', digits=(16, 2), track_visibility="always",help="Payslips Social Insurances.",index=True,store=True)
    payslips_gross = fields.Monetary('Payslips Gross', digits=(16, 2), track_visibility="always",help="Payslips Gross.",index=True,store=True)
    payslips_taxes = fields.Monetary('Payslips Taxes', digits=(16, 2), track_visibility="always",help="Payslips Taxes.",index=True,store=True)
    payslips_net_salaries = fields.Monetary('Payslips Net Salaries', digits=(16, 2), track_visibility="always",help="Payslips Net Salaries.",index=True,store=True)


    def calculate_batch_payslips(self):

        payslip_run_id = self.id

        gross = 0.0
        basic = 0.0
        tax = 0.0
        net_salary = 0.0
        insurance = 0.0

        payslips = self.env['hr.payslip'].search([('payslip_run_id', '=', int(payslip_run_id)),('state','=','verify')])

        for payslip in payslips:

            payslip_lines = self.env['hr.payslip.line'].search([('slip_id', '=', int(payslip.id))])

            for pl in payslip_lines:

                if pl.code == "BASIC_REVERSE" or pl.code == "BASIC":
                    basic = basic + pl.amount
                elif pl.code == "GROSS_REVERSE" or pl.code == "GROSS":
                    gross = gross + pl.amount
                elif pl.code == "NET_REVERSE" or pl.code == "NET":
                    net_salary = net_salary + pl.amount
                elif pl.code == "NSAT_REVERSE" or pl.code == "NSAT":
                    tax = tax + pl.amount
                elif pl.code == "ICSR_REVERSE" or pl.code == "SIR_REVERSE" or pl.code == "ICSR" or pl.code == "SIR":
                    insurance = insurance + pl.amount

            payslip.state = "done"

        self.payslips_net_salaries = net_salary
        self.payslips_insurance = insurance
        self.payslips_gross = gross
        self.payslips_taxes = tax
        self.payslips_basics = basic