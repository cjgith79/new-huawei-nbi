#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys

# from conf import ROOT_DIR
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

def validate_extension(extension=None):
    if not extension:
        return None

    if extension in ['mml', 'txt']:
        return extension

def u2020_process_file(file_name=None):
    if not file_name:
        return None

    extension = validate_extension(file_name.split(".")[-1])
    if not extension:
        print("Valid file extensions: .mml")
        sys.exit()

    createfolder(pathLocalUp)
    createfolder(pathLocalDl)

    ftp = GestorFTP(cred=FTP_PM_CRED,
        pLu=pathLocalUp, pRu=pathRemotoUp,
        pld=pathLocalDl, pRd=pathRemotoDl)
    print(f"ftp[{ftp}]", flush=True)

    telnet = ConectorTelnet(dat=CRED_U2020)
    print(f"telnet[{telnet}]", flush=True)

    # Vía ftp depositar archivo en U2020 folder
    ftp.enviar(file_name)

    # Enviar telnet a U2020
    telnet.conecta()
    telnet.ejecuta_scritp(file_name)
    telnet.desconecta()

    # Esperar aparición de archivo de resultados
    # Traer archivo de resultados
    ftp.extraer(file_name[:-4])
    print('Extrayendo el archivo:', file_name[:-4])

if __name__ == '__main__':
    '''
    Uso: python app.py [-h] input
    '''

    parser = argparse.ArgumentParser(description='File to process')
    parser.add_argument('input', type=str, help='Input file')
    args = parser.parse_args()

    # print(f"ROOT_DIR[{ROOT_DIR}]")

    u2020_process_file(file_name=args.input)
