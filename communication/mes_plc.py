from time import sleep
from .opcua_connection import StartClient

from ..general.queries import next_piece_query
from ..models import engine

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
            print('\n')
            print('\n')
            print('\n')
            print('===Left Side===')
            print(vacancies_left_side)

            values_to_update = next_piece(vacancies_left_side)

            print(values_to_update)

            # escrita de variaveis
            
            if not(warehouse_exit_ALT6_state(client)):
                update_warehouse_exit('left', values_to_update['id'], values_to_update['machine'], values_to_update['piece_type'], client)  

            #read_warehouse_entry_left(client)
            
            sleep(3)

            # Right side 

            # leitura de variaveis
            
            vacancies_right_side = vacancies_right(client)
            
            values_to_update = next_piece(vacancies_right_side)

            print('===Right Side===')
            print(vacancies_right_side)
            print(values_to_update)

            if  not values_to_update:
                continue

            # escrita de variaveis
            if not(warehouse_exit_ART2_state(client)):
                update_warehouse_exit('right', values_to_update['id'], values_to_update['machine'], values_to_update['piece_type'], client)  


            #read_warehouse_entry_right(client)

            sleep(3)

    return