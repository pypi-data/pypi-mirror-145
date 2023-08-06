import threading
from unittest import TestCase

import pytest

from stock_client import StockServiceClient
from stock_client.constants import StockAdjustmentType
from stock_service import service
from stock_service.config import OldConfig, DEFAULTS
from stock_service.models.take2.stock import Take2Stock


class AdjustStockTestCase(TestCase):

    ADJUSTMENT = {
        "product_id": 1,
        "warehouse_id": 3,
        "customer_id": 1234,
        "quantity": 10,
        "new_reasoncode": StockAdjustmentType.TYPE_INBOUND_PO_RECEIPT,
        "old_reasoncode": StockAdjustmentType.TYPE_INBOUND_PO_SELLABLE,
        "instruction_id": "*",
        "is_prepaid_voucher": False,
        "advanced_shipping_notification": None,
        "license_plate_number": None,
        "trace_id": "0ee92f80-b838-4a56-b846-04cc7cccdd94",
        "return_reference_number": None,
    }

    CLIENT_TEST_PORT = 7001

    @classmethod
    def setUpClass(cls):
        DEFAULTS["ENV"] = "staging"  # connect to staging db
        OldConfig._instance = None
        OldConfig().configure(db_pool_size=1)

        cls.service_process = threading.Thread(
            target=service.run_service, args=(cls.CLIENT_TEST_PORT, 1)
        )
        cls.service_process.daemon = True
        cls.service_process.start()
        cls.client = StockServiceClient(["localhost:{}".format(cls.CLIENT_TEST_PORT)])

    def setUp(self):
        self.sql_client = OldConfig.get_db_client()
        # cleanup
        self.tearDown()
        # add test products
        with self.sql_client.get_session_context("master") as session:
            session.add(
                Take2Stock(
                    product_id=self.ADJUSTMENT["product_id"],
                    warehouse_id=self.ADJUSTMENT["warehouse_id"],
                )
            )
            session.commit()

    def tearDown(self):
        with self.sql_client.get_session_context("master") as session:
            session.query(Take2Stock).filter_by(
                product_id=self.ADJUSTMENT["product_id"],
                warehouse_id=self.ADJUSTMENT["warehouse_id"],
            ).delete()
            session.commit()

    @classmethod
    def tearDownClass(cls):
        DEFAULTS["ENV"] = "test"  # connect to staging db
        OldConfig._instance = None

    def test_adjust_stock_error(self):
        # test invalidate old_reasoncode
        with self.assertRaises(ValueError):
            self.client.adjust_stock(**dict(self.ADJUSTMENT, old_reasoncode=-3))
        # test invalidate new_reasoncode
        with self.assertRaises(ValueError):
            self.client.adjust_stock(**dict(self.ADJUSTMENT, new_reasoncode=-3))

    @pytest.mark.skip(
        reason="Cannot currently mock in a threaded service. Needs another solution."
    )
    def test_adjust_stock(self):
        out = self.client.adjust_stock(**self.ADJUSTMENT)
        adjusted_take2stock, take2adjustment = (
            out["adjusted_stock"],
            out["adjustment_record"],
        )
        stock_sellable = (
            adjusted_take2stock["on_hand"]
            - adjusted_take2stock["damaged"]
            - adjusted_take2stock["expired"]
            - adjusted_take2stock["in_receiving"]
        )
        self.assertDictEqual(
            {
                "product_id": self.ADJUSTMENT["product_id"],
                "warehouse_id": self.ADJUSTMENT["warehouse_id"],
                "on_hand": 0,
                "damaged": 0,
                "discrepancy": 0,
                "expired": 0,
                "in_transit": 0,
                "sellable": stock_sellable,
                "available": stock_sellable - adjusted_take2stock["ibt_prep"],
                "ibt_prep": 0,
                "in_receiving": self.ADJUSTMENT["quantity"],
                "in_returns": 0,
            },
            dict(adjusted_take2stock),
        )
        del take2adjustment["received_at"], take2adjustment["adjustment_id"]
        self.assertDictEqual(
            {
                "product_id": self.ADJUSTMENT["product_id"],
                "warehouse_id": self.ADJUSTMENT["warehouse_id"],
                "customer_id": self.ADJUSTMENT["customer_id"],
                "adjustment_type": StockAdjustmentType.TYPE_INBOUND_PO_RECEIPT,
                "quantity": self.ADJUSTMENT["quantity"],
            },
            dict(take2adjustment),
        )
