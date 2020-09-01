#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys

from db import create_tables
from process_command_file import process_command_file
from process_result_file import process_result_file

def validate_extension(extension=None):
    if not extension:
        return None

    if extension in ['txt', 'rst']:
        return extension

def db_entry(file_path=None,client_id=None,script_id=None):
    if not file_path:
        return None

    extension = validate_extension(file_path.split(".")[-1])
    if not extension:
        print("Valid file extensions: .txt .rst")
        sys.exit()

    create_tables()

    if extension == 'txt':
        process_command_file(file_path=file_path,
            client_id=client_id,script_id=script_id)

    if extension == 'rst':
        process_result_file(file_path=file_path)


if __name__ == '__main__':
    '''
    Uso: python app.py [-h] input
    '''

    parser = argparse.ArgumentParser(description='File to process')
    parser.add_argument('input', type=str, help='Input file')
    args = parser.parse_args()

    # extension = validate_extension(args.input.split(".")[-1])
    # if not extension:
    #     print("Valid file extensions: .com .rst")
    #     sys.exit()

    # create_tables()

    # if extension == 'mml':
    #     process_command_file(file_path=args.input)

    # if extension == 'rst':
    #     process_result_file(file_path=args.input)

    db_entry(file_path=args.input,client_id='client_id',script_id='script_id')
