
import socket

file = open('command1.xml')


msgFromClient       = file.read()

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("127.0.0.1", 54321)

 

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 

# Send to server using created UDP socket

UDPClientSocket.sendto(bytesToSend, serverAddressPort)