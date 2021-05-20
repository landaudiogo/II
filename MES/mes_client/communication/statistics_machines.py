from .opcua_connection import StartClient

from .factory_floor import (
    vacancies_left,
    vacancies_right,
    read_warehouse_entry_left,
    read_warehouse_entry_right,
    warehouse_exit_ALT6_state,
    warehouse_exit_ART2_state,
    update_warehouse_exit,
    unload_vacancies
)

def machine_informations(side, machine, client):

    where = 'R' if side == 'right' else 'L'

    machine_parameters = [ f'Fabrica.Maquina_C{where}1T{machine}.inf_maq.stat_p1',
                           f'Fabrica.Maquina_C{where}1T{machine}.inf_maq.stat_p2',
                           f'Fabrica.Maquina_C{where}1T{machine}.inf_maq.stat_p3',
                           f'Fabrica.Maquina_C{where}1T{machine}.inf_maq.stat_p4',
                           f'Fabrica.Maquina_C{where}1T{machine}.inf_maq.stat_p5',
                           f'Fabrica.Maquina_C{where}1T{machine}.inf_maq.stat_p6',
                           f'Fabrica.Maquina_C{where}1T{machine}.inf_maq.stat_time',
                           f'Fabrica.Maquina_C{where}1T{machine}.inf_maq.Stat_total_p']

    return client.read_variables(machine_parameters)



with StartClient('opc.tcp://localhost:4840') as special_client:

    side = (input("Side on which the machine is:"))
    machine = str(input("Machine Number:"))

    print(machine_informations(side, machine, special_client))

