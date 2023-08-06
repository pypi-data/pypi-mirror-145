
from logging import StreamHandler
from kafka import KafkaProducer
import json
from datetime import datetime
import graphyte
import consul
from jsonformatter import JsonFormatter
from cloudevents.sdk.event import v03
import os
import logging
import uuid
from datetime import datetime
import functools
import time
from inspect import getmembers,isfunction,ismethod
import sys


class ApplicationConfigurator():

    def get(self,config_key):
        config = {}
        try:
            c = consul.Consul(host=os.environ['CONSUL_HOST'], port=os.environ['CONSUL_PORT'])
            index = None
            index, data = c.kv.get(config_key, index=None)
            the_json = data['Value'].decode("utf-8")
            config = json.loads(the_json)
        except Exception as ex:
            print('Exception in getting key')
            print(ex)

        return config

    def put(self,config_key, config_value):
        config = {}
        try:
            c = consul.Consul(host=os.environ['CONSUL_HOST'], port=os.environ['CONSUL_PORT'])
            index = None
            c.kv.put(config_key, config_value)
        except Exception as ex:
            print('Exception in getting key')
            print(ex)

        return config


class KafkaConfig(object):
    def __init__(self, kafka_brokers, json=False):
        self.json = json
        if not json:
            self.producer = KafkaProducer(
                bootstrap_servers=kafka_brokers
            )
        else:
            self.producer = KafkaProducer(
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                bootstrap_servers=kafka_brokers
            )
    def send(self, data, topic):
        if self.json:
            result = self.producer.send(topic, key=b'log', value=data)
        else:
            result = self.producer.send(topic, bytes(data, 'utf-8'))
        print("kafka send result: {}".format(result.get()))


class FerrisKafkaLoggingHandler(StreamHandler):

    def __init__(self,topic='ferris.logs'):
        StreamHandler.__init__(self)
        environment = ApplicationConfigurator().get('ferris.env')
        broker_url = f"{environment['KAFKA_BOOTSTRAP_SERVER']}:{environment['KAFKA_PORT']}"
        self.topic = topic
        # Kafka Broker Configuration
        self.kafka_broker = KafkaConfig(broker_url)

    def emit(self, record):
        msg = self.format(record)
        self.kafka_broker.send(msg, self.topic)


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

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)



class MetricsAPI:


    def __init__(self, topic='ferris.metrics'):
        self.topic = topic
        # Kafka Broker Configuration
        self.kafka_broker = KafkaConfig(broker_url)
        print('metrics init called')

    def send(self,metric_message:MetricMessage):
        try:
            self.kafka_broker.send(metric_message.toJSON(), self.topic)
        except Exception as ex:
            print('Exception in publishing message')
            print(ex)



class Notification(object):
    def __init__(self, from_addr, to_addr, subject, message_content):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.subject = subject
        self.message_content = message_content   
        if update_time == None:
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%Y-%m-%dT%H:%M:%SZ")
            self.update_time = timestampStr
        else:
            self.update_time = update_time

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class NotificatonsAPI():
    def __init__(self, topic='ferris.notifications'):
        self.topic = topic
        # Kafka Broker Configuration
        self.kafka_broker = KafkaConfig(broker_url)
    def send(self, notification:Notification):
        try:
            self.kafka_broker.send(notification.toJSON(), self.topic)
        except Exception as ex:
            print('Exception in publishing message')
            print(ex)


class CloudEventsAPI():

    def __init__(self, topic='ferris.events'):
        self.topic = topic
        # Kafka Broker Configuration
        self.kafka_broker = KafkaConfig(broker_url)
    def send(self, event):
        event.SetEventID(uuid.uuid1().hex)
        date_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

      
        event.SetEventTime(date_time)
        s = json.dumps(event.Properties())
        self.kafka_broker.send(s, self.topic)


# Modified version of Execution-Time (pip)

class ExecutionTime:

    def __init__(self,console=False,module_name=None):
         
        self.module_name = module_name
        self.logtime_data = {}

        if self.module_name is not None:
            self.auto_decorate()
    
    def timeit(self,method):
        @functools.wraps(method)
        def wrapper(*args,**kwargs):
            start_time = time.perf_counter()
            result = method(*args,**kwargs)
            end_time = time.perf_counter()
            current_time = round((end_time-start_time)*1000,4)
            total_time = round((end_time-start_time)*1000,4) # time in milliseconds 
            
            if method.__name__ in self.logtime_data:
                curr = self.logtime_data[method.__name__] 
                tt = curr["total_time"]+total_time
                count = curr["times_called"]+1
                avg_time=round(tt/count,4) 
                self.logtime_data[method.__name__]={'times_called':count,"total_time":tt,"average_time":avg_time,"current_time":current_time}
            else:
                self.logtime_data[method.__name__]={'times_called':1,"total_time":total_time,"average_time":total_time,"current_time":current_time}

        return wrapper
     
    def auto_decorate(self):
        try:
            module = sys.modules[self.module_name]
            items = getmembers(module,isfunction)
            for name,addr in items:
                setattr(module,name,self.timeit(addr))
        except KeyError as e:
            raise f'Error Occured, No module by name {module_name}. If you think this was a mistake than raise issue at {self.issue_url}'

environment = ApplicationConfigurator().get('ferris.env')
broker_url = f"{environment['KAFKA_BOOTSTRAP_SERVER']}:{environment['KAFKA_PORT']}"
