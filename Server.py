from tkinter import *
from socket import *
from os import listdir

from Objeto import Objeto
from Utils.UDP import Udp
from Utils.listar import *

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
            if self.servidor.responder("SignIn "+mensagem, (ip, int(porta))) != "FAIL":
                self.principal()
            else:
                self.titulo['text'] = "Não consegui conectar!"
                self.titulo['fg'] = 'red'
        else:
            self.titulo['text'] = 'Digite as informações corretamente!'
            self.titulo['fg'] = 'red'
    
    def principal(self):
        self.limpa()
        self.janela.geometry("230x280+600+400")

        Label(self.frame, text = "Servidor de Arquivos", bg = self.cor).grid(row = 0, columnspan = 3)
        Label(self.frame, text = "Arquivos enviados:", bg = self.cor).grid(row = 1)
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
                        self.enviaArquivo(mensagem, (ip, port))
                    elif requisicao == 'FOLDER':
                        self.enviaPasta(mensagem, (ip, port))
                    elif requisicao == "LIST":
                        mensagem = self.codificar(self.listar())
                        self.servidor.responder(mensagem, (ip, port))
                    else:
                        self.messageRed("Não entendi.")
            self.janela.update_idletasks()
    
    def enviaArquivo(self, nome, endereco):
        self.servidor.enviarArquivo(nome, endereco)
        resultado = self.servidor.getReport()
        if resultado.split()[0] == "FINISH":
            self.messageBlack("Arquivo enviado com Sucesso!")
            self.lista.insert(END, nome)
        else:
            resultado = resultado.split()[1]
            if resultado == "SEND":
                self.messageRed("Cliente caiu!")
            elif resultado == "FILE":
                self.messageRed("Arquivo inacessível!")
            else:
                self.messageRed("Algo deu errado...")
    
    def enviaPasta(self, path, endereco):
        self.servidor.enviarPasta(path, endereco)
        resultado = self.servidor.getReport()
        if resultado.split()[0] == "FINISH":
            self.messageBlack("Arquivos enviados com Sucesso!")
            self.lista.insert(END, path)
        else:
            resultado = resultado.split()[1]
            if resultado == "FOLDER":
                self.messageRed("Pasta inacessível!")
            elif resultado == "SEND":
                self.messageRed("Cliente inacessível!")
            elif resultado == "FILE":
                self.messageRed("Arquivo inacessível!")
            else:
                self.messageRed("Algo deu errado...")

    def listar(self, path = '.'):
        arquivos = listdir(path)
        dic = {}
        dic[path] = [x for x in arquivos if x.split('.') != [x]]
        for x in [x for x in arquivos if x.split('.') == [x]]:
            dic.update(self.listar(path+'/'+x))
        return dic

    def codificar(self, dicionario):
        string = ''
        for nome in dicionario:
            string += nome + ':' + str(dicionario[nome]) + "§"
        return string.replace("'", "")

if __name__ == '__main__':
    servidor = Server()
    servidor.janela.mainloop()
