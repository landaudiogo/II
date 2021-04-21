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
            vacancies_left_side = vacancies_left(client)

            values_to_update = next_piece(vacancies_left_side)

            if  values_to_update:
                
                # escrita de variaveis

                state_L, ready_L, mover_L = warehouse_exit_ALT6_state(client)

                print(state_L)
                print(ready_L)
                
                if not(state_L) and ready_L and not(mover_L):
                    update_warehouse_exit('left', values_to_update['id'], values_to_update['machine'], values_to_update['piece_type'], client)  
                    
                    piece = Piece(piece_id = values_to_update['id'], location = False)
                    with session_manager() as session:
                        session.merge(piece)
                        session.commit()
                    

                #read_warehouse_entry_left(client)
            


            # Right side 

            # leitura de variaveis
            
            vacancies_right_side = vacancies_right(client)
            
            values_to_update = next_piece(vacancies_right_side)

            if  values_to_update:

                state_R, ready_R, mover_R = warehouse_exit_ART2_state(client)
                print(state_R)
                print(ready_R)
                
                # escrita de variaveis
                if not(state_R) and ready_R and not(mover_R) :
                    update_warehouse_exit('right', values_to_update['id'], values_to_update['machine'], values_to_update['piece_type'], client)  
                    
                    piece = Piece(piece_id = values_to_update['id'], location = False)
                    with session_manager() as session:
                        session.merge(piece)
                        session.commit()
                    

                #read_warehouse_entry_right(client)


    return