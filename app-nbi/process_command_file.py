#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import re

from db import save_file
from db import save_command
from db import create_tables
from db import create_session_wrap

def process_command_file(file_path=None,client_id=None,script_id=None):

    if not file_path:
        return

    file_name = os.path.basename(file_path)
    received = datetime.datetime.utcnow()

    # Debo capturar command y network_element de cada línea
    pattern_ = re.compile('(MOD  .*);{(.*)}')

    create_session_wrap()
    new_file = save_file(file_name=file_name,received=received,
                        client_id=client_id,script_id=script_id)
    with open(file_path) as fp:
        for line in fp:
            match = pattern_.search(line)
            if match:
                command = match.group(1)
                network_element = match.group(2)
                save_command(new_file,command,
                    network_element)
