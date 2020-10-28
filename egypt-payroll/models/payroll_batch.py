# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import datetime
from datetime import date
import logging
_logger = logging.getLogger(__name__)


class payslipbatchrun(models.Model):
    _inherit = 'hr.payslip.run'

    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)
    payslips_basics = fields.Monetary('Payslips Basics', digits=(16, 2), track_visibility="always",help="Payslips Basics.",index=True,store=True)
    payslips_insurance = fields.Monetary('Payslips Social Insurances', digits=(16, 2), track_visibility="always",help="Payslips Social Insurances.",index=True,store=True)
    payslips_gross = fields.Monetary('Payslips Gross', digits=(16, 2), track_visibility="always",help="Payslips Gross.",index=True,store=True)
    payslips_taxes = fields.Monetary('Payslips Taxes', digits=(16, 2), track_visibility="always",help="Payslips Taxes.",index=True,store=True)
    payslips_net_salaries = fields.Monetary('Payslips Net Salaries', digits=(16, 2), track_visibility="always",help="Payslips Net Salaries.",index=True,store=True)

    partner_id = fields.Many2one('res.partner', string='Customer', required=True, index=True, tracking=1)
    journal_id = fields.Many2one('account.journal', string='Journal', required=True, readonly=True)
    invoice_payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', store=True, index=True)
    invoice_date = fields.Date(string='Invoice Date', required=True, index=True,default=fields.Date.context_today)
    account_id = fields.Many2one('account.account', string='Account', store=True, index=True)


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
                elif pl.code == "NSAT_REVERSE" or pl.code == "NSAT":
                    net_salary = net_salary + pl.amount
                elif pl.code == "ST_REVERSE" or pl.code == "ST":
                    tax = tax + pl.amount
                elif pl.code == "ICSR_REVERSE" or pl.code == "SIR_REVERSE" or pl.code == "ICSR" or pl.code == "SIR":
                    insurance = insurance + pl.amount

            payslip.state = "done"

        self.payslips_net_salaries = net_salary
        self.payslips_insurance = insurance
        self.payslips_gross = gross
        self.payslips_taxes = tax * -1
        self.payslips_basics = basic

    def create_payslips_invoice(self):

        productProductPayrollServiceId = ""
        productProductHandlingFeesId = ""


        invoice = self.env['account.move'].create({
            'partner_id': int(self.partner_id),
            'invoice_payment_term_id': int(self.invoice_payment_term_id),
            'journal_id': int(self.journal_id),
            'invoice_user_id' : int(self._uid),
            'invoice_date' : self.invoice_date,
            'ref' : self.name,
            'move_type' : "out_invoice",
            #'invoice_payment_state' : "not_paid",
        })

        self.env.cr.commit()

        productProduct = self.env['product.product'].search([('default_code', '=', "PS01")])
        if productProduct:
            productProductPayrollServiceId = productProduct[0]['id']
            _logger.info('productProductPayrollServiceId minds ! "%s"' % (str(productProductPayrollServiceId)))

        productProduct = self.env['product.product'].search([('default_code', '=', "HF01")])
        if productProduct:
            productProductHandlingFeesId = productProduct[0]['id']
            _logger.info('productProductHandlingFeesId minds ! "%s"' % (str(productProductHandlingFeesId)))


        '''invoice_lines = self.env['account.move.line'].with_context(
            check_move_validity=False).create({
            'move_id': int(invoice),
            'partner_id': int(self.partner_id),
            'product_id': int(productProductPayrollServiceId),
            'quantity' : 1.0,
            'price_unit' : self.payslips_net_salaries,
            'credit' : self.payslips_net_salaries,
            'debit' : 0.0,
            'account_id' : self.account_id.id,
            'name' : "Basic: " + str(self.payslips_basics) + ", Gross: " + str(self.payslips_gross) + ", Social Insurances: " + str(self.payslips_insurance) + ", Taxes: " + str(self.payslips_taxes) + ", Net Salaries: " + str(self.payslips_net_salaries),
        })'''

        invoice_lines = self.env['account.move.line'].with_context(
            check_move_validity=False).create({
            'move_id': int(invoice),
            'partner_id': int(self.partner_id),
            'product_id': int(productProductHandlingFeesId),
            'quantity': 1.0,
            'price_unit': self.payslips_net_salaries * 0.05,
            #'credit': self.payslips_net_salaries * 0.05,
            #'debit': 0.0,
            'account_id': self.account_id.id,
            'name' : "Basic: " + str(self.payslips_basics) + ", Gross: " + str(self.payslips_gross) + ", Social Insurances: " + str(self.payslips_insurance) + ", Taxes: " + str(self.payslips_taxes) + ", Net Salaries: " + str(self.payslips_net_salaries),
        })

        self.env.cr.commit()

