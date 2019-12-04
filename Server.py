from tkinter import *
from socket import *
from Objeto import Objeto
from Transporte.UDP import Udp

class Server(Objeto):
    def __init__(self):
        super().__init__("Server", "Azure", 19000)
        self.cor = "Azure"
        self.inicio()

    def main(self):
        self.limpa()
        self.janela.geometry("240x140+600+400")
        self.servidor = Udp("Server", self.ip, self.port)
        self.titulo = Label(self.frame, text = 'Informe o DNS', bg = self.cor)
        Label(self.frame, text = "Digite o Ip: ", bg = self.cor).grid(row = 1, pady = 2)
        Label(self.frame, text = "Digite a porta:", bg = self.cor).grid(row = 2, pady = 2)
        Label(self.frame, text = "Digite o nome:", bg = self.cor).grid(row = 3, pady = 2)
        
        self.entrada1 = Entry(self.frame, width = 15)
        self.entrada1.insert(0, "127.0.0.1")
        self.entrada2 = Entry(self.frame, width = 15)
        self.entrada2.insert(0, 53000)
        self.entrada3 = Entry(self.frame, width = 15)

        enviar = Button(self.frame, text = "Conectar", command = self.verificar2)

        self.titulo.grid(row = 0, columnspan = 2)
        self.entrada1.grid(row = 1, column = 1)
        self.entrada2.grid(row = 2, column = 1)
        self.entrada3.grid(row = 3, column = 1)
        enviar.grid(row = 4, columnspan = 2)

    def verificar2(self):
        if self.entrada1.get() != '' and self.entrada2.get().isnumeric():
            ip = self.entrada1.get()
            porta = self.entrada2.get()
            mensagem = self.entrada3.get()
            if self.servidor.responde("SignIn "+mensagem, (ip, int(porta))) != "Failed":
                self.principal()
            else:
                self.titulo['text'] = "Não consegui esse conectar"
                self.titulo['fg'] = 'red'
        else:
            self.titulo['text'] = 'Digite as informações corretamente'
            self.titulo['fg'] = 'red'
    
    def principal(self):
        self.limpa()
        
if __name__ == '__main__':
    servidor = Server()
