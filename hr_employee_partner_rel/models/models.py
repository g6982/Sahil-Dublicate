# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    employee_id = fields.Many2one('hr.employee', string='Employee')

    def action_update_employee_partner_id(self):
        for partner in self:
            partner.employee_id = False
            employee = self.env['hr.employee'].search([('address_home_id', '=', partner.id)])
            if employee:
                partner.update({
                    'employee_id': employee.id
                })


