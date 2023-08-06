import datetime
import sys
import threading

from unittest.mock import create_autospec
from s4f.errors import ServiceError

from stock_client import StockServiceClient
from stock_client.constants import StockAdjustmentType
from stock_service import service
from stock_service.controllers import stock_adjustment_controller
from stock_service.controllers import stock_controller
from stock_service.controllers import stock_snapshot_controller

from tests.stock_service.integration.base import BaseIntegrationTestCase
from tests.stock_service.data.stock import WAREHOUSES


class StockTestCase(BaseIntegrationTestCase):
    STOCK = {
        "product_id": 25,
        "warehouse_id": 3,
        "on_hand": 8,
        "damaged": 2,
        "discrepancy": 3,
        "expired": 1,
        "in_transit": 2,
        "sellable": 8,
        "available": 6,
        "in_receiving": 3,
        "in_returns": 2,
        "ibt_prep": 0,
    }

    ID = 6
    SNAPSHOT = {
        "on_hand": 1,
        "damaged": 2,
        "discrepancy": 3,
        "expired": 4,
        "in_transit": 5,
        "sellable": 6,
        "available": 7,
        "in_receiving": 8,
        "in_returns": 9,
        "ibt_prep": 0,
    }

    ADJUSTMENT = {
        "product_id": 1,
        "warehouse_id": 1,
        "customer_id": 1234,
        "quantity": 10,
        "new_reasoncode": StockAdjustmentType.TYPE_INBOUND_PO_RECEIPT,
        "old_reasoncode": StockAdjustmentType.TYPE_INBOUND_PO_SELLABLE,
        "instruction_id": 4567,
        "is_prepaid_voucher": False,
        "advanced_shipping_notification": "",
        "license_plate_number": "",
        "trace_id": "0ee92f80-b838-4a56-b846-04cc7cccdd94",
        "return_reference_number": "",
    }

    CLIENT_TEST_PORT = 7001

    @classmethod
    def setUpClass(cls):
        super().setUpClass(in_memory=False)
        cls.service_process = threading.Thread(
            target=service.run_service, args=(cls.CLIENT_TEST_PORT, 1)
        )
        cls.service_process.daemon = True
        cls.service_process.start()
        cls.client = StockServiceClient(["localhost:{}".format(cls.CLIENT_TEST_PORT)])

    def test_get_stock_levels(self):
        stock_controller.create_stock(self.STOCK)
        results = self.client.get_stock_levels(
            self.STOCK["product_id"], self.STOCK["warehouse_id"]
        )
        self.assertDictEqual(results, self.STOCK)

    def test_get_stock_levels_not_found(self):
        with self.assertRaises(ValueError):
            self.client.get_stock_levels(None, self.STOCK["warehouse_id"])
        with self.assertRaises(ValueError):
            self.client.get_stock_levels(1, 2)
        with self.assertRaises(ServiceError):
            self.client.get_stock_levels(sys.maxsize, self.STOCK["warehouse_id"])

    def test_create_and_get_stock_snapshot(self):
        results = self.client.create_stock_snapshot(self.ID, self.SNAPSHOT)
        self.assertEqual(results["adjustment_id"], self.ID)
        self.assertDictEqual(results["snapshot"], self.SNAPSHOT)
        results = self.client.get_stock_snapshot(self.ID)
        self.assertEqual(results["adjustment_id"], self.ID)
        self.assertDictEqual(results["snapshot"], self.SNAPSHOT)

    def test_get_unknown_stock_snapshot(self):
        with self.assertRaises(ServiceError):
            self.client.get_stock_snapshot(sys.maxsize)

    def test_create_duplicate_stock_snapshot(self):
        self.client.create_stock_snapshot(self.ID, self.SNAPSHOT)
        with self.assertRaises(ServiceError):
            self.client.create_stock_snapshot(self.ID, self.SNAPSHOT)

    def create_legacy_products_table(self):
        with self.sqlclient.get_connection("master") as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                `qtyInStockCpt` int(11) DEFAULT NULL,
                `qtyInStockJhb` int(11) DEFAULT NULL,
                `idProduct` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY
                );
                """
            )

    def test_get_stock_levels_for_warehouses(self):
        # GIVEN: stock in products table
        self.create_legacy_products_table()
        stock = dict(self.STOCK, warehouse=WAREHOUSES[self.STOCK["warehouse_id"]])
        stock_controller.create_stock(self.STOCK)

        # WHEN: getting stock using product_id and single warehouse_id
        stocks = self.client.get_stock_levels_for_warehouses(
            product_id=stock["product_id"], warehouse_ids=stock["warehouse_id"]
        )
        # THEN: list with one stock should be returned
        self.assertEqual(stocks.pop(), stock)

        # WHEN: getting stock using product_id and single warehouse_id as list
        stocks = self.client.get_stock_levels_for_warehouses(
            product_id=self.STOCK["product_id"],
            warehouse_ids=[self.STOCK["warehouse_id"]],
        )
        # THEN: list with one stock should be returned
        self.assertEqual(stocks.pop(), stock)

        # WHEN: getting stock using product_id and warehouse_ids=None
        stocks = self.client.get_stock_levels_for_warehouses(
            product_id=self.STOCK["product_id"], warehouse_ids=None
        )
        # THEN: stocks from all warehouses should be returned
        self.assertEqual(len(stocks), 2)
        cpt, jhb = stocks
        self.assertEqual(jhb, stock)
        self.assertDictEqual(
            cpt,
            {
                "product_id": 25,
                "warehouse_id": 1,
                "on_hand": 0,
                "damaged": 0,
                "discrepancy": 0,
                "expired": 0,
                "in_transit": 0,
                "sellable": 0,
                "available": 0,
                "in_receiving": 0,
                "in_returns": 0,
                "ibt_prep": 0,
                "warehouse": WAREHOUSES[1],
            },
        )
        with self.assertRaises(TypeError):
            self.client.get_stock_levels_for_warehouses(1, "invalid_warehouse")

        with self.assertRaises(ValueError):
            self.client.get_stock_levels_for_warehouses(None, 1)

    def get_stock_on_hand_for_products_by_datetime_fixture(
        self, product_id, create_snapshot=True
    ):
        adjustment = stock_adjustment_controller.create_stock_adjustment(
            dict(
                product_id=product_id,
                warehouse_id=self.ADJUSTMENT.get("warehouse_id"),
                quantity=self.ADJUSTMENT.get("quantity"),
                customer_id=self.ADJUSTMENT.get("customer_id"),
                adjustment_type=int(self.ADJUSTMENT.get("new_reasoncode")),
            )
        )

        if create_snapshot:
            stock_snapshot_controller.create_stock_snapshot(
                take2_adjustment_id=adjustment.adjustment_id,
                take2_snapshot=self.SNAPSHOT,
            )

    def test_get_stock_on_hand_for_products_by_datetime(self):
        product_id_with_adjustment_and_snapshots = [111, 222]
        product_id_without_adjustment_and_snapshots = [10, 11]
        product_id_with_adjustment_but_without_snapshots = [20, 21]

        for product_id in product_id_with_adjustment_and_snapshots:
            self.get_stock_on_hand_for_products_by_datetime_fixture(
                product_id, create_snapshot=True
            )

        for product_id in product_id_with_adjustment_but_without_snapshots:
            self.get_stock_on_hand_for_products_by_datetime_fixture(
                product_id, create_snapshot=False
            )

        # get stock on hand for products with snapshots and adjustment
        response = self.client.get_stock_on_hand_for_products_by_datetime(
            product_id_with_adjustment_and_snapshots,
            datetime.datetime.now() + datetime.timedelta(seconds=10),
        )
        self.assertEqual(
            response,
            [
                {
                    "product_id": i,
                    "stock_on_hand": self.SNAPSHOT["on_hand"]
                    + self.SNAPSHOT["in_returns"],
                }
                for i in product_id_with_adjustment_and_snapshots
            ],
        )

        # get stock on hand for products without adjustment, these should have stock_on_hand=0
        response = self.client.get_stock_on_hand_for_products_by_datetime(
            product_id_without_adjustment_and_snapshots,
            datetime.datetime.now() + datetime.timedelta(seconds=1),
        )
        self.assertEqual(
            response,
            [
                {"product_id": i, "stock_on_hand": 0}
                for i in product_id_without_adjustment_and_snapshots
            ],
        )

        # test client product_ids validation
        with self.assertRaises(ValueError):
            self.client.get_stock_on_hand_for_products_by_datetime(
                "junk", datetime.datetime.now()
            )

        # test client adjustment_datetime arg validation
        with self.assertRaises(ValueError):
            self.client.get_stock_on_hand_for_products_by_datetime(
                [1, 2], "junk datetime"
            )

    def test_retry(self):
        # GIVEN
        dummy_func = create_autospec(lambda s: s, side_effect=ValueError)
        with self.assertRaises(ValueError):
            retry = StockServiceClient.retry_call(ValueError, retries=3)
            retry(dummy_func)(self.client)

        # THEN
        self.assertEqual(dummy_func.call_count, 3)
