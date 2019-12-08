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
        self.servidor = Udp("server", self.port)
        self.titulo = Label(self.frame, text = 'Informe o DNS', bg = self.cor)
        Label(self.frame, text = "Digite o Ip: ",bg = self.cor).grid(row = 1, pady = 2)
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
            mensagem = self.entrada3.get() + ":" + str(self.port)
            if self.servidor.responder("SignIn "+mensagem, (ip, int(porta))) != "Failed":
                self.principal()
            else:
                self.titulo['text'] = "Não consegui esse conectar"
                self.titulo['fg'] = 'red'
        else:
            self.titulo['text'] = 'Digite as informações corretamente'
            self.titulo['fg'] = 'red'
    
    def principal(self):
        self.limpa()
        self.janela.geometry("230x280+600+400")

        Label(self.frame, text = "Servidor de Arquivos", bg = self.cor).grid(row = 0, columnspan = 3)
        Label(self.frame, text = "Arquivos recebidos:", bg = self.cor).grid(row = 1)
        self.lista = Listbox(self.frame, width = 35)
        self.resultado = Label(self.frame, text = "Inativo", bg = self.cor)
        self.ligar = Button(self.frame, text = "Ligar", command = self.turnOn)
        self.comecar = Button(self.frame, text = "Iniciar", command = self.iniciar)
        self.parar = Button(self.frame, text = "Parar", command = self.desligar)
        
        self.lista.grid(row = 2, columnspan = 3)
        self.resultado.grid(row = 3, columnspan = 3)
        self.ligar.grid(row = 4, column = 0, sticky = W, padx = 20)
        self.comecar.grid(row = 4, column = 1, sticky = W, padx = 5)
        self.parar.grid(row = 4, column = 2, sticky = W, padx = 5)
        
    def desligar(self):
        self.ligado = False
        self.messageBlack('Servidor desligado')

    def turnOn(self):
        self.ligado = True
        self.messageBlack('Servidor ligado')

    def iniciar(self):
        if self.ligado: self.messageBlack('Preparado para receber...')
        else: self.messageRed("Não está ligado!")

        while self.ligado:
            self.janela.update_idletasks()
            self.janela.update()
            if self.ligado:
                mensagem, ip, port = self.servidor.receber()
                if mensagem != None:
                    endereco = ip+":"+str(port)
                    requisicao, mensagem = mensagem.split()
                    if requisicao == 'FILE':
                        self.servidor.receberArquivo(mensagem)
                        resultado = self.servidor.getReport()
                        if resultado.split()[0] == "FINISH":
                            self.messageBlack("Arquivo recebido com Sucesso!")
                            self.lista.insert(END, mensagem)
                        else:
                            resultado = resultado.split()[1]
                            if resultado == "SEND":
                                self.messageRed("Cliente inacessível!")
                            elif resultado == "TIME":
                                self.messageRed("Cliente inacessível!")
                            else:
                                self.messageRed("Algo deu errado...")
            self.janela.update_idletasks()

if __name__ == '__main__':
    servidor = Server()
