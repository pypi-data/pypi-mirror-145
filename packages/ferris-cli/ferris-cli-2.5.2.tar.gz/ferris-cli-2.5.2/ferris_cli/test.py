
import logging

from ferris_cli.ferris_cli import FerrisKafkaLoggingHandler
from jsonformatter import JsonFormatter

logger = logging.getLogger('kafka_logging')
kh = FerrisKafkaLoggingHandler()
kh.setLevel(logging.INFO)

STRING_FORMAT = '''{
"Levelname":       "levelname",
"Name":            "name",
"Asctime":         "asctime",
"Message":         "message"
}'''

formatter =  JsonFormatter(STRING_FORMAT)
kh.setFormatter(formatter)
logger.addHandler(kh)


logger.info('loading file') 
print('sent logs')

