from odoo import models, api, fields

from datetime import datetime


class PosSessioncloseReport(models.AbstractModel):
    _name = 'report.cyb_pos_session_report.session_closing_report'

    @api.model
    def _get_report_values(self, docids, data):
        session = self.env['pos.session'].browse(docids[0])
        if session:
            data = session.get_closing_control_data()
        if docids.__len__()==2:
            counted_cash = docids[1]
        else:
            counted_cash = 0

        if session.cash_register_total_entry_encoding:
            payment_in_cash = session.cash_register_total_entry_encoding
        else:
            payment_in_cash = 0

        return {
            'doc_ids': docids,
            'doc_model': self.env['res.company'],
            'data': data,
            'docs': self.env['res.company'].browse(self.env.company.id),
            'counted_cash':counted_cash,
            'payment_in_cash':payment_in_cash,
            'company': session.company_id.name,
            'pos':session.config_id.name,
            'username':session.user_id.name,
            'display_currency': session.currency_id

        }