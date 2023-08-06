import json
import logging
from datetime import datetime

from .broker import FerrisBroker
from .config import ApplicationConfigurator, DEFAULT_CONFIG

LOGS_KEY = "ferris_cli.notifications"
DEFAULT_TOPIC = 'ferris.notifications'


class Notification:

    def __init__(self, from_addr, to_addr, subject, message_content):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.subject = subject
        self.message_content = message_content

        date_time = datetime.now()
        timestamp = date_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.update_time = timestamp

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class FerrisNotificatons:

    @staticmethod
    def send(notification: Notification, topic=None):

        if not topic:
            topic = ApplicationConfigurator.get(DEFAULT_CONFIG).get('DEFAULT_NOTIFICATIONS_TOPIC', DEFAULT_TOPIC)

        try:
            resp = FerrisBroker().send(topic, notification.to_json())

            logging.getLogger(LOGS_KEY).info("Response from broker.send: %s ", str(resp))
        except Exception as e:
            logging.getLogger(LOGS_KEY).error("Error while sending notification:")
            logging.getLogger(LOGS_KEY).exception(e)


