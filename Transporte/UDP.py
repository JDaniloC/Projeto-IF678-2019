from socket import *
from os import listdir

class Udp:
    def __init__(self, opcao, port = None):
        self.port = port
        self.control = socket(AF_INET, SOCK_DGRAM)
        if opcao == 'server' and port != None:
            self.control.bind(('', self.port))
        self.control.settimeout(5.0)

        self.report = 'FINISH'

    def receber(self):
        try:
            mensagem, endereco = self.control.recvfrom(2048)
            mensagem = mensagem.decode()
        except:
            mensagem = None
            endereco = ('0', 0)
        return (mensagem, ) + endereco

    def responder(self, mensagem, endereco):
        try:
            self.control.sendto(mensagem.encode(), endereco)
            resultado = 'Successfull'
        except:
            resultado = 'Failed'
        return resultado
    
    def enviarPasta(self, pasta, destino):
        self.report = "FINISH"
        try:
            nomes = listdir(pasta)
            for arquivo in nomes:
                self.report += " " + arquivo
                self.enviarArquivo(pasta+"/"+arquivo, destino)
                if self.report.split()[0] != "FINISH":
                    break
        except:
            if self.report.split()[0] != "FAIL":
                self.report = "FAIL FOLDER"

    def enviarArquivo(self, path, destino):
        self.report = "FINISH"
        self.tentativa = 0
        try:
            arquivo = open(path, 'rb')
        except:
            self.report = "FAIL FILE"

        if self.report == "FINISH":
            try:
                self.responder("FILE "+path.split("/")[1], destino)
                parte = arquivo.read(1024)
                while parte:
                    ack = self.enviar(destino, parte)
                    if ack != "FAIL":
                        self.tentativa = 0
                        self.report = str(ack.decode())
                        parte = arquivo.read(2048)
                    else:
                        self.tentativa += 1
                        if self.tentativa == 3:
                            parte = False
                self.responder("CLOSE CONN", destino)
            except:
                self.report = "FAIL SEND"
            finally:
                arquivo.close()

    def enviar(self, destino, mensagem):
        try:
            self.client.sendto(mensagem, destino)
            try:
                mensagem, address = self.client.recvfrom(2048)
                resultado = mensagem
            except:
                resultado = "FAIL"
        except:
            resultado = "FAIL"
        return resultado

    def receberArquivo(self, nome):
        ack = 0
        arquivo = open(nome, "wb")
        try:
            parte, address = self.server.recvfrom(2048)
            try:
                while parte != b"CLOSE CONN":
                    arquivo.write(parte)
                    ack += len(parte)
                    mensagem = "ACK "+str(ack)
                    self.server.sendto(mensagem.encode(), address)
                    parte, address = self.server.recvfrom(2048)
                self.report = "FINISH"
            except:
                self.report = "FAIL SEND"
        except:
            self.report = "FAIL TIME" # Não é uma boa essa!!
        arquivo.close()

    def getReport(self): return self.report
