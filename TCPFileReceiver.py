from socket import *
from Transporte.UDP import Udp

class Receiver:
    def __init__(self, ip, port):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.connect((ip, port))
        print("Servidor conectado.")

    def enviar(self, mensagem):
        self.client.send(mensagem.encode())

    def receber(self):
        return self.client.recv(2048).decode()

    def receberArquivo(self, nome):
        nome = nome.split('/')[-1]
        arquivo = open(nome, "wb")
        parte = self.client.recv(2048)
        self.enviar("ACK")
        while parte != b"CLOSE CONN" and parte != b"ERRO FILE":
            arquivo.write(parte)
            parte = self.client.recv(2048)
            self.enviar("ACK")
        if parte != b"ERRO FILE":
            print("Arquivo recebido com sucesso!")
        else:
            print("Aconteceu um erro.")
        arquivo.close()
        self.enviar("ACK")
        
    def fecharConexao(self):
        self.client.close()

name = '127.0.0.1'
port = 54000
dns = Udp('')
message = "GET " + input("Nome do servidor: ")
dns.responder(message, (name, port))
name, ip, port = dns.receber()
dns.control.close()

serverIp, serverPort = name.split(":")
control = Receiver(serverIp, int(serverPort))
verificador = True
while verificador:
    comando = input("Digite o comando:")
    if len(comando.split()) == 2:
        requisicao, complemento = comando.split()
    else:
        requisicao = "NONE"
    if requisicao.upper() == "FILE":
        print("Requisitando arquivo.")
        control.enviar("FILE "+complemento)
        mensagem = control.receber().split()[1].split("/")[-1]
        control.enviar("ACK")
        control.receberArquivo(mensagem)
    elif requisicao.upper() == "CLOSE":
        print("Fechando...")
        control.enviar("CLOSE CONN")
        verificador = False
    else:
        print(f"Não entendi o comando {requisicao}")
    
