from dateutil import parser
from stock_service.utils import stats
from stock_service.config import Config
from stock_service.producers.base import Producer
from stock_service.external.merchant_returns import get_merchant_return_item_price
from stock_service.external.tal import wms_instructions
from stock_client.constants import AdjustmentTypeNames, StockAdjustmentType

config = Config()


class StockAdjustmentProducer(Producer):
    @stats.profile_with_stats(namespace="producers")
    def send_stock_adjustment_event(
        self,
        adjusted_stock,
        adjustment,
        quantity,
        is_seller_listing: bool,
        instruction_id,
        advanced_shipping_notification,
        return_reference_number,
        trace_id,
        license_plate_number,
    ):

        if adjustment["quantity"] > 0:
            direction = wms_instructions.WmsInstruction.DIR_IN
        else:
            direction = wms_instructions.WmsInstruction.DIR_OUT

        instruction = wms_instructions.get_wms_instruction(
            adjustment["product_id"], instruction_id
        )
        adjustment_type = adjustment["adjustment_type"]
        adjustment_type_name = AdjustmentTypeNames.get(adjustment_type)

        received_at = parser.parse(adjustment["received_at"])

        payload = {
            "sku_id": adjustment["product_id"],
            "is_seller_listing": bool(is_seller_listing),
            "instruction_id": instruction_id,
            "instruction_type": instruction["instruction"].get("idInstructionType"),
            "adjustment_type_id": adjustment_type,
            "adjustment_type_name": adjustment_type_name,
            "asn": advanced_shipping_notification or "",
            "stock_on_hand": adjusted_stock["on_hand"] + adjusted_stock["in_returns"],
            "warehouse_direction": wms_instructions.WmsInstruction.DIRECTION_MAPPING[
                direction
            ],
            "warehouse_id": adjustment["warehouse_id"],
            "quantity": quantity,
            "cost_price": float(instruction["stock_item"].get("CostPrice", 0.0)),
            "received_timestamp": received_at.strftime("%Y-%m-%dT%H:%M:%S.%f+02:00"),
            "file": "stock_service/stock_service_controller.py",
            "order_id": instruction["instruction"].get("idOrder"),
            "rrn": instruction["instruction"].get("rrn")
            or return_reference_number
            or "",
            "lpn_nbr": license_plate_number,
            "trace_id": trace_id,
        }

        if (
            adjustment_type
            == StockAdjustmentType.TYPE_OUTBOUND_MERCHANT_RETURN_COLLECTED
        ):
            merchant_return_item_price = get_merchant_return_item_price(
                instruction_id, adjustment["product_id"]
            )

            if merchant_return_item_price:
                payload["user_captured_price"] = float(
                    merchant_return_item_price["price"]
                )

        self.send(payload, type="adjustment")

    @stats.profile_with_stats(namespace="producers")
    def send_stock_movement_event(
        self,
        adjusted_stock,
        adjustment,
        quantity,
        is_seller_listing: bool,
        instruction_id,
        advanced_shipping_notification,
    ):
        """
        send stock adjustment movement event to kafka `stock_adjustment_service` topic
        """
        if adjustment["quantity"] > 0:
            direction = wms_instructions.WmsInstruction.DIR_IN
        else:
            direction = wms_instructions.WmsInstruction.DIR_OUT

        instruction = wms_instructions.get_wms_instruction(
            adjustment["product_id"], instruction_id
        )
        adjustment_type = adjustment["adjustment_type"]

        payload = {
            "sku_id": adjustment["product_id"],
            "is_seller_listing": bool(is_seller_listing),
            "instruction_id": instruction_id,
            "instruction_type": instruction["instruction"].get("idInstructionType"),
            "adjustment_type_id": adjustment_type,
            "asn": advanced_shipping_notification or "",
            "warehouse_direction": wms_instructions.WmsInstruction.DIRECTION_MAPPING[
                direction
            ],
            "warehouse_id": adjustment["warehouse_id"],
            "quantity": quantity,
            "cost_price": float(instruction["stock_item"].get("CostPrice", 0.0)),
            "received_timestamp": adjustment["received_at"].strftime(
                "%Y-%m-%dT%H:%M:%S.%f+02:00"
            ),
            "file": "stock_service/stock_service_controller.py",
            "adjustment": {
                "idStockAdjustment": adjustment["adjustment_id"],
                "idProduct": adjustment["product_id"],
                "idParent": adjustment["parent_id"],
                "idCustomer": adjustment["customer_id"],
            },
            "snapshot": {
                "stockOnHand": adjusted_stock["on_hand"],
                "stockDamaged": adjusted_stock["damaged"],
                "stockDiscrepency": adjusted_stock["discrepancy"],
                "stockExpired": adjusted_stock["expired"],
                "stockInTransit": adjusted_stock["in_transit"],
                "stockSellable": adjusted_stock["sellable"],
                "stockAvailable": adjusted_stock["available"],
                "stockInReceiving": adjusted_stock["in_receiving"],
                "stockInReturns": adjusted_stock["in_returns"],
            },
        }

        if (
            adjustment_type
            == StockAdjustmentType.TYPE_OUTBOUND_MERCHANT_RETURN_COLLECTED
        ):
            merchant_return_item_price = get_merchant_return_item_price(
                instruction_id, adjustment["product_id"]
            )

            if merchant_return_item_price:
                payload["user_captured_price"] = float(
                    merchant_return_item_price["price"]
                )

        self.send(payload, type="stock_movement")
