import configparser
from datetime import datetime
from decouple import config
import json
from kafka import KafkaProducer
from kafka import KafkaConsumer
import random
import time
import uuid

from event import Event

ENV = config('ENV')

producer = KafkaProducer(
   value_serializer=lambda msg: json.dumps(msg).encode('utf-8'), # we serialize our data to json for efficent transfer
   bootstrap_servers=['localhost:9092'])

config_dict = configparser.ConfigParser()
config_dict.read('kafka.conf')
section = 'kafka_' + ENV
MML_TOPIC = config_dict[section]['mml_topic']
RST_TOPIC = config_dict[section]['rst_topic']

consumer = KafkaConsumer(
    RST_TOPIC,
    auto_offset_reset='latest', # where to start reading the messages at
    group_id='event-collector-group-1', # consumer group id
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')) # we deserialize our data from json
)

config_dict.read('client.conf')
section = 'client_' + ENV
CLIENT_ID = config_dict[section]['client_id']

def _produce_mml_msg():
    data = {
        'client_id': CLIENT_ID,
        'script_id': 'script_id',
        'command_type': ['MOD', 'ADD', 'RMV', 'LST', 'DSP',],
        'command_list': [
            {'index': 0,
                'data': {   'command': 'MOD  EUTRANINTRAFREQNCELL:LOCALCELLID=5,MCC="730",MNC="09",ENODEBID=16698,CELLID=1,CELLINDIVIDUALOFFSET=dB0,CELLQOFFSET=dB0;',
                    'network_element': 'MBTS-VAL_3G_138'
                }
            },
            {'index': 1,
                'data': {   'command': 'MOD  EUTRANINTRAFREQNCELL:LOCALCELLID=1,MCC="730",MNC="09",ENODEBID=5115,CELLID=2,CELLINDIVIDUALOFFSET=dB0,CELLQOFFSET=dB0;',
                    'network_element': 'MBTS-VA0817'
                }
            },
        ]
    }
    return data

def send_events():
    while(True):
        print('-' * 20, flush=True)
        data = _produce_mml_msg()
        event_ = Event(type_='mml_type',data=data)
        id_ = event_.id_
        print(f"id_[{id_}]", flush=True)
        # print(f"as_dictionary[{event_.as_dictionary()}]")
        print("Previous producer.send()", flush=True)
        producer.send(MML_TOPIC, value=event_.as_dictionary())
        print("After producer.send()", flush=True)
        time.sleep(3) # simulate some processing logic
        print("Previous for m in consumer", flush=True)
        for m in consumer:
            print("After for m in consumer", flush=True)
            # print(m.value) # this works as expected
            print(f"id_[{m.value['id_']}]", flush=True)
            # break
            if id_  == m.value['id_']:
                print("*** match", flush=True)
                break
            else:
                print("continue", flush=True)
                continue



if __name__ == '__main__':
    send_events()
