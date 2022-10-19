# -*- coding: utf-8 -*-
# from odoo import http


# class HrEmployeePartnerRel(http.Controller):
#     @http.route('/hr_employee_partner_rel/hr_employee_partner_rel/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_employee_partner_rel/hr_employee_partner_rel/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_employee_partner_rel.listing', {
#             'root': '/hr_employee_partner_rel/hr_employee_partner_rel',
#             'objects': http.request.env['hr_employee_partner_rel.hr_employee_partner_rel'].search([]),
#         })

#     @http.route('/hr_employee_partner_rel/hr_employee_partner_rel/objects/<model("hr_employee_partner_rel.hr_employee_partner_rel"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_employee_partner_rel.object', {
#             'object': obj
#         })
