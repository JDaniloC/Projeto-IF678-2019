from socket import *
from time import sleep

def loading():
    print("Cliente is typing", end='')
    for i in range(3):
        sleep(0.5)
        print(".", end='')
    print()

port = 12000
server = socket(AF_INET, SOCK_DGRAM)
server.bind(('', port))
print("Server preparado para receber.\n")
while True:
    loading()
    message, address = server.recvfrom(2048)
    if message.decode() == "Closing connection...":
        print("\nO cliente saiu.")
        server.close()
        break
    else:
        print("\nClient respondeu:",message.decode().capitalize())
        nova = input("Digite sua mensagem: ")
        if nova.capitalize() == "Tchau":
            print("\nServer desligado.")
            server.sendto(b'Closing connection...',  address)
            server.close()
            break
        else:
            server.sendto(nova.encode(), address)
        
