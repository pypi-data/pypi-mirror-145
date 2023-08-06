import json
import logging
import consul
import os

LOGS_KEY = "ferris_cli.config"
DEFAULT_CONFIG = os.environ.get('DEFAULT_CONFIG', 'ferris.env')


class ApplicationConfigurator:

    @staticmethod
    def get(config_key=None):
        if not config_key:
            conf = {}

            config_key = os.environ.get("APP_NAME", None)

            if config_key:
                conf = Consul().get(config_key)

            env_conf = Consul().get(DEFAULT_CONFIG)

            env_conf.update(conf)
            env_conf.update(os.environ)

            return env_conf

        return Consul().get(config_key)

    @staticmethod
    def put(config_key, config_value):
        return Consul().put_item(config_key, config_value)


class Consul:

    def __init__(self, consul_host=None, constul_port=None):
        CONSUL_HOST = consul_host if consul_host else os.environ.get('CONSUL_HOST', None)
        CONSUL_PORT = constul_port if constul_port else os.environ.get('CONSUL_PORT', None)
        if CONSUL_HOST:
            self.client = consul.Consul(
                host=CONSUL_HOST,
                port=CONSUL_PORT
            )

    def get_all(self):
        data = {}
        try:
            index, data = self.client.kv.get('', index=None, recurse=True)

            return data
        except Exception as e:
            logging.getLogger(LOGS_KEY).exception(e)

        return data

    def get(self, config_key):
        data = {}

        try:
            index, data = self.client.kv.get(config_key, index=None)

            return json.loads(data['Value'].decode('UTF-8'))

        except Exception as e:
            logging.getLogger(LOGS_KEY).exception(e)

        return data

    def delete_item(self, key):
        try:
            self.client.kv.delete(key)

        except Exception as e:
            logging.getLogger(LOGS_KEY).exception(e)

        return

    def put_item(self, key, value):
        try:
            self.client.kv.put(key, value.replace("'", '"'))

        except Exception as e:
            logging.getLogger(LOGS_KEY).exception(e)

        return {key: value}


