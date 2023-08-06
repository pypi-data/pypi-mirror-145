from stock_service.config import Config
from stock_service.models.owner import Owner
from stock_service.utils.stats import profile_with_stats

config = Config()


@profile_with_stats(namespace="database.stock")
def get_owner(owner_id):
    with config.db_client.get_session_context(role="stock_replica") as session:
        return session.query(Owner).filter(Owner.owner_id == owner_id).one()
