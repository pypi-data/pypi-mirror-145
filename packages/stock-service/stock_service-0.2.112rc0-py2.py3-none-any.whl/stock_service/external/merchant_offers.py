from retry import retry
from s4f.errors import ServiceError

from stock_client.constants import Warehouse
from stock_service.config import Config

config = Config()


@retry(exceptions=ServiceError, tries=3, delay=0.5)
def process_stock_adjustment(offer_id, warehouse_code, legacy_stock_available):
    config.merchant_offer_client.process_takealot_stock_adjustment(
        offer_id=offer_id,
        takealot_stock={Warehouse.CODE_TO_ID[warehouse_code]: legacy_stock_available},
    )
