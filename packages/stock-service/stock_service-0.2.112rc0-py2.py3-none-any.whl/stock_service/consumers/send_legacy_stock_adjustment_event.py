import json

from tal_kafka.consumer.application import ConsumerApplication
from tal_kafka.consumer.singleton import Consumer
from tal_stats_client import StatsClient

from stock_service.config import Config
from stock_client.constants import StockAdjustmentType, Warehouse
from stock_service.controllers import consumer_health_controller
from stock_service.external.tal.products import (
    create_wacp,
    get_legacy_product,
    is_digital,
)
from stock_service.producers import stock_producer
from stock_service.utils import stats

config = Config()
stats_client = StatsClient()
metric_base = "consumers.send_legacy_stock_adjustment_event.functions"

legacy_stock_adjustment_producer = stock_producer.StockAdjustmentProducer(
    topic="stock_adjustment_service"
)


@stats.profile_with_stats(
    namespace="consumers", stat_name="send_legacy_stock_adjustment_event"
)
def handle_event(event):
    payload = event.get("payload")

    product_id = int(payload["product_reference"])
    product = get_legacy_product(product_id)

    # send event to wacp queue if it's not a digital product and not a seller listing
    if product["idSupplier"] and not (
        product["IsSellerListing"] or is_digital(product)
    ):
        additional_data = payload["additional_data"]
        advanced_shipping_notification = additional_data[
            "advanced_shipping_notification"
        ]
        instruction_id = additional_data["instruction_id"]

        update_request = payload["update_request"]
        adjustment_type_id = update_request["new_adjustment_type_id"]
        quantity = update_request["quantity"]

        adjustment = dict(
            warehouse_id=Warehouse.CODE_TO_ID[payload["location"]],
            adjustment_id=payload["adjustment_id"],
            adjustment_type=adjustment_type_id,
            product_id=product_id,
            quantity=quantity,
            received_at=payload["received_at"],
        )

        wacp_quantity = quantity

        # create wacp entry in db if it's not a trusted return
        if adjustment_type_id != StockAdjustmentType.TYPE_TRUSTED_RETURN:
            movement_quantity = payload["movement_quantity"]
            wacp_quantity = movement_quantity

            with config.stats_client.timer(f"{metric_base}.create_wacp"):
                create_wacp(
                    instruction_id,
                    adjustment,
                    movement_quantity,
                    advanced_shipping_notification,
                )

        if wacp_quantity != 0:
            with config.stats_client.timer(
                f"{metric_base}.send_stock_adjustment_event"
            ):
                legacy_stock_adjustment_producer.send_stock_adjustment_event(
                    dict(
                        [
                            (level["status"], level["quantity"])
                            for level in payload["updated_stock_levels"]
                        ]
                    ),
                    adjustment,
                    wacp_quantity,
                    product["IsSellerListing"],
                    instruction_id,
                    advanced_shipping_notification,
                    additional_data["return_reference_number"],
                    payload["trace_id"],
                    additional_data["license_plate_number"],
                )


def handle_message(message):
    content = json.loads(message.value())
    handle_event(content)


def run_consumer():
    config.configure()

    consumer = Consumer()
    consumer.configure(
        hosts=config.kafka_brokers,
        group_id="stock_service_send_legacy_stock_adjustment_event",
        reset="largest",
    )
    consumer.subscribe(["stock_update_notify"])

    app = ConsumerApplication(process_callback=handle_message, workers=1)

    try:
        consumer_health_controller.touch()
        app.run()
    finally:
        consumer_health_controller.remove()


if __name__ == "__main__":
    run_consumer()
