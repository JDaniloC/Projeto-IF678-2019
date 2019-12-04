from socket import *

class Udp:
    def __init__(self, opcao, ip, port):
        self.port = port
        self.control = socket(AF_INET, SOCK_DGRAM)
        if opcao == 'server':
            self.control.bind(('', self.port))
        self.control.settimeout(5.0)

    def recebe(self):
        try:
            mensagem, endereco = self.control.recvfrom(2048)
            mensagem = mensagem.decode()
        except:
            mensagem = None
            endereco = ('0', 0)
        return (mensagem, ) + endereco

    def responde(self, mensagem, endereco):
        resultado = ''
        try:
            self.control.sendto(mensagem.encode(), endereco)
            resultado = 'Successfull'
        except:
            resultado = 'Failed'
        return resultado