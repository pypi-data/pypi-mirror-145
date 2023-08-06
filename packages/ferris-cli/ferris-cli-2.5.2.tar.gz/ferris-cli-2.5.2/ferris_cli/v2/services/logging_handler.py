import logging
from logging import StreamHandler

from .config import ApplicationConfigurator, DEFAULT_CONFIG
from .broker import FerrisBroker
from logstash_formatter import LogstashFormatterV1

LOGS_KEY = "ferris_cli.logging"
DEFAULT_TOPIC = 'ferris.logs'


class FerrisKafkaLoggingHandler(StreamHandler):

    def __init__(self):
        super().__init__()

    def log(self, record, topic=None):

        if not topic:
            topic = ApplicationConfigurator.get(DEFAULT_CONFIG).get('DEFAULT_LOGS_TOPIC', DEFAULT_TOPIC)

        try:
            msg = self.format(record)
            resp = FerrisBroker.send(msg, topic)

            logging.getLogger(LOGS_KEY).info("Response from broker.send: %s ", str(resp))
        except Exception as e:
            logging.getLogger(LOGS_KEY).error("Error while sending logs:")
            logging.getLogger(LOGS_KEY).exception(e)

        return True


class FerrisLogging(FerrisKafkaLoggingHandler):

    def __init__(self):
        super().__init__()

        self.setFormatter(LogstashFormatterV1())

    # @property
    # @staticmethod
    # def formatter():
    #     return LogstashFormatterV1()