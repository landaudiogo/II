import socket
from functools import reduce
from datetime import datetime
from math import (
    exp, 
    ceil
)
from sqlalchemy import func, desc


from ..general.xml import parseXML
from ..general.exceptions import DataException
from ..general.queries import (
    order_quantity_query, 
    pieces_for_transformation_query, 
    unset_pieces_query
)
from ..algorithms.path import Graph, Node
from ..models import (
    Order, 
    Transform,
    Unload,
    Piece,
    MesSession,
    session_manager,
    engine
)


# start_time
with session_manager() as session:
    session_list = session.query(MesSession).all()
    if not session_list:
        start_time = datetime.now().timestamp()
        start_session = MesSession(start_epoch=start_time)
        start_session.object_add(session)
        start_epoch = start_session.start_epoch
        # create all the types of pieces
        pieces = [Piece(list_states=['P1']) for _ in range(400)]
        pieces.extend([Piece(list_states=['P2']) for _ in range(40)])
        pieces.extend([Piece(list_states=['P3']) for _ in range(20)])
        pieces.extend([Piece(list_states=['P4']) for _ in range(20)])
        pieces.extend([Piece(list_states=['P5']) for _ in range(20)])
        pieces.extend([Piece(list_states=['P6']) for _ in range(20)])
        session.bulk_save_objects(pieces)
        session.commit()
    else: 
        start_epoch = session_list[0].start_epoch


# piece_type graph to determine the transformations
node_list = [Node(f'P{i}') for i in range(1,10)]
for i in range(6):
    node_list[i].add_node_next(node_list[i+1])
node_list[4].add_node_next(node_list[8])
node_list[5].add_node_next(node_list[7])
ptype_graph = Graph(node_list)


def process_transformations(order):
    with session_manager() as session: 
        # create the list of transformations limited to 5 elements each
        original = order.transformations[0]
        original.received_time = datetime.now().timestamp()
        num_trans = ceil(original.quantity/5)
        transformations = [Transform(**original._to_dict()) for i in range(num_trans)]
        order.transformations = transformations
        total_qnt = 0
        for trans in order.transformations:
            trans.list_states = ptype_graph.find_path(
                getattr(trans, 'from'),
                getattr(trans, 'to')
            )
            trans.quantity = min(5, original.quantity-total_qnt)
            total_qnt += trans.quantity
        order.object_insert_or_nothing(session)

        # prioritize the orders
        orders = session.query(Order).all()
        for order in orders: 
            if not order.transformations:
                continue
            first_trans = order.transformations[0]
            time_diff = (
                (first_trans.time + first_trans.maxdelay) -
                (int(datetime.now().strftime('%s'))-start_epoch)
            )
            order_quantity = reduce(
                (lambda x, y: x + y.quantity),
                order.transformations,
                0
            )
            for trans in order.transformations:
                trans.priority = (
                    (trans.penalty*exp(-time_diff/100)) * (order_quantity*len(trans.list_states))
                )
            session.merge(order)
        session.commit()

        # associate pieces to transformations 
        transformations = (
            session.query(Transform)
            .order_by(desc(Transform.priority)).all()
        )
        for trans in transformations: 
            with engine.connect() as conn:
                get_piece_ids = pieces_for_transformation_query(
                    trans.transform_id,
                    trans.quantity,
                    conn
                )
                unset_pieces_query(
                    trans.transform_id, 
                    get_piece_ids, 
                    conn
                )

            [session.merge(Piece(piece_id=piece_id, transform_id=trans.transform_id)) 
                for piece_id in get_piece_ids
            ]
            session.commit()




def process_order(order_dict):
    order = Order(**order_dict)
    if order.transformations != []: 
        print('=== PROCESS TRANSFORMATION ===')
        process_transformations(order)

    elif order.unloads != []: 
        with session_manager() as session:
            print(order.number)
            order.object_insert_or_nothing(session)


def process_request_stores():
    """Fetches the pieces in the wearhouse at the moment, and groups the pieces
    by type

    Returns 
    =======
    List: each element piece_type + quantity
        representing the amount of pieces in the shop floor at the moment the
        request was performed

    """

    return 


def thread2():

    HOST = '127.0.0.1'
    PORT = 54321

    UDPserver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
    UDPserver.bind((HOST, PORT))

    while True: 
        message, addr = UDPserver.recvfrom(4096)
        erp_dict = parseXML(
            message.decode(), 
            force_list={
                'Transform': 'transformations', 
                'Unload': 'unloads',
                'Order': 'order'
            }
        ).get('orders')

        if erp_dict.get('order') != None:
            for order_dict in erp_dict['order']: 
                print(order_dict)
                process_order(order_dict)
                print('=== 2 === TERMINOU')
        elif erp_dict.get('request_stores') != None: 
            print('request_stores') 
        elif erp_dict.get('request_orders') != None:
            print('request_orders') 
    return 
