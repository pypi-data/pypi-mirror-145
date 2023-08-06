import unittest
from stock_client.models import ServiceDict, StockServiceDict


class ServiceDictTestCase(unittest.TestCase):
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

    BIND_ALIAS_FIELDS = {
        "idProduct": "product_id",
        "stockOnHand": "on_hand",
        "stockDamaged": "damaged",
        "stockDiscrepency": "discrepancy",
        "stockExpired": "expired",
        "stockInTransit": "in_transit",
        "stockSellable": "sellable",
        "stockAvailable": "available",
        "stockInReceiving": "in_receiving",
        "stockInReturns": "in_returns",
        "stockIbtPrep": "ibt_prep",
    }

    def _assertions(self, response):
        self.assertEqual(response["product_id"], self.STOCK["product_id"])

        with self.assertWarns(DeprecationWarning):
            self.assertEqual(response.idProduct, self.STOCK["product_id"])

        with self.assertWarns(DeprecationWarning):
            self.assertEqual(response["idProduct"], self.STOCK["product_id"])

        with self.assertWarns(DeprecationWarning):
            self.assertEqual(response.get("idProduct"), self.STOCK.get("product_id"))

    def test_response_binding(self):
        response = ServiceDict(self.STOCK, self.BIND_ALIAS_FIELDS)
        self._assertions(response)

    def test_calculated_sellable_stock(self):
        response = StockServiceDict(self.STOCK)
        self.assertEqual(response.calculated_sellable_stock, 2)
        self.assertEqual(response.available_stock, self.STOCK["available"])

    def test_response_on_change(self):
        response = StockServiceDict(self.STOCK)

        # test change using new field name
        response["product_id"] += 1
        self.STOCK["product_id"] += 1
        self._assertions(response)

        # test change using new field name
        response.product_id += 1
        self.STOCK["product_id"] += 1
        self._assertions(response)

        # test change using old camelcase field name
        self.STOCK["product_id"] += 1
        with self.assertWarns(DeprecationWarning):
            response["idProduct"] += 1
        self._assertions(response)

        # test change using old camelcase field name
        self.STOCK["product_id"] += 1
        with self.assertWarns(DeprecationWarning):
            response.idProduct += 1
        self._assertions(response)

    def test_response_to_dict(self):
        response = ServiceDict(self.STOCK, self.BIND_ALIAS_FIELDS)
        self.assertDictEqual(response.to_dict(False), self.STOCK)

        expected_keys = [
            "idProduct",
            "warehouse_id",
            "stockOnHand",
            "stockDamaged",
            "stockDiscrepency",
            "stockExpired",
            "stockInTransit",
            "stockSellable",
            "stockAvailable",
            "stockInReceiving",
            "stockInReturns",
            "stockIbtPrep",
        ]

        returned_keys = response.to_dict(use_alias=True).keys()
        self.assertListEqual(list(returned_keys), expected_keys)
