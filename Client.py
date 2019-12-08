from tkinter import *
from socket import *
from Objeto import Objeto
from Transporte.UDP import Udp
from os import listdir

class Client(Objeto):
    def __init__(self):
        super().__init__("Client", "LightGoldenrod1", 12345)
        self.cor = "LightGoldenrod1"
        self.main()

    def main(self):
        self.limpa()
        self.janela.geometry("260x150+600+400")
        self.servidor = Udp("Client")
        self.resultado = Label(self.frame, text = 'Informe o DNS', bg = self.cor)
        Label(self.frame, text = "Digite o Ip:   ", bg = self.cor).grid(row = 1, pady = 2)
        Label(self.frame, text = "Digite a porta:", bg = self.cor).grid(row = 2, pady = 2)
        Label(self.frame, text = "Digite o nome: ", bg = self.cor).grid(row = 3, pady = 2)
        
        self.entrada1 = Entry(self.frame, width = 15)
        self.entrada1.insert(0, "127.0.0.1")
        self.entrada2 = Entry(self.frame, width = 15)
        self.entrada2.insert(0, 53000)
        self.entrada3 = Entry(self.frame, width = 15)

        enviar = Button(self.frame, text = "Conectar", command = self.verificar2)

        self.resultado.grid(row = 0, columnspan = 2)
        self.entrada1.grid(row = 1, column = 1)
        self.entrada2.grid(row = 2, column = 1)
        self.entrada3.grid(row = 3, column = 1)
        enviar.grid(row = 4, columnspan = 2)

    def verificar2(self):
        if self.entrada1.get() != '' and self.entrada2.get().isnumeric():
            ip = self.entrada1.get()
            porta = self.entrada2.get()
            mensagem = self.entrada3.get()
            if self.servidor.responder("Get "+mensagem, (ip, int(porta))) != "Failed":
                mensagem, ip, port = self.servidor.receber()
                if mensagem != None and mensagem != "NULL":
                    self.ipServer, self.portServer = mensagem.split(":")
                    self.portServer = int(self.portServer)
                    self.serverAddress = (self.ipServer, self.portServer)
                    self.principal()
                else: self.messageRed("Servidor não existe!")
            else: self.messageRed("Não consegui esse conectar")
        else: self.messageRed('Digite as informações corretamente')
    
    def principal(self):
        self.limpa()
        self.janela.geometry("300x280+600+400")

        self.resultado = Label(self.frame, text = 'Transferência de Arquivos', bg = self.cor)
        Label(self.frame, text = "Digite o nome do arquivo: ", bg = self.cor).grid(row = 1, pady = 2)
        Label(self.frame, text = "Digite o nome da pasta:", bg = self.cor).grid(row = 2, pady = 2)
        
        self.entrada1 = Entry(self.frame, width = 15)
        self.entrada2 = Entry(self.frame, width = 15)

        self.variavel = IntVar(self.frame, 0)

        Radiobutton(self.frame, text = "Arquivo", variable = self.variavel, value = 0, indicatoron = False, width = 5).grid(row = 1, column = 2)
        Radiobutton(self.frame, text = "Pasta", variable = self.variavel, value = 1, indicatoron = False, width = 5).grid(row = 2, column = 2)
        
        Label(self.frame, text = "Arquivos enviados:", bg = self.cor).grid(row = 3)
        self.lista = Listbox(self.frame, width = 35)
        enviar = Button(self.frame, text = "Enviar", command = self.verificar3)

        self.resultado.grid(row = 0, columnspan = 3)
        self.entrada1.grid(row = 1, column = 1)
        self.entrada2.grid(row = 2, column = 1)

        self.lista.grid(row = 4, columnspan = 3)
        enviar.grid(row = 5, columnspan = 3)

    def verificar3(self):
        if self.variavel.get() == 0:
            self.messageBlack("Enviando arquivo")
            self.enviaArquivo(self.entrada1.get())
        else:
            self.messageBlack("Enviando arquivos")
            self.enviaPasta(self.entrada2.get())

    def enviaPasta(self, path):
        self.servidor.enviarPasta(path, self.serverAddress)
        resultado = self.servidor.getReport()
        if resultado.split()[0] == "FINISH":
            self.messageBlack("Arquivos enviados com Sucesso!")
        else:
            resultado = resultado.split()[1]
            if resultado == "FOLDER":
                self.messageRed("Pasta inacessível!")
            elif resultado == "SEND":
                self.messageRed("Servidor inacessível!")
            elif resultado == "FILE":
                self.messageRed("Arquivo inacessível!")
            else:
                self.messageRed("Algo deu errado...")

    def enviaArquivo(self, nome):
        self.servidor.enviarArquivo(nome, self.serverAddress)
        resultado = self.servidor.getReport()
        if resultado.split()[0] == "FINISH":
            self.messageBlack("Arquivos enviados com Sucesso!")
        else:
            resultado = resultado.split()[1]
            if resultado == "SEND":
                self.messageRed("Servidor inacessível!")
            elif resultado == "FILE":
                self.messageRed("Arquivo inacessível!")
            else:
                self.messageRed("Algo deu errado...")

if __name__ == '__main__':
    servidor = Client()
