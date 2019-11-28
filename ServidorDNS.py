from tkinter import *
from socket import *
from Transporte.UDP import Udp
from Objeto import Objeto

class Dns(Objeto):
    def __init__(self):
        super().__init__("Servidor DNS", "LightYellow2", 53000)
        
        self.cor = "LightYellow2"
        self.enderecos = {}
        self.ligado = False
        self.clients = 0
            
    def main(self):
        self.limpa()
        self.janela.geometry("230x260+600+400")
        self.servidor = Udp('server', self.ip, self.port)
            
        Label(self.frame, text = "Servidor DNS", bg = self.cor).grid(row = 0, columnspan = 3)
        Label(self.frame, text = "Endereços registrados:", bg = self.cor).grid(row = 1)
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
        self.resultado['text'] = 'Desligado'
        self.resultado['fg'] = 'black'

    def turnOn(self):
        self.ligado = True
        self.resultado['text'] = 'Ligado'
        self.resultado['fg'] = 'black'

    def iniciar(self):
        if self.ligado: self.resultado['text'] = 'Preparado para receber...'
        else:
            self.resultado['text'] = "Não está ligado!"
            self.resultado['fg'] = 'red'
        while self.ligado:
            self.janela.update_idletasks()
            self.janela.update()
            if self.ligado:
                mensagem, ip, port = self.servidor.recebe()
                if mensagem != None:
                    requisicao, mensagem = mensagem.split()
                    if requisicao == 'SignIn':
                        self.lista.insert(END, " " + mensagem + " = " + ip + ":" + str(port))
                        self.enderecos[mensagem] = (ip, port)
                    else:
                        if (ip, port) not in self.enderecos.values():
                            self.lista.insert(END, " " + "Client"+str(self.clients) + " = " + ip + ":" + str(port))
                            self.enderecos["Client"+str(self.clients)] = (ip, port)
                            self.clients += 1
                        endereco = (ip, port)
                        if mensagem in self.enderecos: # TALVEZ BUG
                            self.servidor.responde(self.enderecos[mensagem], endereco)
                        else:
                            self.servidor.responde("NULL", endereco)
            self.janela.update_idletasks()

if __name__ == '__main__':
    program = Dns()
