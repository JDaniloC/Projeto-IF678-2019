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

    def receber(self, bytes = None):
        tentativa = 0
        mensagem = None
        endereco = ('0', 0)
        while tentativa < 3 and mensagem == None:
            try:
                mensagem, endereco = self.control.recvfrom(2048)
                if bytes == None:
                    mensagem = mensagem.decode()
                    print(f"RECEBENDO MENSAGEM {mensagem}")
                    self.control.sendto(b"ACK 0", endereco)
                    print(f"ENVIANDO ACK 0")
                else:
                    resposta = "ACK " + str(bytes + len(mensagem))
                    print(f"RECEBENDO {resposta}")
                    self.control.sendto(resposta.encode(), endereco)
            except:
                tentativa += 1
        return (mensagem, ) + endereco

    def responder(self, mensagem, endereco, bytes = None):
        resultado = "FAIL"
        tentativa = 0
        while resultado == "FAIL" and tentativa < 3:
            try:
                if bytes == None:
                    print(f"ENVIANDO MENSAGEM {mensagem}")
                    self.control.sendto(mensagem.encode(), endereco)
                else:
                    print(f"ENVIANDO PARTE ARQUIVO")
                    self.control.sendto(mensagem, endereco)
                mensagem, address = self.control.recvfrom(2048)
                resultado, ack = mensagem.decode().split()
                print(f"RECEBENDO {resultado} {ack}")
                if resultado == "ACK" and endereco == address and (bytes == None or ack == bytes):
                    resultado = 'FINISH'
                else:
                    tentativa += 1
            except:
                tentativa += 1
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
        ack = 0
        try:
            arquivo = open(path, 'rb')
        except:
            self.report = "FAIL FILE"

        if self.report == "FINISH":
            try:
                parte = arquivo.read(2048)
                ack += len(parte)
                while parte:
                    ack = self.responder(parte, destino, str(ack))
                    if ack != "FAIL":
                        parte = arquivo.read(2048)
                    else:
                        parte = False
                        self.report = "FAIL SEND"
                self.responder("CLOSE CONN", destino)
            except:
                self.report = "FAIL SEND"
            finally:
                arquivo.close()

    def receberArquivo(self, nome):
        ack = 0
        arquivo = open(nome, "wb")
        try:
            parte, ip, port = self.receber(ack)
            while parte != b"CLOSE CONN":
                arquivo.write(parte)
                ack += len(parte)
                parte, ip, port = self.receber(ack)
            self.report = "FINISH"
        except:
            self.report = "FAIL SEND"

    def getReport(self): return self.report
