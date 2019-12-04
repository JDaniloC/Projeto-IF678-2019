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
        self.port = porta
    
    def inicio(self):
        self.titulo = Label(self.frame, text = self.titulo, bg = self.cor)
        Label(self.frame, text = "Digite a porta:", bg = self.cor, pady = 5).grid(row = 1, pady = 2)
        
        self.entrada = Entry(self.frame, width = 15)
        self.entrada.insert(0, str(self.port))

        enviar = Button(self.frame, text = "Iniciar", command = self.verificar, width = 4)

        self.titulo.grid(row = 0, columnspan = 2)
        self.entrada.grid(row = 1, column = 1)
        enviar.grid(row = 2, columnspan = 2)
    
    def verificar(self):
        if self.entrada.get().isnumeric():
            self.port = int(self.entrada.get())
            self.main()
        else:
            self.titulo['text'] = 'Digite a porta corretamente!'
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

if __name__ == "__main__":
    print("oi")
    objeto = Objeto("Default", 'black', 1000)
    objeto.inicio()
