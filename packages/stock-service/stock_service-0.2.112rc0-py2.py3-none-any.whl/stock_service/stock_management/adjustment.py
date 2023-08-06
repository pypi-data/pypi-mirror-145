from stock_service.errors import InvalidStockAdjustmentError
from stock_service.models.take2.stock import Take2StockDict
from stock_service.utils import stats
from stock_service.config import OldConfig, Config
from stock_service.external.tal.ibt import prep

from stock_client.constants import StockAdjustmentType, FINAL_STOCK_ADJUSTMENT_STATES

logger = OldConfig.logger
config = Config()


def calculated_sellable_stock(stock: Take2StockDict) -> int:
    """
    Runs the stock sellable calculation as per the stock adjustments spec.

    NOTE: we do no checks on negative values here. If this formula results in a negative value it indicates
            that we have oversold.
    """
    return (
        stock["on_hand"] - stock["damaged"] - stock["expired"] - stock["in_receiving"]
    )


def calculate_stock_quantity(
    take2stock: Take2StockDict, old_reasoncode: int, new_reasoncode: int, quantity: int
) -> Take2StockDict:
    """
    recalculates stock quantity based reason codes

    :param stock: idproduct
    :param old_reasoncode: old adjustment type so we know if we must do any negative adjustments
    :param new_reasoncode: stock is always adjusted for a reason, this reason code specifies WHY
                            we are adjusting stock.
    :param quantity: the incremental quantity to adjust by
    """

    take2stock = Take2StockDict(**take2stock)

    # stock adjustments cannot transition from a final state to any other
    if int(old_reasoncode) in FINAL_STOCK_ADJUSTMENT_STATES:
        raise InvalidStockAdjustmentError(
            f"Stock adjustment not allowed: new_reasoncode={new_reasoncode}, old_reasoncode={old_reasoncode}"
        )
    #: new reason = inbound po receipt
    if int(new_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_RECEIPT:
        #: increment stock in receiving, but not yet put away.
        take2stock.on_hand += int(quantity)
        take2stock.in_receiving += int(quantity)
        if int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_DAMAGED:
            take2stock.on_hand -= int(quantity)
            take2stock.damaged -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_DAMAGED:
            take2stock.on_hand -= int(quantity)
            take2stock.damaged -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_EXPIRED:
            take2stock.on_hand -= int(quantity)
            take2stock.expired -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_SELLABLE:
            take2stock.on_hand -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_MISSING:
            take2stock.discrepancy -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_RETURN:
            take2stock.in_returns -= int(quantity)
    #: =====================================================================
    #: new reason = voetstoets inbound po receipt
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_VOET_INBOUND_PO_RECEIPT:
        #: increment stock in receiving, but not yet put away.
        take2stock.on_hand += int(quantity)
        take2stock.in_receiving += int(quantity)
        if int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_DAMAGED:
            take2stock.on_hand -= int(quantity)
            take2stock.damaged -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_DAMAGED:
            take2stock.on_hand -= int(quantity)
            take2stock.damaged -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_EXPIRED:
            take2stock.on_hand -= int(quantity)
            take2stock.expired -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_SELLABLE:
            take2stock.on_hand -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_MISSING:
            take2stock.discrepancy -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_RETURN:
            take2stock.in_returns -= int(quantity)
    #: =====================================================================
    #: new reason = voetstoets inbound po damaged
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_VOET_INBOUND_PO_DAMAGED:
        take2stock.on_hand += int(quantity)
        take2stock.damaged += int(quantity)
        if int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_RECEIPT:
            take2stock.on_hand -= int(quantity)
            take2stock.in_receiving -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_EXPIRED:
            take2stock.on_hand -= int(quantity)
            take2stock.expired -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_SELLABLE:
            take2stock.on_hand -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_MISSING:
            take2stock.discrepancy -= int(quantity)
    #: =====================================================================
    #: new reason = voetstoets general return
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_VOET_GENERAL_RETURN:
        take2stock.in_returns += int(quantity)  #: increment stock in returns
        if int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_RECEIPT:
            take2stock.in_receiving -= int(quantity)
            take2stock.on_hand -= int(quantity)
    #: =====================================================================
    #: new reason = voet expired
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_VOET_GENERAL_EXPIRED:
        take2stock.expired += int(quantity)
        take2stock.on_hand += int(quantity)
        if int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_DAMAGED:
            take2stock.on_hand -= int(quantity)
            take2stock.damaged -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_RECEIPT:
            take2stock.on_hand -= int(quantity)
            take2stock.in_receiving -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_SELLABLE:
            take2stock.on_hand -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_MISSING:
            take2stock.discrepancy -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_GOOD:
            take2stock.on_hand -= int(quantity)
    #: ======================================================================
    #: new reason = voet return to supplier
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_VOET_RETURN_TO_SUPPLIER:
        if int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_RECEIPT:
            take2stock.in_receiving += int(quantity)
            take2stock.on_hand += int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_RETURN:
            take2stock.in_returns += int(quantity)
        elif int(old_reasoncode) in (
            StockAdjustmentType.TYPE_GENERAL_DAMAGED,
            StockAdjustmentType.TYPE_INBOUND_PO_DAMAGED,
        ):
            take2stock.damaged += int(quantity)
            take2stock.on_hand += int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_EXPIRED:
            take2stock.expired += int(quantity)
            take2stock.on_hand += int(quantity)
        else:
            take2stock.on_hand += int(quantity)
    #: ======================================================================
    #: new reason = inbound po damaged
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_DAMAGED:
        take2stock.on_hand += int(quantity)
        take2stock.damaged += int(quantity)
        if int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_RECEIPT:
            take2stock.on_hand -= int(quantity)
            take2stock.in_receiving -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_EXPIRED:
            take2stock.on_hand -= int(quantity)
            take2stock.expired -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_SELLABLE:
            take2stock.on_hand -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_MISSING:
            take2stock.discrepancy -= int(quantity)
    #: ======================================================================
    #: new reason = inbound po sellable
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_SELLABLE:
        if int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_RECEIPT:
            take2stock.in_receiving -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_DAMAGED:
            take2stock.damaged -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_EXPIRED:
            take2stock.expired -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_MISSING:
            take2stock.discrepancy -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_RETURN:
            take2stock.on_hand += int(quantity)
            #: returns scenario 1 - here stock has moved from having an RTN lock code, to having no lock code
            # (Returns -> good)
            take2stock.in_returns -= int(quantity)
    #: ======================================================================
    #: new reason = inbound sellable migration
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_INBOUND_SELLABLE_MIGRATION:
        take2stock.on_hand += int(quantity)
    #: ======================================================================
    #: new reason = internal allocation adjustment
    elif int(new_reasoncode) in (
        StockAdjustmentType.TYPE_INTERNAL_ALLOCATION_ADJUSTMENT,
        StockAdjustmentType.TYPE_MANUAL,
    ):
        #: stock on hand is not adjusted for internet allocation at this moment.
        # An internal allocation is not a real stock adj. it's internal to tal, when an order item changes status,
        # We need to recalculate stock so that 'available' takes into account the change of item status but
        # Stock on hand is not actually affected until we get a message from the warehouse
        pass
    #: ======================================================================
    #: new reason = general return
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_GENERAL_RETURN:
        take2stock.in_returns += int(quantity)  #: increment stock in returns
        if int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_RECEIPT:
            take2stock.in_receiving -= int(quantity)
            take2stock.on_hand -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_CANCEL_COLLECT:
            take2stock.in_returns -= int(quantity)
    #: ======================================================================
    #: new reason = general good
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_GENERAL_GOOD:
        if int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_DAMAGED:
            take2stock.damaged -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_MISSING:
            # When something goes missing we take it out of on hand so here we must add it back
            take2stock.discrepancy -= int(quantity)
            take2stock.on_hand += int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_RECEIPT:
            take2stock.in_receiving -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_EXPIRED:
            take2stock.expired -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_RETURN:
            #: from return to good stock
            take2stock.in_returns -= int(quantity)
            take2stock.on_hand += int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_CANCEL_COLLECT:
            # we decrement stock here because it will be added back into stock later
            take2stock.on_hand -= int(quantity)
        else:
            take2stock.on_hand += int(quantity)
    #: ======================================================================
    #: new reason = inbound PO good
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_GOOD:
        if int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_DAMAGED:
            take2stock.damaged -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_RETURN:
            #: here we are going from a return, to good stock
            pass
        else:
            take2stock.on_hand += int(quantity)
    #: ======================================================================
    #: new reason = general damaged
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_GENERAL_DAMAGED:
        if int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_EXPIRED:
            take2stock.expired -= int(quantity)
            take2stock.damaged += int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_RECEIPT:
            take2stock.in_receiving -= int(quantity)
            take2stock.damaged += int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_MISSING:
            take2stock.on_hand += int(quantity)
            take2stock.discrepancy -= int(quantity)
            take2stock.damaged += int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_GOOD:
            take2stock.damaged += int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_CANCEL_COLLECT:
            # we decrement take2stock here because it will be added back into stock later
            take2stock.on_hand -= int(quantity)
            take2stock.damaged -= int(quantity)
        else:
            take2stock.on_hand += int(quantity)
            take2stock.damaged += int(quantity)

    #: =======================================================================
    #: new reason = expired
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_GENERAL_EXPIRED:
        if int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_DAMAGED:
            take2stock.damaged -= int(quantity)
            take2stock.expired += int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_RECEIPT:
            take2stock.expired += int(quantity)
            take2stock.in_receiving -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_SELLABLE:
            take2stock.expired += int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_MISSING:
            take2stock.expired += int(quantity)
            take2stock.on_hand += int(quantity)
            take2stock.discrepancy -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_GOOD:
            take2stock.expired += int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_CANCEL_COLLECT:
            # we decrement stock here because it will be added back into stock later
            take2stock.expired -= int(quantity)
            take2stock.on_hand -= int(quantity)
        else:
            take2stock.on_hand += int(quantity)
            take2stock.expired += int(quantity)

    #: =======================================================================
    #: new reason = general missing
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_GENERAL_MISSING:
        # When cancelling a collect orderitem only decrement stock on hand
        if int(old_reasoncode) == StockAdjustmentType.TYPE_CANCEL_COLLECT:
            take2stock.on_hand -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_DAMAGED:
            take2stock.damaged -= int(quantity)
            take2stock.discrepancy += int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_EXPIRED:
            take2stock.on_hand -= int(quantity)
            take2stock.expired -= int(quantity)
            take2stock.discrepancy += int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_GOOD:
            take2stock.on_hand -= int(quantity)
            take2stock.discrepancy += int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_RETURN:
            take2stock.in_returns -= int(quantity)
            take2stock.discrepancy += int(quantity)
        else:
            # When something goes missing increase stock in discrepency and decrease stock on hand
            take2stock.on_hand -= int(quantity)
            take2stock.discrepancy += int(quantity)
    #: =======================================================================
    #: new reason = sales order shipped
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_OUTBOUND_SALES_ORDER_SHIPPED:
        take2stock.on_hand -= int(quantity)
    #: =======================================================================
    #: new reason = ibt shipped
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_OUTBOUND_IBT_SHIPPED:
        take2stock.on_hand -= int(quantity)
    #: =======================================================================
    #: new reason = ibt cancelled
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_OUTBOUND_IBT_CANCELLED:
        pass
    #: =======================================================================
    #: new reason = ibt in transit
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_OUTBOUND_IBT_IN_TRANSIT:
        pass
    #: =======================================================================
    #: new reason = ibt good sellable received
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_INBOUND_IBT_SELLABLE:
        take2stock.on_hand += int(quantity)
    #: =======================================================================
    #: new reason = ibt bad damaged received
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_INBOUND_IBT_DAMAGED:
        take2stock.on_hand += int(quantity)
        take2stock.damaged += int(quantity)
    #: =======================================================================
    #: new reason = ibt received allocated on hold
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_OUTBOUND_AUTO_IBT_ON_HOLD:
        pass
    #: =======================================================================
    #: new reason = ibt in transit shipped
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_OUTBOUND_AUTO_IBT_IN_TRANSIT:
        take2stock.on_hand -= int(quantity)
    #: =======================================================================
    #: new reason = don't know what this means
    elif (
        int(new_reasoncode)
        == StockAdjustmentType.TYPE_OUTBOUND_AUTO_IBT_ON_HOLD_IN_TRANSIT
    ):
        pass
    #: =======================================================================
    #: new reason = ibt put away.
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_INBOUND_IBT_PUTAWAY:
        pass
    #: new reason = prepaid stock uploaded
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_PREPAID:
        take2stock.on_hand += int(quantity)
    #: new reason = return to supplier
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_RETURN_TO_SUPPLIER:
        if int(old_reasoncode) == StockAdjustmentType.TYPE_INBOUND_PO_RECEIPT:
            take2stock.in_receiving += int(quantity)
            take2stock.on_hand += int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_RETURN:
            take2stock.in_returns += int(quantity)
        elif int(old_reasoncode) in (
            StockAdjustmentType.TYPE_GENERAL_DAMAGED,
            StockAdjustmentType.TYPE_INBOUND_PO_DAMAGED,
        ):
            take2stock.damaged += int(quantity)
            take2stock.on_hand += int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_EXPIRED:
            take2stock.expired += int(quantity)
            take2stock.on_hand += int(quantity)
        else:
            take2stock.on_hand += int(quantity)
    elif int(new_reasoncode) == StockAdjustmentType.TYPE_TRUSTED_RETURN:
        # do nothing
        pass
    elif (
        int(new_reasoncode)
        == StockAdjustmentType.TYPE_OUTBOUND_MERCHANT_RETURN_COLLECTED
    ):
        if int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_GOOD:
            take2stock.on_hand -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_RETURN:
            take2stock.in_returns -= int(quantity)
        elif int(old_reasoncode) == StockAdjustmentType.TYPE_GENERAL_EXPIRED:
            take2stock.expired -= int(quantity)
            take2stock.on_hand -= int(quantity)
        else:
            raise InvalidStockAdjustmentError(
                f"Stock adjustment not allowed: new_reasoncode={new_reasoncode}, old_reasoncode={old_reasoncode}"
            )
    else:
        raise InvalidStockAdjustmentError(
            f"Unknown stock adjustment type new_reasoncode={new_reasoncode}, "
            f"old_reasoncode={old_reasoncode} - not processing"
        )

    return take2stock


@stats.profile_with_stats(namespace="internal")
def adjust_stock_quanities(
    take2stock: Take2StockDict,
    quantity: int,
    old_reason_code: int,
    new_reason_code: int,
) -> Take2StockDict:
    """
    Adjust stock for a product and warehouse depending on the old and new reason codes

    :param take2stock: product id
    :param quantity: the incremental qty to adjust by
    :param old_reason_code: old adjustment type so we know if we must do any negative adjustments
    :param new_reason_code: stock is always adjusted for a reason, this reason code specifies WHY we are adjusting
    :return: returns adjusted stock
    """

    if not (new_reason_code and old_reason_code):
        raise ValueError("A stock adjustment requires both a new and old reason code")

    if not (isinstance(new_reason_code, int) and isinstance(old_reason_code, int)):
        raise ValueError(
            f"new_reasoncode={new_reason_code} and old_reasoncode={old_reason_code} must be both int."
        )

    updated_take2stock = calculate_stock_quantity(
        take2stock, old_reason_code, new_reason_code, quantity
    )
    updated_take2stock["sellable"] = calculated_sellable_stock(updated_take2stock)
    updated_take2stock["ibt_prep"] = prep.calculate_ibt_prep(
        take2stock["product_id"], take2stock["warehouse_id"]
    )
    return updated_take2stock
