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

        self.inicio()
            
    def main(self):
        self.limpa()
        self.janela.geometry("230x260+600+400")
        self.servidor = Udp('server', self.port)
            
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
        self.messageBlack('Desligado')

    def turnOn(self):
        self.ligado = True
        self.messageBlack('Ligado')

    def iniciar(self):
        if self.ligado: self.messageBlack('Preparado para receber...')
        else: self.messageRed("Não está ligado!")

        while self.ligado:
            self.janela.update_idletasks()
            self.janela.update()
            if self.ligado:
                mensagem, ip, port = self.servidor.receber()
                if mensagem != None:
                    requisicao, mensagem = mensagem.split()
                    if requisicao == 'SignIn':
                        mensagem, porta = mensagem.split(":")
                        endereco = ip + ":" + porta
                        self.lista.insert(END, " " + mensagem + " = " + endereco)
                        self.enderecos[mensagem] = endereco
                    else:
                        endereco = ip+":"+str(port)
                        if endereco not in self.enderecos.values():
                            self.lista.insert(END, " " + "Client"+str(self.clients) + " = " + endereco)
                            self.enderecos["Client"+str(self.clients)] = endereco
                            self.clients += 1
                        endereco = (ip, port)
                        if mensagem in self.enderecos: envio = self.servidor.responder(self.enderecos[mensagem], endereco)
                        else: envio = self.servidor.responder("NULL", endereco)
                        
                        if envio == "FAIL": self.messageRed("Envio não funcionou")
                        else: self.messageBlack("Respondeu requisição")
            self.janela.update_idletasks()
    

if __name__ == '__main__':
    program = Dns()
