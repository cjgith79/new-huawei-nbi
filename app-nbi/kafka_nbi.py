#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
from decouple import config
import json
from kafka import KafkaConsumer
from kafka import KafkaProducer
import os
import sys

from db_entry import db_entry
from conector_telnet import ConectorTelnet
from conf import (  FTP_PM_CRED,
                    CRED_U2020,
                    pathLocalUp,
                    pathRemotoUp,
                    pathLocalDl,
                    pathRemotoDl
                )
from gestor_ftp import GestorFTP
from utils import createfolder

ENV = config('ENV')

config_dict = configparser.ConfigParser()
config_dict.read('kafka.conf')
section = 'kafka_' + ENV

MML_TOPIC = config_dict[section]['mml_topic']
RST_TOPIC = config_dict[section]['rst_topic']
PARCIAL_EXECUTION = config_dict[section]['parcial_execution']
# MML_FOLDER_FILES = config_dict[section]['mml_files']

consumer = KafkaConsumer(
    MML_TOPIC,
    auto_offset_reset='latest', # where to start reading the messages at
    group_id='event-collector-group-1', # consumer group id
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')) # we deserialize our data from json
)

producer = KafkaProducer(
   value_serializer=lambda msg: json.dumps(msg).encode('utf-8'), # we serialize our data to json for efficent transfer
   bootstrap_servers=['localhost:9092'])

class Mml_event(object):
    """This class is made to facilitate the information flow"""
    def __init__(self):
        super(Mml_event, self).__init__()
        self.id_ = None
        self.datetime_ = None
        self.client_id = None
        self.script_id = None
        self.command_type = None # Note it's a list
        self.data = None # list of dictionaries

    def __str__(self):
        message = (
                f"\nid_[{self.id_}]\n"
                f"datetime_[{self.datetime_}]\n"
                f"client_id[{self.client_id}]\n"
                f"script_id[{self.script_id}]\n"
                f"command_type[{self.command_type}]\n"
                f"data[{self.data}]"
        )
        return message

    def is_valid(self):
        print(f"command_type[{self.command_type}]")

        command_list = self.data
        for dict_ in command_list:
            data_dict = dict_['data']
            token_ = data_dict['command'].split()[0]
            print(f"token_[{token_}]")
            if not token_ in self.command_type:
                return False

        return True

    def some_valid(self):
        print(f"command_type[{self.command_type}]")

        command_list = self.data
        for dict_ in command_list:
            data_dict = dict_['data']
            token_ = data_dict['command'].split()[0]
            print(f"token_[{token_}]")
            if token_ in self.command_type:
                return True

        return False

    def generate_mml_file(self, dir=os.getcwd()):
        # --------------------------
        # self.id_ = "HelloWorld" # It works
        # self.id_ = self.id_[:8] # It works
        # self.id_ = self.id_[:16] # It fails
        self.id_ = self.id_.split('-')[0] # It works
        # --------------------------
        path = f"{os.path.join(dir, self.id_)}.txt"
        print(f"path[{path}]")
        with open(path, 'w') as writer:
            command_list = self.data
            for dict_ in command_list:
                data_dict = dict_['data']
                token_ = data_dict['command'].split()[0]
                print(f"token_[{token_}]")
                if token_ in self.command_type:
                    writer.write(f" {data_dict['command']}")
                    writer.write("{"
                                f"{data_dict['network_element']}"
                                "}\n")
        return f"{self.id_}.txt"

def get_mml_event(message=None):
    if not message:
        print("**** No message")
        return None

    mml_event = Mml_event()

    print(f"id_[{message['id_']}]")
    mml_event.id_ = message['id_']
    print(f"datetime_[{message['datetime_']}]")
    mml_event.datetime_ = message['datetime_']
    print(f"type_[{message['type_']}]")
    print(f"client_id[{message['data']['client_id']}]")
    mml_event.client_id = message['data']['client_id']
    print(f"script_id[{message['data']['script_id']}]")
    mml_event.script_id = message['data']['script_id']
    print(f"command_type[{message['data']['command_type']}]")
    mml_event.command_type = message['data']['command_type']
    command_list = message['data']['command_list']
    mml_event.data = message['data']['command_list']

    for dict_ in command_list:
        print(f"\tindex[{dict_['index']}]")
        data_dict = dict_['data']
        print(f"\tcommand[{data_dict['command']}]")
        print(f"\tnetwork_element[{data_dict['network_element']}]")

    return mml_event

# def show_message(message=None):
#     if not message:
#         print("**** No message")
#         return

#     print(f"id_[{message['id_']}]")
#     print(f"datetime_[{message['datetime_']}]")
#     print(f"type_[{message['type_']}]")
#     print(f"client_id[{message['data']['client_id']}]")
#     print(f"script_id[{message['data']['script_id']}]")
#     print(f"command_type[{message['data']['command_type']}]")
#     command_list = message['data']['command_list']

#     for dict_ in command_list:
#         print(f"\tindex[{dict_['index']}]")
#         data_dict = dict_['data']
#         print(f"\tcommand[{data_dict['command']}]")
#         print(f"\tnetwork_element[{data_dict['network_element']}]")

def validate_extension(extension=None):
    if not extension:
        return None

    if extension in ['txt']:
        return extension

def consume_events():
    createfolder(pathLocalUp)
    createfolder(pathLocalDl)

    ftp = GestorFTP(cred=FTP_PM_CRED,
        pLu=pathLocalUp, pRu=pathRemotoUp,
        pld=pathLocalDl, pRd=pathRemotoDl)
    print(f"ftp[{ftp}]", flush=True)

    telnet = ConectorTelnet(dat=CRED_U2020)
    print(f"telnet[{telnet}]", flush=True)

    print("Previous m in consumer", flush=True)
    for m in consumer:
        print("After m in consumer", flush=True)
        print(m.value) # this works as expected
        # show_message(message=m.value)
        mml_event = get_mml_event(message=m.value)
        print('-' * 20)
        if mml_event:
            print(f"mml_event[{mml_event}]")
            print('-' * 20)
            # process_mml_event(mml_event=mml_event)
            if mml_event.some_valid():
                # Debo generar archivo de comandos
                # path = mml_event.generate_mml_file(dir=MML_FOLDER_FILES)
                # path = mml_event.generate_mml_file(dir=f"{MML_FOLDER_FILES}")
                path = mml_event.generate_mml_file(dir=pathLocalUp)
                # En base al archivo de comandos grabar en la BD
                # db_entry(file_path=path,client_id=mml_event.client_id,
                #    script_id=mml_event.script_id)
                pathLocalUp
                db_entry(file_path=os.path.join(pathLocalUp, path),client_id=mml_event.client_id,
                    script_id=mml_event.script_id)
                # Vía ftp depositar archivo en U2020 folder
                ftp.enviar(path)
                # Enviar telnet a U2020
                telnet.conecta()
                telnet.ejecuta_scritp(path)
                telnet.desconecta()
                # Esperar aparición de archivo de resultados
                # Traer archivo de resultados
                ftp.extraer(path[:-4])
                print('Extrayendo el archivo:', path[:-4])
                # Actualizar BD
                # Responder vía Kafka a cliente
                print("Previous producer.send()", flush=True)
                producer.send(RST_TOPIC, value=m.value)
                print("After producer.send()", flush=True)
                # Preguntas:
                # - qué hago con los archivos generados ?
                # Sugerencias:
                # - generar log de proceso
                pass
            else:
                # Responder vía Kafka a cliente
                pass


if __name__ == '__main__':
    consume_events()
