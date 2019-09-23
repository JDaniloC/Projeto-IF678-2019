from socket import *
from time import sleep

def loading():
    print("Cliente is typing", end='')
    for i in range(3):
        sleep(0.5)
        print(".", end='')
    print()

port = 12000
server = socket(AF_INET, SOCK_STREAM)
server.bind(("", port))
server.listen(1) # Quantos clientes.
while True:
    print("\nServer está preparado para receber.")
    client, address = server.accept()
    print("Cliente conectado!")
    verificador = True
    while verificador:
        loading()
        message = client.recv(1024).decode()
        if message.capitalize() == "Closing connection...":
            print("\nO cliente saiu.")
            client.close()
            verificador = False
        else:
            print("\nClient respondeu:", message.capitalize())
            answer = input("Digite sua mensagem: ")
            if answer.capitalize() == "Tchau":
                print("\nServer desligado.")
                client.send(b'Closing connection...')
                client.close()
                verificador = False
            else:
                client.send(answer.encode())
    if not int(input("Digite 0 para fechar o servidor: ")):
        print("Server closed.")
        server.close()
        break
    
