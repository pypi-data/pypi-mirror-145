import json

from tal_kafka.consumer.application import ConsumerApplication
from tal_kafka.consumer.singleton import Consumer

from stock_service.utils import stats
from stock_service.config import Config
from stock_client.constants import Warehouse
from stock_service.controllers import consumer_health_controller, stock_controller
from stock_service.managers.update_stock_managers import adjust_stock_async
from stock_service.producers.stock_adjustment_producers import (
    send_stock_adjustment_error_event,
)


config = Config()
error_event_type = config.service_config.get_str("update_stock_error_event.type")


@stats.profile_with_stats(namespace="consumers", stat_name="adjust_stock")
def handle_adjust_stock(event):
    config.logger.debug(f"Handling adjust_stock event: {event}")
    payload = event.get("payload")
    additional_data = payload.get("additional_data", {})
    try:
        adjust_stock_async(
            product_id=int(payload["product_reference"]),
            warehouse_id=Warehouse.CODE_TO_ID[payload["location"]],
            quantity=payload.get("quantity"),
            old_reason_code=payload.get("previous_adjustment_type"),
            new_reason_code=payload.get("new_adjustment_type"),
            customer_id=additional_data.get("customer_id", 0),
            instruction_id=additional_data.get("instruction_id", 0),
            advanced_shipping_notification=additional_data.get(
                "advanced_shipping_notification", ""
            ),
            license_plate_number=additional_data.get("license_plate_number", ""),
            return_reference_number=additional_data.get("return_reference_number", ""),
            is_prepaid_voucher=additional_data.get("is_prepaid_voucher", False),
            trace_id=payload.get("trace_id"),
            group_number=additional_data.get("group_number", 0),
            sequence_number=additional_data.get("sequence_number", 0),
        )

    except Exception as error:
        config.logger.exception(error)
        send_stock_adjustment_error_event(
            "adjust_stock", type(error).__name__, str(error), payload
        )


@stats.profile_with_stats(namespace="consumers", stat_name="set_stock")
def handle_set_stock(event):
    config.logger.debug(f"Handling set_stock event: {event}")
    payload = event.get("payload")
    stock = {
        "product_id": int(payload["product_reference"]),
        "warehouse_id": Warehouse.CODE_TO_ID[payload["location"]],
    }
    # assume take2 level names for now and not doing any conversion
    for level in payload["levels"]:
        stock[level["status"]] = level["quantity"]
    try:
        stock_controller.update_stock(stock)
    except Exception as error:
        config.logger.exception(error)
        send_stock_adjustment_error_event(
            "set_stock", type(error).__name__, str(error), payload
        )


def handle_message(message):
    content = json.loads(message.value())
    config.logger.info(content)
    if content["type"] == "adjust_stock":
        handle_adjust_stock(content)
    elif content["type"] == "set_stock":
        handle_set_stock(content)


def run_consumer():
    config.configure()

    consumer = Consumer()
    consumer.configure(
        hosts=config.kafka_brokers,
        group_id=config.service_config.get_str("update_stock_request_event.group_id"),
    )
    consumer.subscribe(
        [config.service_config.get_str("update_stock_request_event.topic")]
    )

    app = ConsumerApplication(
        process_callback=handle_message,
        workers=config.service_config.get_int("update_stock_request_event.workers"),
        max_queue_size=5,
    )

    try:
        consumer_health_controller.touch()
        app.run()
    finally:
        consumer_health_controller.remove()


if __name__ == "__main__":
    run_consumer()
