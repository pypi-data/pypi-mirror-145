import sys

from stock_service.config import Config
from stock_service.external.tal.products import get_legacy_product, is_digital

config = Config()
config.configure()


def main():
    with config.db_client.get_connection("take2_replica") as connection:
        rows = connection.execute(
            """
            SELECT
                idProduct
            FROM
                tsin_products
                JOIN tsin_formats ON tsin_formats.idTsin = tsin_products.idTsin
            WHERE
                tsin_formats.idFormat = 5
            LIMIT 100
        """
        ).fetchall()
        for row in rows:
            (product_id,) = row
            print(product_id)


def check_product(product_id):
    product = get_legacy_product(product_id)
    print(is_digital(product))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        check_product(int(sys.argv[1]))
    else:
        main()
