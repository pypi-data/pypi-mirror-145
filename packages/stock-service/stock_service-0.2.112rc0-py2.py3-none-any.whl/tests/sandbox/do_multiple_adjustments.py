from multiprocessing import Pool
import random
import time

from stock_client import StockServiceClient
from stock_client.constants import StockAdjustmentType
from stock_service.config import Config
from stock_service.errors import InvalidStockAdjustmentError
from stock_service.stock_management.adjustment import calculate_stock_quantity

config = Config()
config.configure()
stock_client = StockServiceClient(endpoints=config.find_service("stock-service"))
ADJUSTMENTS = 100
CONCURRENCY = 5


def pick_random_adjustment():
    reason_codes = list(StockAdjustmentType)
    while True:
        old_reason_code = random.choice(reason_codes)
        new_reason_code = random.choice(reason_codes)

        stock = {
            "product_id": 1,
            "warehouse_id": 1,
            "on_hand": 10,
            "damaged": 10,
            "discrepancy": 10,
            "expired": 10,
            "in_transit": 10,
            "sellable": 10,
            "available": 10,
            "in_receiving": 10,
            "in_returns": 10,
        }

        try:
            new_stock = calculate_stock_quantity(
                take2stock=stock,
                old_reasoncode=old_reason_code,
                new_reasoncode=new_reason_code,
                quantity=1,
            )
        except InvalidStockAdjustmentError:
            continue

        new_stock = dict(new_stock)
        if new_stock != stock:
            return old_reason_code, new_reason_code


def get_test_product_ids():
    with config.db_client.get_connection("take2_primary") as connection:
        rows = connection.execute(
            """
            SELECT
                idProduct
            FROM
                products
            WHERE
                Active = 1 LIMIT 100
        """
        ).fetchall()
        return (row["idProduct"] for row in rows)


def make_random_adjustment():
    product_id = random.choice(list(get_test_product_ids()))
    warehouse_id = random.choice((1, 3))
    old_reason_code, new_reason_code = pick_random_adjustment()
    quantity = random.randint(1, 5)

    time.sleep(random.randint(1, 20) * 0.05)

    try:
        stock_client.adjust_stock(
            product_id=product_id,
            warehouse_id=warehouse_id,
            quantity=quantity,
            old_reasoncode=old_reason_code,
            new_reasoncode=new_reason_code,
        )
    except Exception as error:
        print(error)


def main():
    with Pool(CONCURRENCY) as pool:
        for _ in range(ADJUSTMENTS):
            pool.apply_async(make_random_adjustment)
        pool.close()
        pool.join()


if __name__ == "__main__":
    main()
