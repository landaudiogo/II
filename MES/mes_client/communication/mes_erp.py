import socket

from ..general.xml import parseXML
from ..general.exceptions import DataException
from ..models import (
    Order, 
    Transform,
    Unload,
    session_manager
)


def process_order(erp_dict, list_transformations, list_unloads):
    order_dict = erp_dict.get('order') 
    if order_dict is None: 
        raise DataException(
            data_exception_type='Missing key from erp_dict', 
            message='Expected erp_dict to contain order'
        )

    with session_manager() as session:
        order = Order(**order_dict)
        order.object_insert_or_nothing(session)

        if order.transformations != []: 
            print('received transformation')
            # prioritize the orders based on a metric to be defined
            list_transformations.extend(order.transformations)

        elif order.unloads != []: 
            print('received unload')
            list_unloads.extend(order.unloads)


def process_request_stores():
    """Fetches the pieces in the wearhouse at the moment, and groups the pieces
    by type

    Returns 
    =======
    List: each element piece + quantity
    representing the amount of pieces in the shop floor at the moment the
    request was performed

    """

    return 

def process_request_stores():
    return 



def thread2(list_transformations, list_unloads):

    HOST = '127.0.0.1'
    PORT = 5902

    UDPserver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
    UDPserver.bind((HOST, PORT))

    with session_manager() as session: 
        unloads = session.query(Unload).all()
        transformations = session.query(Transform).all()

        list_transformations.list_init(transformations)
        list_unloads.list_init(unloads)

    while True: 
        message, addr = UDPserver.recvfrom(4096)
        erp_dict = parseXML(
            message.decode(), 
            force_list={'Transform': 'transformations', 'Unload': 'unloads'}
        )

        if erp_dict.get('order') != None:
            process_order(erp_dict, list_transformations, list_unloads)
        elif erp_dict.get('request_stores') != None: 
            print('request_stores') 
        elif erp_dict.get('request_orders') != None:
            print('request_orders') 
    return 
