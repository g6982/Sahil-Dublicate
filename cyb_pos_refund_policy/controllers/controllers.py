# -*- coding: utf-8 -*-
# from odoo import http


# class PosRefundPolicy(http.Controller):
#     @http.route('/cyb_pos_refund_policy/cyb_pos_refund_policy', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cyb_pos_refund_policy/cyb_pos_refund_policy/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cyb_pos_refund_policy.listing', {
#             'root': '/cyb_pos_refund_policy/cyb_pos_refund_policy',
#             'objects': http.request.env['cyb_pos_refund_policy.cyb_pos_refund_policy'].search([]),
#         })

#     @http.route('/cyb_pos_refund_policy/cyb_pos_refund_policy/objects/<model("cyb_pos_refund_policy.cyb_pos_refund_policy"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cyb_pos_refund_policy.object', {
#             'object': obj
#         })
