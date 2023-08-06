import time
from typing import List

import click

from stock_client.constants import StockAdjustmentType, Warehouse
from stock_service.config import Config
from stock_service.producers.base import Producer

config = Config()

STOCK_NEW = 0
STOCK_PUTAWAY = 1


def get_product_ids(num_ids: int) -> List[int]:
    """
    Return a list of random product IDs from the DB

    :param num_ids: Number of IDs to return for our test
    :returns: A list of randomly selected product IDs
    """
    with config.db_client.get_session_context(role="stock_replica") as session:
        results = session.execute(
            """
            SELECT DISTINCT product_reference
            FROM inventory
            ORDER BY RAND()
            LIMIT :num_ids
        """,
            {"num_ids": num_ids},
        ).fetchall()
        return [product["product_reference"] for product in results]


class ConsumerTester:
    def __init__(self):
        topic = config.service_config.get_str("update_stock_request_event.topic")
        self.producer = Producer(topic=topic)

    def run_test(self, rate: int, test_product_ids: List[int]):
        """
        Continously produce dummy messages to the topic at the given rate

        :param rate: Number of messages to send per minute
        :param test_product_ids: Product IDs to include in the test
        """
        incoming_stock_payload = self._create_payload(STOCK_NEW)
        putaway_payload = self._create_payload(STOCK_PUTAWAY)
        sleep_time = 60 / rate
        counter = 0

        config.logger.info("producer sleep time set to: %s seconds", sleep_time)

        while True:
            product_id = test_product_ids[counter]
            incoming_stock_payload["product_reference"] = str(product_id)
            putaway_payload["product_reference"] = str(product_id)
            self.producer.send(incoming_stock_payload, "adjust_stock")
            self.producer.send(putaway_payload, "adjust_stock")
            config.logger.debug("Sent 'adjust_stock' for product_id %s", product_id)
            # Continuously iterate through our test products
            counter = (counter + 1) % len(test_product_ids)
            time.sleep(sleep_time)

    def _create_payload(self, adjustment_type: int):
        """
        Produce dummy stock adjustment payload based on the given type
        """
        payload = {
            "quantity": 1,
            "additional_data": {
                "customer_id": 0,
                "instruction_id": 0,
                "advanced_shipping_notification": "",
                "is_prepaid_voucher": False,
                "license_plate_number": "",
                "return_reference_number": "",
                "group_number": 0,
                "sequence_number": 0,
            },
            "source_name": "",
            "source_reference": "",
            "trace_id": "",
        }
        if adjustment_type == STOCK_NEW:
            payload.update(
                {
                    "previous_adjustment_type": StockAdjustmentType.TYPE_INBOUND_PO_RECEIPT,
                    "new_adjustment_type": StockAdjustmentType.TYPE_INBOUND_PO_RECEIPT,
                    "location": Warehouse.JHB_CODE,
                }
            )
        else:
            payload.update(
                {
                    "previous_adjustment_type": StockAdjustmentType.TYPE_INBOUND_PO_RECEIPT,
                    "new_adjustment_type": StockAdjustmentType.TYPE_INBOUND_PO_SELLABLE,
                    "location": Warehouse.JHB_CODE,
                }
            )
        return payload


@click.command()
@click.option(
    "--rate", default=1000, type=click.INT, help="Messages to send per minute"
)
@click.option(
    "--num-products",
    default=10,
    type=click.INT,
    help="Number of actual products to use in the test",
)
def main(rate: int, num_products: int):
    """Runs the "load test" on the consumer"""
    config.configure()
    config.logger.info("Beginning Consumer Adjustments test")
    product_ids = get_product_ids(num_products)
    config.logger.info("products under test: %s", product_ids)
    tester = ConsumerTester()
    tester.run_test(rate, product_ids)


if __name__ == "__main__":
    main()
