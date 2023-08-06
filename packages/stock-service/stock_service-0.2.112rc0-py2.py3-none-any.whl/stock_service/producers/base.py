from stock_service.config import Config
from tal_schema_registry.schema_registry import SchemaRegistry

config = Config()


class Producer(object):
    """
    kafka producer instance
    usage:
        >>> producer = Producer(topic='dummy_topic')
        >>> producer.send({"hello": "takealot"})
    """

    def __init__(self, topic: str):
        self.topic = topic
        self.schema_producer = config.kafka_schema_producer(
            source_service_name=config.service_config.get_str("kafka.srv_name"),
            topic=topic,
            schema_registry=SchemaRegistry(),
        )

    def send(self, payload: dict, type: str):
        self.schema_producer.send(payload, type)
        config.logger.info(
            "sent event to kafka topic=%s, event_type=%s, payload=%s",
            self.topic,
            type,
            payload,
        )
