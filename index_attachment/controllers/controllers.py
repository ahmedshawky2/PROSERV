# -*- coding: utf-8 -*-
from odoo import http

# class IndexAttachment(http.Controller):
#     @http.route('/index_attachment/index_attachment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/index_attachment/index_attachment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('index_attachment.listing', {
#             'root': '/index_attachment/index_attachment',
#             'objects': http.request.env['index_attachment.index_attachment'].search([]),
#         })

#     @http.route('/index_attachment/index_attachment/objects/<model("index_attachment.index_attachment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('index_attachment.object', {
#             'object': obj
#         })