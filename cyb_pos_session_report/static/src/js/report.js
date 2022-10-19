odoo.define('cyb_pos_session_report.ClosePosPopupCustom', function(require) {
    'use strict';
    const Registries = require('point_of_sale.Registries');
    var rpc = require('web.rpc');
    const ClosePosPopup = require('point_of_sale.ClosePosPopup');
    const ClosePosPopupExt = (ClosePosPopup) => class extends ClosePosPopup{
        constructor() {
            super(...arguments);
        }
        PrintReportclosePos() {
        console.log(this.state.payments[this.defaultCashDetails.id].counted);
            this.env.pos.do_action('cyb_pos_session_report.session_closing_report', {
                    additional_context: {
                        active_ids: [this.env.pos.pos_session.id,this.state.payments[this.defaultCashDetails.id].counted],
                    },

                });


        }
    };
    Registries.Component.extend(ClosePosPopup, ClosePosPopupExt);
    return ClosePosPopup;
});
