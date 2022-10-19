# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning

# Ahmed Salama Code Start ---->
PARTNER_TYPE = [('customer_rank', 'Customer'), ('supplier_rank', 'Vendor'),
                ('employee', 'Employee'), ('no_partner', 'No Partner')]
RECIPT_TYPE = [('in', 'IN'), ('out', 'Out')]


class MoneyReceipt(models.Model):
    _name = 'money.receipt'
    _description = "Accounting Money Receipts In/Out"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _check_company_auto = True

    name = fields.Char("Money Receipt")
    active = fields.Boolean(default=True)
    receipt_type = fields.Selection(RECIPT_TYPE, "Receipt Type", required=True, tracking=True)
    journal_id = fields.Many2one('account.journal', "Journal", check_company=True, readonly=True, required=True,
                                 states={'draft': [('readonly', False)]}, tracking=True, domain=[('type', '=', 'cash')])
    account_id = fields.Many2one(related='journal_id.default_account_id', readonly=True)
    company_id = fields.Many2one('res.company', readonly=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', 'Currency', readonly=True, states={'draft': [('readonly', False)]},
                                  help='Utility field to express amount currency', required=True, tracking=True,
                                  default=lambda self: self.env.company.currency_id)
    item_ids = fields.One2many('money.receipt.item', 'money_receipt_id', "Items", readonly=True,
                               states={'draft': [('readonly', False)]})
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_compute_amount')
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
    ], string='Status', required=True, readonly=True, copy=False, tracking=True, default='draft')
    date = fields.Date(string='Date', required=True, index=True, readonly=True, tracking=True,
                       states={'draft': [('readonly', False)]}, copy=False, default=fields.Date.context_today)
    move_id = fields.Many2one('account.move', "Journal Entry")
    label = fields.Char('Label', readonly=True, states={'draft': [('readonly', False)]})

    # --------------------------------------------------
    # CRUD
    # --------------------------------------------------

    @api.model
    def create(self, vals):
        """
        Add Seq for Request
        :param vals: create vals
        :return: SUPER
        """
        vals['name'] = "MRECP/%s/%s" % (dict(self._fields['receipt_type'].selection).get(vals.get('receipt_type'))
                                        , self.env['ir.sequence'].sudo().next_by_code('money.receipt.code'))
        attend = super(MoneyReceipt, self).create(vals)
        return attend

    # --------------------------------------------------
    # actions
    # --------------------------------------------------

    def action_post(self):
        move_obj = self.env['account.move']
        for money_receipt in self:
            move_vals = self._prepare_move_values()
            move = move_obj.sudo().create(move_vals)
            if move:
                move.post()
                money_receipt.move_id = move.id
                money_receipt.state = 'posted'
            else:
                raise Warning(_("Something went wrong while creating move!!!"))

    def action_cancel(self):
        """
        - Cancel Request
        """
        for rec in self:
            rec.state = 'cancel'

    def action_draft(self):
        """
        - reset state to draft
        """
        for rec in self:
            rec.state = 'draft'

    # --------------------------------------------------
    # main methods
    # --------------------------------------------------

    def _prepare_move_values(self):
        """
        This function prepares move values related to an expense
        """
        self.ensure_one()

        total_amount = sum(item.amount for item in self.item_ids)
        if self.label:
            name = self.label
        else:
            name = self.name
        move_line_src = {
            'name': name,
            'quantity': 1,
            'debit': total_amount if self.receipt_type == 'in' else 0,
            'credit': total_amount if self.receipt_type == 'out' else 0,
            'account_id': self.account_id.id,
            'money_receipt_id': self.id,
            'currency_id': self.currency_id.id,
        }
        move_lines = self.item_ids._get_account_move_line_values()
        move_lines.append((0, 0, move_line_src))
        print("MOVE VALS:: ", move_lines)
        move_values = {
            'journal_id': self.journal_id.id,
            'company_id': self.company_id.id,
            'date': self.date,
            'ref': self.label,
            'money_receipt_id': self.id,
            'name': '/',
            'line_ids': move_lines
        }
        return move_values

    @api.onchange('item_ids')
    @api.depends('item_ids.amount')
    def _compute_amount(self):
        for receipt in self:
            receipt.amount_total = sum(item.amount for item in receipt.item_ids)


class MoneyReceiptItem(models.Model):
    _name = 'money.receipt.type'
    _description = "Accounting Money Receipts Item In/Out"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _check_company_auto = True

    @api.onchange('receipt_type', 'account_optional')
    def account_domain(self):
        account_domain = []
        if self.account_optional:
            if self.receipt_type == 'out':
                account_domain = []
            elif self.receipt_type == 'in':
                account_domain = []
        # return {'domain': {'account_id': account_domain}}
        return account_domain

    name = fields.Char("Type", required=True)
    active = fields.Boolean(default=True)
    receipt_type = fields.Selection(RECIPT_TYPE, "Receipt Type", required=True, tracking=True)
    company_id = fields.Many2one('res.company', readonly=True, default=lambda self: self.env.company)
    account_optional = fields.Boolean("Account Optional",
                                      help="If selected account field will be optional, to be selected from receipt itself")
    account_id = fields.Many2one('account.account', string='Account', index=True, ondelete="cascade",
                                 tracking=True, check_company=True, domain=account_domain)
    partner_type = fields.Selection(PARTNER_TYPE, "Partner Type", required=True, default='no_partner')


class MoneyReceiptLine(models.Model):
    _name = 'money.receipt.item'
    _description = "Accounting Money Receipts Line In/Out"

    @api.onchange('money_receipt_type_id')
    @api.depends('money_receipt_type_id.partner_type')
    def partner_domain(self):
        partner_domain = []
        type_id = self.money_receipt_type_id
        if type_id and type_id.partner_type:
            if type_id.partner_type in ['customer_rank', 'supplier_rank']:
                partner_domain = [(type_id.partner_type, '!=', 0)]
            elif type_id.partner_type == 'employee':
                employee_partners = self.env['res.partner'].search([('employee_id', '!=', False)])
                partner_domain = [('id', 'in', list(set(employee_partners.ids)))]
        return {'domain': {'partner_id': partner_domain}}
        # return partner_domain

    @api.onchange('money_receipt_type_id')
    @api.depends('money_receipt_type_id.partner_type')
    def account_domain(self):
        account_domain = []
        type_id = self.money_receipt_type_id
        if type_id and type_id.account_optional:
            if type_id.receipt_type == 'out':
                account_domain = [('user_type_id', '=', 15)]
            elif type_id.receipt_type == 'in':
                account_domain = [('user_type_id', 'in', [3, 14])]
        return {'domain': {'account_id': account_domain}}
        # return account_domain

    @api.onchange('money_receipt_type_id')
    def _onchange_money_receipt_type_id(self):
        for item in self:
            account_id = False
            if item.money_receipt_type_id and item.money_receipt_type_id.account_id:
                account_id = item.money_receipt_type_id.account_id.id
            item.account_id = account_id
            item.label = item.money_receipt_id.label

    money_receipt_id = fields.Many2one('money.receipt', "Money Receipt")
    receipt_type = fields.Selection(related='money_receipt_id.receipt_type')
    money_receipt_type_id = fields.Many2one('money.receipt.type', "Item", required=True, tracking=True)
    partner_type = fields.Selection(related='money_receipt_type_id.partner_type')
    account_optional = fields.Boolean(related='money_receipt_type_id.account_optional')
    account_id = fields.Many2one('account.account', string='Account', index=True, ondelete="cascade",
                                 required=True, tracking=True, check_company=True, )
    company_id = fields.Many2one('res.company', readonly=True, default=lambda self: self.env.company)
    partner_id = fields.Many2one('res.partner', "Partner")
    currency_id = fields.Many2one(related='money_receipt_id.currency_id', string='Currency',
                                  readonly=True, store=True,
                                  help='Utility field to express amount currency')
    amount = fields.Monetary(string='Amount', default=0.0, currency_field='currency_id')
    label = fields.Char('Label')

    def _get_account_move_line_values(self):
        move_line_values = []
        for item in self:
            move_line_name = ""
            if item.label:
                move_line_name = item.label
            else:
                if item.partner_id:
                    move_line_name += item.partner_id.name + ': '
                if item.money_receipt_id:
                    move_line_name += item.money_receipt_id.name
            account_dst = item.account_id
            account_date = item.money_receipt_id.date or fields.Date.context_today()

            # destination move line
            move_line_dst = (0, 0, {
                'name': move_line_name,
                'debit': item.amount if item.receipt_type == 'out' else 0,
                'credit': item.amount if item.receipt_type == 'in' else 0,
                'account_id': account_dst.id,
                'date_maturity': account_date,
                'currency_id': item.currency_id.id,
                'money_receipt_id': item.money_receipt_id.id,
                'money_receipt_item_id': item.id,
                'partner_id': item.partner_id.id,
            })
            move_line_values.append(move_line_dst)

        return move_line_values

# Ahmed Salama Code End.
