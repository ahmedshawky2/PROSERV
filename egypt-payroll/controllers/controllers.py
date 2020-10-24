# -*- coding: utf-8 -*-
from odoo import http

# class Innovanity-payroll(http.Controller):
#     @http.route('/innovanity-payroll/innovanity-payroll/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/innovanity-payroll/innovanity-payroll/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('innovanity-payroll.listing', {
#             'root': '/innovanity-payroll/innovanity-payroll',
#             'objects': http.request.env['innovanity-payroll.innovanity-payroll'].search([]),
#         })

#     @http.route('/innovanity-payroll/innovanity-payroll/objects/<model("innovanity-payroll.innovanity-payroll"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('innovanity-payroll.object', {
#             'object': obj
#         })