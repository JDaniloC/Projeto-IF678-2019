from socket import *
from time import sleep
from os import listdir


class Client:
    def __init__(self):
        self.client = socket(AF_INET, SOCK_DGRAM)
        
    def enviarPasta(self, pasta, destino):
        try:
            nomes = listdir(pasta)
            for arquivo in nomes:
                print(f"Enviando {arquivo}")
                self.enviarArquivo(pasta+"/"+arquivo, destino)
        except:
            print("Não foi possível abrir esta pasta!")

    def enviarArquivo(self, path, destino):
        self.tentativa = 0
        try:
            arquivo = open(path, 'rb')
            try:
                self.request(destino, "FILE "+path.split("/")[1])
                parte = arquivo.read(1024)
                while parte:
                    ack = self.enviar(destino, parte)
                    if ack != "FAIL":
                        self.tentativa = 0
                        print(f"Ele recebeu: {str(ack.decode())} parte")
                        parte = arquivo.read(2048)
                    else:
                        self.tentativa += 1
                        if self.tentativa == 3:
                            break
                self.request(destino, "CLOSE CONN")
            except:
                print("Não foi possível enviar o arquivo!")
        except:
            print("Não foi possível abrir este arquivo!")
                    
    def enviar(self, destino, mensagem):
        print("Tentando enviar mensagem...")
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
            
    def request(self, destino, tipo):
        try:
            self.client.sendto(tipo.encode(), destino)
            return "SUCS"
        except:
            return "FAIL"

client = Client()
destino = ("192.168.0.110", 12000)
client.enviarPasta("envios", destino)
#client.enviar(destino, b"Teste")
