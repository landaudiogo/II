import socket
from time import sleep

command_list = [f'command{i}.xml' for i in range(5, 7)]
sleep_list = [3, 47, 3, 0]

for i, name in enumerate(command_list):
    file = open(name, 'r')
    command = file.read()
    bytesToSend         = str.encode(command)
    serverAddressPort   = ("127.0.0.1", 54321)
    bufferSize          = 10000

    print(f'=== sending command{i+1}.xml ===')

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    stream = UDPClientSocket.recv(10000)
    message = stream.decode()
    print(message)


    file.close()
    sleep(sleep_list[i])