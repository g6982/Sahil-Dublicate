# -*- coding: utf-8 -*-
from datetime import timedelta, datetime

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    refund_days = fields.Integer(string="Return Period")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()

        res['refund_days'] = int(
            self.env['ir.config_parameter'].sudo().get_param('cyb_pos_refund_policy.refund_days', default=0))

        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('cyb_pos_refund_policy.refund_days', self.refund_days)

        super(ResConfigSettings, self).set_values()



class pos_order(models.Model):
    _inherit = 'pos.order'

    def get_refund_policy(self):
        if self._context.get('order'):
            order = self.env['pos.order'].search([('pos_reference','=',self._context['order'])])
            if order:
                days = int(self.env['ir.config_parameter'].sudo().get_param('cyb_pos_refund_policy.refund_days'))
                diff = datetime.now() - order.create_date
                if diff.days > days:
                    return 'Its old'
                else:
                    return ''
        else:
            return ''