from time import sleep

from ..general.queries import next_piece_query
from ..models import engine


def next_piece(vacancies_dict): 
    machine_list = [key
        for key, value in vacancies_dict.items()
            if value > 0
    ]

    if not machine_list:
        return
    with engine.connect() as connection: 
        next_piece_query(machine_list, connection)


def thread1():
    left_cell = {
        2: 0,
        3: 0, 
    }
    right_cell = {
        1: 0, 
        2: 0,
    }

    while True: 
        # Left side
        # leitura de variaveis
        # determina peça
        # escrita de variaveis

        # Right side 
        # leitura de variaveis
        # determina peça
        # escrita de variaveis

        sleep(3)
    return
