from ftplib import FTP

class GestorFTP:

    def __init__(self, cred, pLu='', pRu='', pld='', pRd='', log=None):

        self.ip = cred['ip']
        self.port = cred['port']
        self.user = cred['user']
        self.passw = cred['password']
        self.path_localDl = pld
        self.path_localUp = pLu
        self.path_remoto_up = pRu
        self.path_remoto_dl = pRd
        self.log = log
        # print("-- inicializado datos para ftp --")

    # archivo = nombre del archivo (.txt) Ej: myfile.txt
    def enviar(self, arch):
        print('*********************************Archivo a enviar por FTP '+arch)
        ftp = FTP(self.ip)
        ftp.login(self.user, self.passw)
        with open(self.path_localUp + arch, 'rb') as f:  #
            ftp.storlines('STOR %s' % self.path_remoto_up + arch, f)
        ftp.quit()
        print('** archivo enviado ftp **')

    def writeline(data):
        filedata.write(data)
        filedata.write(os.linesep)

    # Ej: arch_rem = 'remotefile07042020_20200407000000_rsilva_118.rst'
    def extraer(self, arch_rem):
        band = False
        ftp = FTP(self.ip)
        ftp.login(self.user, self.passw)
        ftp.cwd(self.path_remoto_dl)
        filelist=ftp.nlst()
        for file in filelist:
            fildir=file.split('.')
            filsize=len(fildir)
            if(filsize>1 and file.startswith(arch_rem) and file.endswith('rst')):
                ftp.retrbinary('RETR %s' %file, open(self.path_localDl + file, 'wb').write)
                band = True
                # ------------
                break
                # ------------

        # Extracción
        #filedata = open('resultados.txt', 'w')
        #ftp.retrlines('RETR ' + self.path_remoto_dl + arch_rem, writeline)
        #filedata.close()
        ftp.quit()
        print('** archivo obtenido ftp **')
        # return band
        return band, file

    def __str__(self):
        return "Soy un gestor de ftp"

