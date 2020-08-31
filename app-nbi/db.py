#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
from datetime import datetime
from decouple import config
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    Index,
    ForeignKey,
    String,
    create_engine,
    and_
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from result_mml import ResultMML

ENV = config('ENV')
DB_STR_CONNECTION = None
ENGINE = None
BASE = declarative_base()
SESSION = None


def db_str_connection():
    global DB_STR_CONNECTION

    if DB_STR_CONNECTION:
        return

    section = 'mysql_' + ENV

    config_dict = configparser.ConfigParser()
    config_dict.read('mysql.conf')

    host = config_dict[section]['host']
    user = config_dict[section]['user']
    password = config_dict[section]['password']
    database = config_dict[section]['database']
    port = config_dict[section]['port']

    DB_STR_CONNECTION = ("mysql+mysqlconnector:"
                f"//{user}:{password}@{host}:{port}/{database}")

class File(BASE):
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True) # Auto-increment should be default
    name = Column(String(250), nullable=False)
    received = Column(DateTime)
    client_id = Column(String(250), nullable=False)
    script_id = Column(String(250), nullable=False)
    __table_args__ = (Index('my_index', "name"), )

    def __repr__(self):
        return (f"File(id[{self.id}], "
                f"name[{self.name}], "
                f"received[{self.received}])",
                f"client_id[{self.client_id}])",
                f"script_id[{self.script_id}])"
                )

class Result(BASE):
    __tablename__ = 'result'
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('file.id'))
    file = relationship(File)
    executed_time_stamp = Column(DateTime)
    command = Column(String(256), nullable=False)
    network_element = Column(String(64), nullable=False)
    o_m_id = Column(String(64))
    retcode = Column(String(32))
    result = Column(Boolean)
    __table_args__ = (Index('my_index', "command", "network_element"), )

    def __repr__(self):
        return (f"Result(id[{self.id}], "
                f"file_id[{self.file_id}], "
                f"executed_time_stamp[{self.executed_time_stamp}], "
                f"command[{self.command}], "
                f"network_element[{self.network_element}], "
                f"o_m_id[{self.o_m_id}], "
                f"retcode[{self.retcode}], "
                f"result[{self.result}])")

def create_session_wrap():
    global SESSION

    if SESSION:
        return

    create_engine_wrap()
    DBSession = sessionmaker(bind=ENGINE)
    SESSION = DBSession()

def create_engine_wrap():
    global ENGINE

    if ENGINE:
        return

    db_str_connection()
    ENGINE = create_engine(DB_STR_CONNECTION)

def create_tables():
    create_engine_wrap()

    # Create all tables in the engine.
    BASE.metadata.create_all(ENGINE)

def save_file(file_name=None,received=None,client_id=None,script_id=None):

    # print(f"file_name[{file_name}] command[{command}] received[{received}] network_element[{network_element}]")

    new_file = File(name=file_name,received=received,
                client_id=client_id,script_id=script_id)
    SESSION.add(new_file)
    SESSION.commit()

    return new_file

def save_command(file=None,command=None,network_element=None):

    # print(f"file_name[{file_name}] command[{command}] received[{received}] network_element[{network_element}]")

    new_result = Result(command=command,
                    network_element=network_element,file=file)
    SESSION.add(new_result)
    SESSION.commit()

def save_result(result_mml=None):

    if not result_mml:
        return

    # print(result_mml)

    our_result = SESSION.query(Result).\
        filter(Result.command==result_mml.command).\
        filter(Result.network_element==result_mml.network_element).first()

    if not our_result:
        print("**** save_result: No hubo matching.")
        print(result_mml)
        return

    if result_mml.executed_time_stamp:
        our_result.executed_time_stamp = datetime.strptime(
            result_mml.executed_time_stamp, '%Y-%m-%d %H:%M:%S')

    if result_mml.o_m_id:
        our_result.o_m_id = result_mml.o_m_id

    if result_mml.retcode:
        our_result.retcode = result_mml.retcode

    our_result.result = result_mml.result

    # print(our_result)
    SESSION.add(our_result)
    SESSION.commit()
