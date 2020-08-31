# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "rjsilvia"
__date__ = "$13-04-2020 14:14:48$"
import sys
import telnetlib

def iflog(log, msg):
    if log:
        log.info(msg)
    else:
        print(msg) 

class ConectorTelnet:
    
    def __init__(self, dat, log=None):
        self.ip = dat['ip']
        self.port = dat['port']
        self.user = dat['user']
        self.passw = dat['password']
        self.log = log
        #print("-- inicializado datos para telnet --")
        iflog(self.log, "-- inicializado datos para telnet --")

    def encmsg(self, string):
        print('++ Codificando ++')
        return (string+'\r\n').encode('ascii')
    
    def read_until_decode(self):
        return self.tn.read_until(self.encmsg('---    END')).decode('ascii')

    def conecta(self):
        self.tn = telnetlib.Telnet(host=self.ip, port=self.port)
        #tn.set_debuglevel(debuglevel=3)
        self.tn.write(self.encmsg('LGI:OP="'+self.user+'", PWD="'+self.passw+'";'))
        #print(self.tn.read_until(self.encmsg('---    END')).decode('ascii'))
        iflog(self.log, self.read_until_decode())

    def envia_comando(self, comando):
        self.tn.write(self.encmsg(comando))
        #print(self.tn.read_until(self.encmsg('---    END')).decode('ascii'))
        iflog(self.log, self.read_until_decode())

    # archi => nombre del archivo en U2020
    def ejecuta_scritp(self, archi):
        self.tn.write(self.encmsg('S_ACTIVATE:FILE=' + archi + ';'))
        #print(self.tn.read_until(self.encmsg('---    END')).decode('ascii'))
        iflog(self.log, self.read_until_decode())

    def desconecta(self):
        self.tn.write(self.encmsg('LGO:OP="'+self.user+'";'))
        # print(self.tn.read_until(self.encmsg('---    END')).decode('ascii'))
        iflog(self.log, self.read_until_decode())
        self.tn.close()

    def __str__(self):
        return "Soy un gestor de telnet"

