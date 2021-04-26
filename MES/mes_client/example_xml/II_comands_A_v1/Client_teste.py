import socket
from time import sleep

name_list = (f'command{i}.xml' for i in range(1,5))

for name in name_list:

    file = open(name, 'r')
    command = file.read()

    bytesToSend         = str.encode(command)

    serverAddressPort   = ("127.0.0.1", 54321)

    bufferSize          = 1024

    # Create a UDP socket at client side

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send to server using created UDP socket

    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    # enviar mensagem
    file.close()
    break
    sleep(20)