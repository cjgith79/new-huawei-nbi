#!/usr/bin/env python
# -*- coding: utf-8 -*-

from configparser import ConfigParser
from datetime import datetime
import time
import uuid


class Event(object):

    def get_types():
        parser = ConfigParser()
        parser.read('event.conf')

        types = []
        section_name = 'types'
        if section_name in parser.sections():
            types = [name for name, value in parser.items(section_name)]
        return types

    types = get_types()

    def __init__(self,type_=None,data=None):
        super(Event, self).__init__()
        # UUID produces a universally unique identifier
        self.id_ = str(uuid.uuid4())
        self.datetime_ = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        self.type_ = type_
        self.is_valid_type_ = self.type_ in Event.types
        self.data = data

    def __str__(self):
        message = (
                f"\nid_[{self.id_}]\n"
                f"datetime_[{self.datetime_}]\n"
                f"type_[{self.type_}]\n"
                f"is_valid_type_[{self.is_valid_type_}]"
                f"data[{self.data}]"
        )
        return message

    def as_dictionary(self):
        return {
            'id_': self.id_,
            'datetime_': self.datetime_,
            'type_': self.type_,
            'data': self.data
        }


if __name__ == '__main__':
    while(True):
        event_ = Event(type_='mml_type')
        print(f'event_{event_}')
        print(f'types[{Event.types}]')
        print(f'as_dictionary[{event_.as_dictionary()}]')
        time.sleep(3)
