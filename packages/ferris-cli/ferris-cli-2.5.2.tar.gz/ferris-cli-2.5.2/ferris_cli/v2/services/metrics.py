import json
import logging
from datetime import datetime

from .broker import FerrisBroker
from .config import ApplicationConfigurator, DEFAULT_CONFIG

LOGS_KEY = "ferris_cli.metrics"
DEFAULT_TOPIC = 'ferris.metrics'


class MetricMessage(object):

    def __init__(self, metric_key, metric_value, update_time=None):
        self.metric_key = metric_key
        self.metric_value = metric_value

        if update_time == None:
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%Y-%m-%dT%H:%M:%SZ")
            self.update_time = timestampStr
        else:
            self.update_time = update_time

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)


class FerrisMetrics:

    @staticmethod
    def send(message: MetricMessage, topic=None):

        if not topic:
            topic = ApplicationConfigurator.get(DEFAULT_CONFIG).get('DEFAULT_METRICS_TOPIC', DEFAULT_TOPIC)

        try:
            resp = FerrisBroker().send(topic, message.to_json())

            logging.getLogger(LOGS_KEY).info("Response from broker.send: %s ", str(resp))
        except Exception as e:
            logging.getLogger(LOGS_KEY).error("Error while sending metric message:")
            logging.getLogger(LOGS_KEY).exception(e)


