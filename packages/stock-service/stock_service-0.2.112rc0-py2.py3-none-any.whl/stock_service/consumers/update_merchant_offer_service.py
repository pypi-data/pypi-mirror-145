import json

from tal_kafka.consumer.application import ConsumerApplication
from tal_kafka.consumer.singleton import Consumer

from stock_service.utils import stats
from stock_service.config import Config
from stock_service.controllers import consumer_health_controller
from stock_service.external.merchant_offers import process_stock_adjustment
from stock_service.external.tal.products import get_legacy_product

config = Config()


@stats.profile_with_stats(
    namespace="consumers", stat_name="update_merchant_offer_service"
)
def handle_event(event):
    payload = event.get("payload")

    product_id = int(payload["product_reference"])
    product = get_legacy_product(product_id)

    if not product["IsSellerListing"]:
        return

    available_stock = [
        level["quantity"]
        for level in payload["updated_stock_levels"]
        if level["status"] == "available"
    ][0]
    legacy_stock_available = max(available_stock, 0)

    process_stock_adjustment(product_id, payload["location"], legacy_stock_available)

    config.logger.info(
        "Merchant offer service updated with product=%s warehouse=%s stock=%s",
        product_id,
        payload["location"],
        legacy_stock_available,
    )


def handle_message(message):
    content = json.loads(message.value())
    handle_event(content)


def run_consumer():
    config.configure()

    consumer = Consumer()
    consumer.configure(
        hosts=config.kafka_brokers,
        group_id="stock_service_update_merchant_offer_service",
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
