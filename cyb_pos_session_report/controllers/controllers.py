# -*- coding: utf-8 -*-
# from odoo import http


# class PosSessionReport(http.Controller):
#     @http.route('/cyb_pos_session_report/cyb_pos_session_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cyb_pos_session_report/cyb_pos_session_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cyb_pos_session_report.listing', {
#             'root': '/cyb_pos_session_report/cyb_pos_session_report',
#             'objects': http.request.env['cyb_pos_session_report.cyb_pos_session_report'].search([]),
#         })

#     @http.route('/cyb_pos_session_report/cyb_pos_session_report/objects/<model("cyb_pos_session_report.cyb_pos_session_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cyb_pos_session_report.object', {
#             'object': obj
#         })
