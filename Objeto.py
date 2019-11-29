from tkinter import *
from socket import *

class Objeto:
    def __init__(self, titulo, cor, porta):
        self.janela = Tk()
        self.janela.title(titulo)
        self.janela.geometry("240x110+600+400")
        self.janela['bg'] = cor
        self.frame = Frame(self.janela)
        self.frame['bg'] = cor
        self.frame.pack()

        self.titulo = titulo

        self.cor = cor
        self.ip = ''
        self.port = porta
        
        self.inicio()
    
    def inicio(self):
        self.titulo = Label(self.frame, text = self.titulo, bg = self.cor)
        Label(self.frame, text = "Digite seu Ip: ", bg = self.cor).grid(row = 1, pady = 2)
        Label(self.frame, text = "Digite a porta:", bg = self.cor).grid(row = 2, pady = 2)
        
        self.entrada1 = Entry(self.frame, width = 15)
        self.entrada1.insert(0, "127.0.0.1")
        self.entrada2 = Entry(self.frame, width = 15)
        self.entrada2.insert(0, str(self.port))

        local = Radiobutton(self.frame, text = "Local", command = self.localIp, indicatoron = False, width = 5)
        proprio = Radiobutton(self.frame, text = "Online", command = self.selfIp, indicatoron = False, width = 5)
        enviar = Button(self.frame, text = "Iniciar", command = self.verificar)

        self.titulo.grid(row = 0, columnspan = 3)
        self.entrada1.grid(row = 1, column = 1)
        self.entrada2.grid(row = 2, column = 1)
        local.grid(row = 1, column = 2)
        proprio.grid(row = 2, column = 2)
        enviar.grid(row = 3, columnspan = 3)
    
    def localIp(self): 
        self.entrada1.delete(0, 'end')
        self.entrada1.insert(0, "127.0.0.1")
    
    def selfIp(self): 
        self.entrada1.delete(0, 'end')
        self.entrada1.insert(0, str(gethostbyname(gethostname())))
    
    def verificar(self):
        if self.entrada1.get() != '' and self.entrada2.get().isnumeric():
            self.ip = self.entrada1.get()
            self.port = int(self.entrada2.get())
            self.main()
        else:
            self.titulo['text'] = 'Digite as informações corretamente'
            self.titulo['fg'] = 'red'

    def main(self):
        pass
    
    def iniciar(self):
        pass
    
    def limpa(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def messageBlack(self, message):
        self.resultado['text'] = message
        self.resultado['fg'] = 'black'
        
    def messageRed(self, message):
        self.resultado['text'] = message
        self.resultado['fg'] = 'red'