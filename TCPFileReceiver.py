from socket import *

from Utils.UDP import Udp

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
while True:
    message = "GET " + input("Nome do servidor: ")
    dns.responder(message, (name, port))
    name, ip, port = dns.receber()
    if name != 'NULL':
        break
    else:
        print("Servidor não encontrado")
dns.control.close()

serverIp, serverPort = name.split(":")
control = Receiver(serverIp, int(serverPort))
verificador = True

print('''
Comandos:
file CAMINHODOARQUIVO
list all
close conn
''')

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
    elif requisicao.upper() == 'LIST':
        print("Pedindo arquivos.")
        control.enviar("LIST ALL")
        mensagem = control.receber()
        for i in mensagem.split('§'):
            print(i)
    elif requisicao.upper() == "CLOSE":
        print("Fechando...")
        control.enviar("CLOSE CONN")
        verificador = False
    else:
        print(f"Não entendi o comando {requisicao}")
    
