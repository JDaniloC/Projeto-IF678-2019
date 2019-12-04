from socket import *
from time import sleep

def loading():
    print("Waiting server answer", end='')
    for i in range(3):
        sleep(0.5)
        print(".", end='')
    print()


name = '172.20.4.148'
port = 12000
client = socket(AF_INET, SOCK_DGRAM)
while True:
    message = input("Digite sua mensagem: ")
    if message.capitalize() == "Tchau":
        print("\nVocê saiu.")
        client.sendto(b'Closing connection...', (name, port))
        client.close()
        break
    else:
        client.sendto(message.encode(),(name, port))
        loading()
        nova, address = client.recvfrom(2048)
        if nova.decode() == "Closing connection...":
            print("\nO servidor desligou.")
            client.close()
            break
        else:
            print("\nHost respondeu:", nova.decode().capitalize())

