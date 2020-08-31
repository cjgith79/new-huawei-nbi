#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import re

from db import save_result
from db import create_tables
from db import create_session_wrap

from result_mml import ResultMML

def process_result_file(file_path=None):

    if not file_path:
        return

    result_mml = ResultMML(None)
    create_session_wrap()
    with open(file_path) as fp:
        for line in fp:
            command_ = result_mml.command_search(line)
            if command_:
                if result_mml.command:
                    save_result(result_mml)
                result_mml = ResultMML(command_)
            result_mml.fields_search(line)

    if result_mml.command:
        save_result(result_mml)
