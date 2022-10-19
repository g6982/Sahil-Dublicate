odoo.define('cyb_pos_refund_policy.TicketScreenCustom', function(require) {
    'use strict';
    const Registries = require('point_of_sale.Registries');
    const TicketScreen = require('point_of_sale.TicketScreen');
    var rpc = require('web.rpc');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const { Gui } = require('point_of_sale.Gui');
    const TicketScreenExt = (TicketScreen) => class extends TicketScreen{
        constructor() {
            super(...arguments);
        }
        async _onClickOrder({ detail: clickedOrder }) {
            var self = this;
            if (!clickedOrder || clickedOrder.locked) {
                if (this._state.ui.selectedSyncedOrderId == clickedOrder.backendId) {
                    this._state.ui.selectedSyncedOrderId = null;
                } else {

                    console.log(clickedOrder.state);
                    if(clickedOrder.state=='paid' || clickedOrder.state=='done'){
                           await this.rpc({
                                model: 'pos.order',
                                method: 'get_refund_policy',
                                args: [[]],
                                kwargs: {context: {order: clickedOrder.name}},
                            })
                            .then(function (data) {
                                if (data=='Its old'){
                                    Gui.showPopup('ErrorPopup', {
                                        title: 'Error',
                                        body: 'You cannot refund the order that exceeds refund policy days.'
                                    });
                                }
                                else{
                                    self._state.ui.selectedSyncedOrderId = clickedOrder.backendId;
                                }
                            });
                    }
//                    else{
//                        this._state.ui.selectedSyncedOrderId = clickedOrder.backendId;
//                    }

                }
                if (!this.getSelectedOrderlineId()) {
                console.log('qwe2');
                    // Automatically select the first orderline of the selected order.
                    const firstLine = clickedOrder.get_orderlines()[0];
                    if (firstLine) {
                        this._state.ui.selectedOrderlineIds[clickedOrder.backendId] = firstLine.id;
                    }
                }
                NumberBuffer.reset();
            } else {
                this._setOrder(clickedOrder);
            }
            this.render();
        }
//        getHasItemsToRefund() {
//
//            const order = this.getSelectedSyncedOrder();
//            console.log(order);
//            console.log('za');
//            if(order){
//                this.rpc({
//                    model: 'pos.order',
//                    method: 'get_refund_policy',
//                    args: [[]],
//                    kwargs: {context: {order: order.id}},
//                })
//                .then(function (data) {
//                    console.log('success');
//                });
//            }
//            if (!order) return false;
//            if (this._doesOrderHaveSoleItem(order)) return true;
//
//
//             this.showPopup('ErrorPopup', {
//                    title: this.env._t('Its old'),
//                    body: 'cannot refund'
//                });
//            const total = Object.values(this.env.pos.toRefundLines)
//                .filter(
//                    (toRefundDetail) =>
//                        toRefundDetail.orderline.orderUid === order.uid && !toRefundDetail.destinationOrderUid
//                )
//                .map((toRefundDetail) => toRefundDetail.qty)
//                .reduce((acc, val) => acc + val, 0);
//            return !this.env.pos.isProductQtyZero(total);
//        }
    };
    Registries.Component.extend(TicketScreen, TicketScreenExt);
    return TicketScreen;
});
