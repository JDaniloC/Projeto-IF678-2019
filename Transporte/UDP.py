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
            resultado = 'FINISH'
        except:
            resultado = 'FAIL'
        return resultado
    
    def enviarPasta(self, pasta, destino):
        self.report = "FINISH"
        try:
            nomes = listdir(pasta)
            for arquivo in nomes:
                self.responder("NAME "+pasta+"/"+arquivo, destino)
                self.enviarArquivo(pasta+"/"+arquivo, destino)
                if self.report.split()[0] != "FINISH":
                    break
        except:
            if self.report.split()[0] != "FAIL":
                self.report = "FAIL FOLDER"
        finally:
            self.responder("CLOSE CONN", destino)

    def enviarArquivo(self, path, destino):
        self.report = "FINISH"
        self.tentativa = 0
        try:
            arquivo = open(path, 'rb')
        except:
            self.report = "FAIL FILE"

        if self.report == "FINISH":
            try:
                parte = arquivo.read(2048)
                while parte:
                    ack = self.enviar(destino, parte)
                    if ack != "FAIL":
                        self.tentativa = 0
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
        resultado = "FINISH"
        try:
            self.control.sendto(mensagem, destino)
        except:
            resultado = "FAIL"

        if resultado == "FINISH":
            try:
                mensagem, address = self.control.recvfrom(2048)
                resultado = mensagem
            except:
                resultado = "FAIL"
        return resultado

    def receberArquivo(self, nome):
        ack = 0
        arquivo = open(nome, "wb")
        try:
            parte, address = self.control.recvfrom(2048)
        except:
            self.report = "FAIL TIME" # Não é uma boa essa!!
        
        if self.report != "FAIL TIME":
            try:
                while parte != b"CLOSE CONN":
                    arquivo.write(parte)
                    ack += len(parte)
                    mensagem = "ACK "+str(ack)
                    self.control.sendto(mensagem.encode(), address)
                    parte, address = self.control.recvfrom(2048)
                self.report = "FINISH"
            except:
                self.report = "FAIL SEND"

    def getReport(self): return self.report
