from time import sleep
from .opcua_connection import StartClient

from ..general.queries import next_piece_query
from ..models import engine, Piece, session_manager

from .factory_floor import (
    vacancies_left,
    vacancies_right,
    read_warehouse_entry_left,
    read_warehouse_entry_right,
    warehouse_exit_ALT6_state,
    warehouse_exit_ART2_state,
    update_warehouse_exit
)

def next_piece(vacancies_dict): 
    machine_list = [key
        for key, value in vacancies_dict.items()
            if value > 0
    ]

    if not machine_list:
        return
    with engine.connect() as connection: 
        return next_piece_query(machine_list, connection)
        


def thread1():

    with StartClient('opc.tcp://localhost:4840') as client:
        
        while True: 
            # Left side
            
            # leitura de variaveis
            state_L, ready_T2, ready_T3, curr_piece = warehouse_exit_ALT6_state(client)
            if not curr_piece:
                vacancies_left_side = vacancies_left(client)
                if not ready_T2:
                    vacancies_left_side.pop('2')
                if not ready_T3:
                    vacancies_left_side.pop('3')
                values_to_update = next_piece(vacancies_left_side)

                if  values_to_update:
                    print(values_to_update)
                    # escrita de variaveis
                    if state_L:
                        update_warehouse_exit('left', values_to_update['id'], values_to_update['machine'], values_to_update['piece_type'], client)  
                        piece = Piece(piece_id = values_to_update['id'], location = False)
                        with session_manager() as session:
                            session.merge(piece)
                            session.commit()

            read_warehouse_entry_left(client)
            
            # Right side 

            # leitura de variaveis
            state_R, ready_T1, ready_T2, curr_piece = warehouse_exit_ART2_state(client)
            if not curr_piece:
                vacancies_right_side = vacancies_right(client)
                if not ready_T1:
                    vacancies_right_side.pop('1')
                if not ready_T2:
                    vacancies_right_side.pop('2')
                values_to_update = next_piece(vacancies_right_side)

                if  values_to_update:
                    print(values_to_update)
                    # escrita de variaveis
                    if state_R:
                        update_warehouse_exit('right', values_to_update['id'], values_to_update['machine'], values_to_update['piece_type'], client)  
                        piece = Piece(piece_id = values_to_update['id'], location = False)
                        with session_manager() as session:
                            session.merge(piece)
                            session.commit()

            read_warehouse_entry_right(client)


    return