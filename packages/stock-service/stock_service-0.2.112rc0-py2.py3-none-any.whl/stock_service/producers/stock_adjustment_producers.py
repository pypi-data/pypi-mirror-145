from datetime import datetime

import pytz
from tal_schema_registry import SchemaRegistry

from stock_client.constants import AdjustmentTypeNames
from stock_service.utils import stats
from stock_service.config import Config

config = Config()


@stats.profile_with_stats(namespace="producers")
def send_stock_adjustment_error_event(event_type, error_type, error_message, payload):
    schema_producer = config.kafka_schema_producer(
        source_service_name=config.service_config.get_str("kafka.srv_name"),
        topic=config.service_config.get_str("stock_update_error.topic"),
        schema_registry=SchemaRegistry(),
    )
    schema_producer.send(payload, "stock_movement")


@stats.profile_with_stats(namespace="producers")
def send_stock_update_notify_event(
    product_reference,
    location,
    update_request,
    stock_levels,
    additional_data,
    trace_id,
    adjustment_id,
    movement_quantity,
    received_at,
):

    if received_at:
        received_at = pytz.timezone("UTC").localize(received_at)
    else:
        received_at = datetime.now(pytz.utc)

    # Remove data that is not levels
    stock_levels.pop("product_id", None)
    stock_levels.pop("warehouse_id", None)
    level_list = [
        {"status": status, "quantity": quantity}
        for status, quantity in stock_levels.items()
    ]

    update_request["new_adjustment_type"] = AdjustmentTypeNames.get(
        update_request["new_adjustment_type_id"], ""
    )
    update_request["previous_adjustment_type"] = AdjustmentTypeNames.get(
        update_request["previous_adjustment_type_id"], ""
    )
    update_request.setdefault("source_name", "")
    update_request.setdefault("source_reference", "")

    payload = {
        "owner": "tal",
        "product_reference": product_reference,
        "location": location,
        "update_request": update_request,
        "updated_stock_levels": level_list,
        "additional_data": {
            "customer_id": additional_data.get("customer_id", 0) or 0,
            "instruction_id": additional_data.get("instruction_id", 0) or 0,
            "is_prepaid_voucher": additional_data.get("is_prepaid_voucher", False)
            or False,
            "license_plate_number": additional_data.get("license_plate_number", "")
            or "",
            "advanced_shipping_notification": additional_data.get(
                "advanced_shipping_notification", ""
            )
            or "",
            "return_reference_number": additional_data.get(
                "return_reference_number", ""
            )
            or "",
            "group_number": additional_data.get("group_number", 0) or 0,
            "sequence_number": additional_data.get("sequence_number", 0) or 0,
        },
        "trace_id": str(trace_id or ""),
        "adjustment_id": adjustment_id or 0,
        "movement_quantity": movement_quantity or 0,
        "received_at": received_at.isoformat(),
    }

    schema_producer = config.kafka_schema_producer(
        source_service_name=config.service_config.get_str("kafka.srv_name"),
        topic=config.service_config.get_str("update_stock_notify_event.topic"),
        schema_registry=SchemaRegistry(),
    )

    schema_producer.send(
        message=payload,
        event_type=config.service_config.get_str("update_stock_notify_event.type"),
    )
