from socket import *
from os import listdir

class Tcp:
    def __init__(self, listen, port = None):
        self.port = port
        self.control = socket(AF_INET, SOCK_STREAM)
        if listen > 0 and port != None:
            self.control.bind(('', self.port))
            self.listen(listen)
        self.control.settimeout(5.0)
        self.client, self.address = None, None

        self.report = 'FINISH'

    def conectar(self):
        self.client, self.address = self.control.accept()

    def receber(self): # São vários clients
        if self.client != None:
            try:
                mensagem = self.client.recv(2048).decode()
            except:
                mensagem = None
        else: mensagem = None
        return mensagem

    def responder(self, mensagem, endereco):
        if self.client != None:
            try:
                self.client.send(mensagem.encode())
                resultado = 'FINISH'
            except:
                resultado = 'FAIL'
        else: resultado = "FAIL"
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
