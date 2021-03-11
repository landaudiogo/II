import socket
from ..general.xml.HandleERPRequest import parseXML
from ..models import Order, Session

HOST = '127.0.0.1'
PORT = 5902

UDPserver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
UDPserver.bind((HOST, PORT))

while True: 
    message, addr = UDPserver.recvfrom(4096)
    order_string = message.decode()
    order_dict = parseXML(order_string, force_list={'Transform': 'transformations', 'Unload': 'unloads'})
    order = Order(**order_dict['order'])
    session = Session()
    order.object_insert_or_nothing(session)
    # prioriza os dados
