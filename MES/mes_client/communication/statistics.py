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

    ret =  client.read_variables(machine_parameters)
    new_dict = {}
    for key, value in ret.items():
        key = key.replace(f'Fabrica.Maquina_C{where}1T{machine}.inf_maq.', '')
        new_dict[key] = value
    return new_dict


def unloads_information(zone, client):
    
    unload_informations = [f'Fabrica.pusher_CR2T{zone}.inf_pusher.stat_p1',
                           f'Fabrica.pusher_CR2T{zone}.inf_pusher.stat_p2',
                           f'Fabrica.pusher_CR2T{zone}.inf_pusher.stat_p3',
                           f'Fabrica.pusher_CR2T{zone}.inf_pusher.stat_p4',
                           f'Fabrica.pusher_CR2T{zone}.inf_pusher.stat_p5',
                           f'Fabrica.pusher_CR2T{zone}.inf_pusher.stat_p6',
                           f'Fabrica.pusher_CR2T{zone}.inf_pusher.stat_p7',
                           f'Fabrica.pusher_CR2T{zone}.inf_pusher.stat_p8',
                           f'Fabrica.pusher_CR2T{zone}.inf_pusher.stat_p9',
                           f'Fabrica.pusher_CR2T{zone}.inf_pusher.stat_total_p']

    ret = client.read_variables(unload_informations)
    new_dict = {
        key.replace(f'Fabrica.pusher_CR2T{zone}.inf_pusher.', ''): value
        for key, value in ret.items()
    }
    return new_dict



with StartClient('opc.tcp://localhost:4840') as special_client:
    while True:
        options = (input("1-Machines Statistics\n2-Unloads Informations\n"))

        if options == '1':
            side = (input("Side on which the machine is:"))
            machine = str(input("Machine Number:"))
            ret = machine_informations(side, machine, special_client)
            for key, value in ret.items(): 
                print(key, value)
        else:
            for i in range(3,6):
                print(f'Zone {i-2}:')
                ret = unloads_information(i, special_client)
                for key, value in ret.items(): 
                    print(key, value)
                print('\n')

        print('\n\n')