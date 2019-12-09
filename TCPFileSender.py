from socket import *
from Transporte.UDP import Udp
from os import listdir

class Sender:
    def __init__(self, port):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind(("", port))
        self.server.listen(1)

    def conectar(self):
        print("\nProcurando usuário...")
        self.client, self.address = self.server.accept()
        print("Cliente conectado!")

    def receber(self):
        return self.client.recv(2048).decode()

    def enviarArquivo(self, path):
        try:
            arquivo = open(path, 'rb')
            mensagem = "FILE "+path
            self.client.send(mensagem.encode())
            self.receber()
            parte = arquivo.read(2048)
            while parte:
                self.client.send(parte)
                parte = arquivo.read(2048)
                self.receber()
            self.client.send(b"CLOSE CONN")
            self.receber()
        except:
            self.client.send(b"ERRO FILE")
            print("Não foi possível abrir este arquivo!")

    def fecharConexao(self):
        self.client.close()

meuIp = '127.0.0.1'
minhaPorta = '12000'
name = '127.0.0.1'
port = 54000
dns = Udp('')
message = "SignIn " + input("Nome do servidor: ") + ":" + meuIp + ":" + minhaPorta
dns.responder(message, (name, port))
dns.control.close()

port = int(minhaPorta)
control = Sender(port)
control.conectar()

verificador = True
while verificador:
    message = control.receber()
    if message.split()[0] == "FILE":
        print(f"Ele requisitou o arquivo {message.split()[1]}.")
        control.enviarArquivo(message.split()[1])
    elif message.split()[0] == "CLOSE":
        print("Fechando server.")
        control.fecharConexao()
        verificador = False
    else:
        print("Não entendi...")
