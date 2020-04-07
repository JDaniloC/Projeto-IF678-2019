from socket import *

class Server:
    def __init__(self):
        port = 12000
        self.server = socket(AF_INET, SOCK_DGRAM)
        self.server.bind(('', port))
        print("Preparado para receber!")

    def receber(self):
        message, address = self.server.recvfrom(2048)
        print("Recebi uma mensagem!")
        message = message.decode()
        if message.split()[0] == "FILE":
            self.receberArquivo(message.split()[1])
        else:
            print("Não era um arquivo D:")

    def receberArquivo(self, nome):
        ack = 0
        arquivo = open(nome, "wb")
        parte, address = self.server.recvfrom(2048)
        while parte != b"CLOSE CONN":
            arquivo.write(parte)
            ack += len(parte)
            mensagem = "ACK "+str(ack)
            self.server.sendto(mensagem.encode(), address)
            parte, address = self.server.recvfrom(2048)
        print("Arquivo recebido com sucesso!")
        arquivo.close()

server = Server()
while True:
    server.receber()
        
