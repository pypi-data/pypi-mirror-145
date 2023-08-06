import logging
import os
import pathlib
from pathlib import Path
import sys
import threading

import cache_client
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from sql_client import SQLClient

from merchant_returns_service_client import MerchantReturnsServiceClient
from s4f_clients.merchant_offer_service import MerchantOfferServiceClient
from tal_kafka.producer.schema_producer import SchemaProducer
from tal_kafka.producer.singleton import Producer
from tal_stats_client import StatsClient
from tal_service_config import ServiceConfig, FORMAT_LIST_OF_TUPLE

from stock_service.backports import cached_property
from stock_service.errors import ServiceError


defaults = {
    "update_stock_request_event": {
        "topic": "stock_update_request",
        "group_id": "stock_service_update_stock_consumer",
        "workers": 1,
    },
    "update_stock_error_event": {
        "topic": "stock_update_error",
        "type": "stock_update_error",
    },
    "update_stock_notify_event": {
        "topic": "stock_update_notify",
        "type": "stock_update_notify",
    },
}


class Config:
    """Singleton that returns a configured instance of the config"""

    SERVICE_NAME = "stock-service"
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
        return cls._instance

    @cached_property
    def env(self) -> str:
        return os.environ.get("ENVIRONMENT", "test")

    @cached_property
    def project_root(self) -> Path:
        return Path(__file__).parent.absolute()

    @cached_property
    def version(self):
        return (self.project_root / ".." / "version").read_text().strip()

    @cached_property
    def logger(self):
        LOGGING_FORMAT = "%(asctime)s %(levelname)s %(threadName)s %(filename)s:%(lineno)s %(message)s"
        logging.basicConfig(
            level=logging.INFO, format=LOGGING_FORMAT, stream=sys.stdout
        )
        return logging.getLogger(__file__)

    @cached_property
    def service_config(self) -> ServiceConfig:
        file = self.project_root / "config" / f"{self.env}.ini"
        self.logger.info("Loading configuration %s with ENVIRONMENT=%s", file, self.env)
        return ServiceConfig(defaults=defaults, ini_files=[file])

    @cached_property
    def stats_client(self) -> StatsClient:
        stats = StatsClient()
        if stats.is_configured():
            return stats
        host, port = self.resolve("statsd")
        stats.configure_for_service(
            os.environ.get("STATSD_NAMESPACE"), host, port, include_fqdn=False
        )
        return stats

    def get_stats_client(self) -> StatsClient:
        stats = StatsClient()
        if stats.is_configured():
            self.logger.warning("statsd client already configured")
        host, port = self.resolve("statsd")
        stats.configure_for_service(
            os.environ.get("STATSD_NAMESPACE"), host, port, include_fqdn=False
        )
        return stats

    def resolve(self, service_name: str) -> tuple:
        """
        resolves dns host ip and port for the specified service using ServiceConfig

        :param service_name: name of the service, i.e statsd, master_database, ...
        :return: tuple (host, port)
        """
        service_key = self.service_config.get(f"{service_name}.srv_name")
        if not service_key:  # check if .ini has .srv_name
            raise ServiceConfigError(f"{service_name} does not have 'srv_name'")
        host, port = self.service_config.find_service(
            service_key, format=FORMAT_LIST_OF_TUPLE
        )[0]
        return host, port

    @property
    def db_client(cls) -> SQLClient:
        return SQLClient()

    def get_db_session(self):
        return self.db_client.get_session_context

    def find_service(self, srv_name: str, format=None) -> list:
        """
        returns host ip and port of srv record
        """
        return self.service_config.find_service(srv_name)

    def configure_db(self, role: str, section_name: str, pool_size: int):
        """
        configures sql client DB connection using {role} as reference. The default configured roles are
        "master" and "slave"

        :param role: name of the connection
        :param section_name: section name in the .ini. example: "[slave_database]" in config/test.ini
        :param pool_size: sqlalchemy pool_size, this should the equals the number of threads / workers
        """

        if role in self.db_client.databases:
            self.logger.warning(f"database role '{role}' already configured")

        try:
            host, port = self.resolve(section_name)
        except ServiceConfigError:
            host = self.service_config.get(f"{section_name}.host")
            port = int(self.service_config.get(f"{section_name}.port"))

        conn_string = self.db_client.generate_connection_string(
            host=host,
            port=port,
            username=self.service_config.get(f"{section_name}.username"),
            password=self.service_config.get(f"{section_name}.password"),
            database=self.service_config.get(f"{section_name}.database"),
            pool_recycle=self.service_config.get(f"{section_name}.pool_recycle"),
            charset=self.service_config.get(f"{section_name}.charset"),
            role=role,
        )
        self.db_client.configure_database(
            connect_string=conn_string, role=role, pool_size=pool_size + 1
        )

    def configure(self, db_pool_size: int = 1):
        """
        run configurations for sql client and statsd
        """

        self.configure_db(
            role="take2_primary",
            section_name="master_take2_mysql",
            pool_size=db_pool_size,
        )
        self.configure_db(
            role="take2_replica",
            section_name="slave_take2_mysql",
            pool_size=db_pool_size,
        )
        self.configure_db(
            role="stock_primary",
            section_name="master_stock_mysql",
            pool_size=db_pool_size,
        )
        self.configure_db(
            role="stock_replica",
            section_name="slave_stock_mysql",
            pool_size=db_pool_size,
        )
        self.configure_db(
            role="master", section_name="master_take2_mysql", pool_size=db_pool_size
        )
        self.configure_db(
            role="slave", section_name="slave_take2_mysql", pool_size=db_pool_size
        )
        self.configure_db(
            role="stock.leader",
            section_name="master_stock_mysql",
            pool_size=db_pool_size,
        )
        self.configure_db(
            role="stock.follower",
            section_name="slave_stock_mysql",
            pool_size=db_pool_size,
        )

        # Configure Sentry
        release = f"stock-service@{self.version}"

        dsn = self.service_config.get("sentry.dsn")
        sentry_logging = LoggingIntegration(
            level=logging.INFO
        )  # Capture info and above as breadcrumbs
        sentry_sdk.init(
            dsn=dsn,
            release=release,
            integrations=[sentry_logging],
            ignore_errors=[ServiceError],
        )

    def configure_kafka(self):
        """
        configures the kafka producer singleton
        """
        producer = Producer()
        hosts = self.find_service(self.service_config.get_str("kafka.srv_name"))
        try:
            producer.configure(",".join(hosts))
        except TypeError:
            self.logger.info("kafka producer already configured")

    @cached_property
    def kafka_brokers(self):
        return ",".join(
            self.find_service(self.service_config.get_str("kafka.srv_name"))
        )

    @cached_property
    def kafka_schema_producer(self):
        producer = Producer()
        try:
            producer.configure(self.kafka_brokers)
        except TypeError:
            self.logger.info("kafka producer already configured")
        return SchemaProducer

    def get_s4f_service(self, service_name: str):
        """
        returns client parameters for s4f client
        """
        host, port = self.resolve(service_name)
        client_params = dict(endpoints=[f"{host}:{port}"])
        send_timeout = self.service_config.get(f"{service_name}.send_timeout")
        recv_timeout = self.service_config.get(f"{service_name}.recv_timeout")
        if send_timeout:
            client_params["send_timeout"] = int(send_timeout)
        if recv_timeout:
            client_params["recv_timeout"] = int(recv_timeout)
        return client_params

    @cached_property
    def memcached_client(self):
        client = cache_client.memcached.MemcachedClient()
        config = self.find_service(
            self.service_config.get_str("general_cache.srv_name")
        )
        client.configure(
            config,
            namespace=self.SERVICE_NAME,
            socket_timeout=int(os.environ.get("CACHING_SOCKET_TIMEOUT", 3)),
            dead_retry=int(os.environ.get("CACHING_DEAD_RETRY", 0)),
        )
        return client

    @cached_property
    def ibt_prep_number_of_days(self):
        return os.environ.get("IBT_PREP_NUMBER_OF_DAYS") or 30

    @cached_property
    def log_stock_differences(self):
        return os.environ.get("LOG_STOCK_DIFFERENCES", "").lower() == "true"

    @cached_property
    def merchant_returns_service_client(self):
        config = self.get_s4f_service("merchant_returns_service")
        client = MerchantReturnsServiceClient(**config)
        return client

    @cached_property
    def merchant_offer_client(self):
        service = self.get_s4f_service("s4f_merchant_offer_service")
        client = MerchantOfferServiceClient(**service)
        return client


# Deprecate everything below.
#######################################################################

DEFAULTS = {
    "SERVICE_NAME": "stock-service",
    "CONFIG_DIR": pathlib.Path("stock_service/config"),
    "ENV": os.environ.get("ENVIRONMENT", "test"),
}

LOGGING_FORMAT = (
    "%(asctime)s %(levelname)s %(threadName)s %(filename)s:%(lineno)s %(message)s"
)
LOG_LEVEL = logging.INFO


def get_version():
    project_root = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(project_root)
    return open(base_dir + "/version", "rt").read().strip()


class ServiceConfigError(Exception):
    """
    raised when an invalid configuration is encountered
    """


class OldConfig:
    """Singleton that returns a configured instance of the config"""

    _instance = None
    _lock = threading.Lock()
    _service_config: ServiceConfig = None
    _dbclient: SQLClient = SQLClient()
    _statsd: StatsClient = StatsClient()
    logging.basicConfig(level=LOG_LEVEL, format=LOGGING_FORMAT, stream=sys.stdout)
    logger = logging.getLogger(__file__)

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(OldConfig, cls).__new__(cls)
                cls._instance._service_config = cls._instance.create_service_config()
        return cls._instance

    @classmethod
    def get_stats_client(cls):
        return cls._statsd

    @classmethod
    def get_db_client(cls):
        return cls._dbclient

    @classmethod
    def resolve(cls, service_name: str) -> tuple:
        """
        resolves dns host ip and port for the specified service using ServiceConfig

        :param service_name: name of the service, i.e statsd, master_database, ...
        :return: tuple (host, port)
        """
        service_key = cls._instance._service_config.get(f"{service_name}.srv_name")
        if not service_key:  # check if .ini has .srv_name
            raise ServiceConfigError("{} does not have 'srv_name'".format(service_name))
        host, port = cls._instance._service_config.find_service(
            service_key, format=FORMAT_LIST_OF_TUPLE
        )[0]
        return host, port

    @classmethod
    def find_service(cls, srv_name: str, format=None) -> list:
        """
        returns host ip and port of srv record
        """
        return cls._instance._service_config.find_service(srv_name)

    @classmethod
    def configure_statsd(cls, statsd: StatsClient):
        """
        configures StatsClient for stock-service

        :param statsd: StatsClient object
        """

        if statsd.is_configured():
            OldConfig.logger.warning("statsd client already configured")

        host, port = cls._instance.resolve("statsd")
        statsd.configure_for_service(
            os.environ.get("STATSD_NAMESPACE"), host, port, include_fqdn=False
        )

    @classmethod
    def configure_db(cls, role: str, section_name: str, pool_size: int):
        """
        configures sql client DB connection using {role} as reference. The default configured roles are
        "master" and "slave"

        :param role: name of the connection
        :param section_name: section name in the .ini. example: "[slave_database]" in config/test.ini
        :param pool_size: sqlalchemy pool_size, this should the equals the number of threads / workers
        """

        if role in cls._dbclient.databases:
            OldConfig.logger.warning("database role '%s' already configured", role)

        try:
            host, port = cls.resolve(section_name)
        except ServiceConfigError:
            host = cls._instance._service_config.get(f"{section_name}.host")
            port = int(cls._instance._service_config.get(f"{section_name}.port"))

        conn_string = cls._dbclient.generate_connection_string(
            host=host,
            port=port,
            username=cls._instance._service_config.get(f"{section_name}.username"),
            password=cls._instance._service_config.get(f"{section_name}.password"),
            database=cls._instance._service_config.get(f"{section_name}.database"),
            pool_recycle=cls._instance._service_config.get(
                f"{section_name}.pool_recycle"
            ),
            charset=cls._instance._service_config.get(f"{section_name}.charset"),
            role=role,
        )
        cls._dbclient.configure_database(
            connect_string=conn_string, role=role, pool_size=pool_size + 1
        )

    @classmethod
    def configure(cls, db_pool_size: int = 1):
        """
        run configurations for sql client and statsd
        """
        cls._instance._service_config = cls.create_service_config()

        cls.configure_db(
            role="take2_primary",
            section_name="master_take2_mysql",
            pool_size=db_pool_size,
        )
        cls.configure_db(
            role="take2_replica",
            section_name="slave_take2_mysql",
            pool_size=db_pool_size,
        )
        cls.configure_db(
            role="stock_primary",
            section_name="master_stock_mysql",
            pool_size=db_pool_size,
        )
        cls.configure_db(
            role="stock_replica",
            section_name="slave_stock_mysql",
            pool_size=db_pool_size,
        )
        cls.configure_db(
            role="master", section_name="master_take2_mysql", pool_size=db_pool_size
        )
        cls.configure_db(
            role="slave", section_name="slave_take2_mysql", pool_size=db_pool_size
        )
        cls.configure_db(
            role="stock.leader",
            section_name="master_stock_mysql",
            pool_size=db_pool_size,
        )
        cls.configure_db(
            role="stock.follower",
            section_name="slave_stock_mysql",
            pool_size=db_pool_size,
        )

        cls.configure_db(
            role="take2_primary",
            section_name="master_take2_mysql",
            pool_size=db_pool_size,
        )
        cls.configure_db(
            role="take2_replica",
            section_name="slave_take2_mysql",
            pool_size=db_pool_size,
        )
        cls.configure_db(
            role="stock_primary",
            section_name="master_stock_mysql",
            pool_size=db_pool_size,
        )
        cls.configure_db(
            role="stock_replica",
            section_name="slave_stock_mysql",
            pool_size=db_pool_size,
        )

        cls.configure_statsd(statsd=cls._statsd)

        # Configure Sentry
        release = "stock-service@" + get_version()

        dsn = cls._instance._service_config.get("sentry.dsn")
        sentry_logging = LoggingIntegration(
            level=logging.INFO
        )  # Capture info and above as breadcrumbs
        sentry_sdk.init(
            dsn=dsn,
            release=release,
            integrations=[sentry_logging],
            ignore_errors=[ServiceError],
        )

    @classmethod
    def create_service_config(cls) -> ServiceConfig:
        env = DEFAULTS["ENV"]
        file = DEFAULTS["CONFIG_DIR"] / "{}.ini".format(env)
        cls.logger.info("Loading configuration %s with ENVIRONMENT=%s", file, env)
        return ServiceConfig(ini_files=[file])

    @classmethod
    def configure_in_memory_database(cls):
        cls._dbclient.configure_database(connect_string="sqlite://", role="master")
        cls._dbclient.configure_database(connect_string="sqlite://", role="slave")
        cls._instance.configure_statsd(statsd=cls._statsd)

    @classmethod
    def get_memcache_config(cls):
        return cls._instance._service_config.find_service(
            cls._instance._service_config.get("general_cache.srv_name")
        )

    @staticmethod
    def monitor_stats(stats: StatsClient, count_errors=True, count_success=True):
        """
        decorator to profile function and count the errors and success
        decorator to catch exception as increment statsd reporting
        """

        def inner(func):
            def handler(*args, **kwargs):
                timer = stats.timer(f"{func.__name__}.timer")
                timer.start()
                try:
                    results = func(*args, **kwargs)
                except Exception as e:
                    if count_errors:
                        stats.incr(f"{func.__name__}.fail.{e.__class__.__name__}")
                    raise
                finally:
                    timer.stop()
                if count_success:
                    stats.incr(f"{func.__name__}.success")
                return results

            return handler

        return inner

    @classmethod
    def get_s4f_service(cls, service_name: str):
        """
        returns client parameters for s4f client
        """
        host, port = cls.resolve(service_name)
        client_params = dict(endpoints=[f"{host}:{port}"])
        send_timeout = cls._instance._service_config.get(f"{service_name}.send_timeout")
        recv_timeout = cls._instance._service_config.get(f"{service_name}.recv_timeout")
        if send_timeout:
            client_params["send_timeout"] = int(send_timeout)
        if recv_timeout:
            client_params["recv_timeout"] = int(recv_timeout)
        return client_params

    @classmethod
    def get(cls, key):
        """
        provides access to config parameters
        usage example:
            >>> config = OldConfig()
            >>> srv_name = config.get('kafka.srv_name')
        """
        return cls._instance._service_config.get_str(key)
