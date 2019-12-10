from tkinter import *
from socket import *
from Objeto import Objeto
from Transporte.UDP import Udp
from os import makedirs

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
            if self.servidor.responder("Get "+mensagem, (ip, int(porta))) != "FAIL":
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
        
        Label(self.frame, text = "Arquivos recebidos:", bg = self.cor).grid(row = 3)
        self.lista = Listbox(self.frame, width = 35)
        self.lista.insert(END, "Servidor:\n")
        self.listar()
        enviar = Button(self.frame, text = "Requisitar", command = self.verificar3)
        listar = Button(self.frame, text = "Listar", command = self.listar)

        self.resultado.grid(row = 0, columnspan = 3)
        self.entrada1.grid(row = 1, column = 1)
        self.entrada2.grid(row = 2, column = 1)

        self.lista.grid(row = 4, columnspan = 3)
        enviar.grid(row = 5, columnspan = 3)
        listar.grid(row = 5, column = 1, columnspan = 3)

    def listar(self):
        self.servidor.responder("LIST all", self.serverAddress)
        mensagem, ip, port = self.servidor.receber()
        if mensagem != None:
            dic = self.decodificar(mensagem)
            for i in dic:
                self.lista.insert(END, i)
                for j in dic[i]:
                    self.lista.insert(END, "      "+j)
            self.lista.insert(END, "")
            self.lista.insert(END, "Recebidos")
        else:
            self.messageRed("Problema no servidor!")

    def decodificar(self, string):
        string = string.replace(" ", "").replace("[", "").replace("]", "")
        lista = string.split("§")
        dic = {}
        for i in lista[:-1]:
            elementos = i.split(':')
            dic[elementos[0]] = elementos[1].split(',')
        return dic

    def verificar3(self):
        if self.variavel.get() == 0:
            self.messageBlack("Requisitando arquivo")
            self.recebeArquivo(self.entrada1.get())
        else:
            self.messageBlack("Requisitando arquivos")
            self.recebePasta(self.entrada2.get())

    def recebeArquivo(self, nome):
        try:
            makedirs('/'.join(nome.split("/")[:-1]))
        except:
            self.messageBlack("Pasta já existente")
        finally:
            resultado = self.servidor.responder("FILE "+nome, self.serverAddress)
            if resultado != "FAIL":
                self.servidor.receberArquivo(nome)
                resultado = self.servidor.getReport()
                if resultado.split()[0] == "FINISH":
                    self.messageBlack("Arquivo recebido com Sucesso!")
                    self.lista.insert(END, nome)
                else:
                    resultado = resultado.split()[1]
                    if resultado == "SEND":
                        self.messageRed("Erro no envio!")
                    elif resultado == "TIME":
                        self.messageRed("Servidor inacessível!")
                    else:
                        self.messageRed("Algo deu errado...")
            else:
                self.messageRed("Servidor inacessível")

    def recebePasta(self, caminho):
        try:
            makedirs(caminho)
        except:
            self.messageBlack("Pasta já existente")
        finally:
            resultado = self.servidor.responder("FOLDER "+caminho, self.serverAddress)
            if resultado != "FAIL":
                enviou = True
                self.lista.insert(END, caminho)
                mensagem, ip, port = self.servidor.receber()
                while mensagem != "CLOSE CONN" and mensagem != None:
                    nome = mensagem.split()[1]
                    self.servidor.receberArquivo(nome)
                    resultado = self.servidor.getReport()
                    if resultado.split()[0] != "FINISH":
                        enviou = False
                        break
                    else:
                        self.lista.insert(END, "      " + nome)
                    mensagem, ip, port = self.servidor.receber()
                if enviou == True and mensagem != None:
                    self.messageBlack("Pasta recebida!")
                elif resultado == "SEND":
                    self.messageRed("Erro no envio!")
                elif resultado == "TIME" or mensagem == None:
                    self.messageRed("Servidor inacessível!")
                else:
                    self.messageRed("Algo deu errado...")
            else:
                self.messageRed("Não consegui conectar!")

if __name__ == '__main__':
    servidor = Client()
    servidor.janela.mainloop()
