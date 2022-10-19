# -*- coding: utf-8 -*-
# from odoo import http


# class InventoryTransferNotification(http.Controller):
#     @http.route('/inventory_transfer_notification/inventory_transfer_notification', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventory_transfer_notification/inventory_transfer_notification/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventory_transfer_notification.listing', {
#             'root': '/inventory_transfer_notification/inventory_transfer_notification',
#             'objects': http.request.env['inventory_transfer_notification.inventory_transfer_notification'].search([]),
#         })

#     @http.route('/inventory_transfer_notification/inventory_transfer_notification/objects/<model("inventory_transfer_notification.inventory_transfer_notification"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventory_transfer_notification.object', {
#             'object': obj
#         })
