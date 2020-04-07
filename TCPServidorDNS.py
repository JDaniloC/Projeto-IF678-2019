from socket import *

from Utils.UDP import Udp

dic = {}
server = Udp('server', 54000)
print("Server preparado para receber.\n")
while True:
    print("Procurando solicitação...")
    message, ip, port = server.receber()
    if message != None:
        mensagem = message.split()
        if mensagem[0] == "SignIn":
            print("Cadastrando servidor...")
            nome, ip, porta = mensagem[1].split(":")
            dic[nome] = ip + ":" + porta
            print(dic)
        else:
            print("Enviando servidor...")
            if mensagem[1] not in dic:
                dic[mensagem[1]] = 'NULL'
            server.responder(dic[mensagem[1]], (ip, port))
        
