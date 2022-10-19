# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning
# Ahmed Salama Code Start ---->


class AccountMoveInherit(models.Model):
	_inherit = 'account.move'
	
	money_receipt_id = fields.Many2one('money.receipt', "Money Receipt")
	

class AccountMoveLineInherit(models.Model):
	_inherit = 'account.move.line'
	
	money_receipt_id = fields.Many2one('money.receipt', "Money Receipt")
	money_receipt_item_id = fields.Many2one('money.receipt.item', "Item")
	

# Ahmed Salama Code End.
