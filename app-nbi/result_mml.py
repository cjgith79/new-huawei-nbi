#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

class ResultMML(object):
    """docstring for ResultMML"""
    pattern_command = re.compile('MML Command-----(.*);')
    pattern_network_element = re.compile('NE : (.*)')
    pattern_executed_time_stamp = re.compile(
        '(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})')
    pattern_o_m_id = re.compile('O&M    #(.*)')
    pattern_retcode = re.compile('RETCODE =(.*)  ')
    pattern_result = re.compile('RETCODE = 0  Operation succeeded(.*)')

    def __init__(self, command):
        super(ResultMML, self).__init__()
        self.command = command
        self.network_element = None
        self.executed_time_stamp = None
        self.o_m_id = None
        self.retcode = None
        self.result = None

    def command_search(self, line):
        match = ResultMML.pattern_command.search(line)
        if match:
            return match.group(1)
        return False

    def network_element_search(self, line):
        if not self.network_element:
            match = ResultMML.pattern_network_element.search(line)
            if match:
                self.network_element = match.group(1)

    def executed_time_stamp_search(self, line):
        if not self.executed_time_stamp:
            match = ResultMML.pattern_executed_time_stamp.search(line)
            if match:
                self.executed_time_stamp = match.group(1)

    def o_m_id_search(self, line):
        if not self.o_m_id:
            match = ResultMML.pattern_o_m_id.search(line)
            if match:
                self.o_m_id = match.group(1)

    def retcode_search(self, line):
        if not self.retcode:
            match = ResultMML.pattern_retcode.search(line)
            if match:
                self.retcode = match.group(1)

    def result_search(self, line):
        if not self.result:
            match = ResultMML.pattern_result.search(line)
            if match:
                self.result = True
            else:
                self.result = False

    def fields_search(self, line):
        self.network_element_search(line)
        self.executed_time_stamp_search(line)
        self.o_m_id_search(line)
        self.retcode_search(line)
        self.result_search(line)

    def __str__(self):
        message = (
                f"command[{self.command}]\n"
                f"network_element[{self.network_element}]\n"
                f"executed_time_stamp[{self.executed_time_stamp}]\n"
                f"o_m_id[{self.o_m_id}]\n"
                f"retcode[{self.retcode}]\n"
                f"result[{self.result}]\n"
            )
        return message
