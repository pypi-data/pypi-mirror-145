import logging
import os
import json

from kafka import KafkaProducer

from .config import ApplicationConfigurator, DEFAULT_CONFIG

LOGS_KEY = "ferris_cli.broker"


class FerrisBroker:

    def __init__(self, host=None, port=None):
        self.host = host
        self.port = port

    def send(self, topic, data, is_json=True):
        resp = FerrisKafka(self.host, self.port, is_json).send(topic, data)

        return resp


class FerrisKafka:

    def __init__(self, host=None, port=None, is_json=True):
        conf = ApplicationConfigurator.get(DEFAULT_CONFIG)

        if host and port:
            broker_address = f"{host}:{port}"
        else:
            broker_address = f"{conf.get('KAFKA_BOOTSTRAP_SERVER')}:{conf.get('KAFKA_PORT')}"

        self._is_json = is_json

        value_serializer = None if not is_json else lambda x: json.dumps(x).encode('utf-8')

        self.producer = KafkaProducer(
            bootstrap_servers=broker_address,
            value_serializer=value_serializer
        )

    def send(self, topic, message):

        resp = self.producer.send(
            topic,
            message
        ).get()

        return resp
