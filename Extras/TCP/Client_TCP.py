from socket import*
from time import sleep

def loading():
    print("Waiting server answer", end='')
    for i in range(3):
        sleep(0.5)
        print(".", end='')
    print()

name = '127.0.0.1'
port = 12000
client = socket(AF_INET, SOCK_STREAM)
client.connect((name, port))
verificador = True
while verificador:
    message = input("Digite sua mensagem: ")
    if message.capitalize() == "Tchau":
        print("\nVocê saiu.")
        client.send(b'Closing connection...')
        client.close()
        verificador = False
    else:
        client.send(message.encode())
        loading()
        answer = client.recv(1024)
        if answer.decode() == "Closing connection...":
            print("\nO servidor desligou.")
            client.close()
            verificador = False
        else:
            print('\nHost respondeu:', answer.decode())


