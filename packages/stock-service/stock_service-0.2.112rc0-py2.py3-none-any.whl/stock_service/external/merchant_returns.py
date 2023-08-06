from retry import retry
from s4f.errors import ServiceError

from stock_service.config import Config
from stock_service.utils.stats import profile_with_stats

config = Config()


@profile_with_stats(namespace="external")
@retry(exceptions=ServiceError, tries=3, delay=0.5)
def get_good_stock_on_hold_by_product_id(product_id, warehouse_id):
    return config.merchant_returns_service_client.get_good_stock_on_hold_by_product_id(
        product_id, warehouse_id
    )


@profile_with_stats(namespace="external")
def get_merchant_return_item_price(instruction_id, product_id):
    return config.merchant_returns_service_client.get_merchant_return_item_price(
        instruction_id, product_id
    )
