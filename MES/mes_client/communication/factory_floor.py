from opcua import Client
from opcua import ua
from ..models import Piece, session_manager

from .opcua_connection import StartClient


def warehouse_exit_ART2_state(client):

    conveyer = ['Fabrica.tapetelinear_ART2.Wait_R.x', 
                'Machines_Right_Control.ReadyT1', 
                'Machines_Right_Control.ReadyT2', 
                'GVL.piece_id_R']

    state = client.read_variables(conveyer)

    return state['Fabrica.tapetelinear_ART2.Wait_R.x'], state['Machines_Right_Control.ReadyT1'], state['Machines_Right_Control.ReadyT2'],  state['GVL.piece_id_R']

def warehouse_exit_ALT6_state(client):

    conveyer = ['Fabrica.tapetelinear_ALT6.Wait_L.x', 
                'Machines_Left_Control.ReadyT2', 
                'Machines_Left_Control.ReadyT3', 
                'GVL.piece_id_L']

    state = client.read_variables(conveyer)

    return state['Fabrica.tapetelinear_ALT6.Wait_L.x'], state['Machines_Left_Control.ReadyT2'], state['Machines_Left_Control.ReadyT3'],  state['GVL.piece_id_L']

def update_warehouse_exit(side, id, transformation, piece_type, client, unload=0, piece_state=False):

    where_to_move = 'R' if side == 'right' else 'L'

    values_to_update = {f'GVL.piece_id_{where_to_move}' : id, 
                        f'GVL.tranformation_{where_to_move}' : transformation, 
                        f'GVL.done_{where_to_move}' : piece_state, 
                        f'GVL.piece_type_{where_to_move}' : int(piece_type[1]), 
                        f'GVL.unload_{where_to_move}' : unload,
                        f'GVL.MOVER_{where_to_move}' : True}

    for key, value in values_to_update.items():
        client.update_unique_variable(key, value)

    

def read_warehouse_entry_right(client):

    values_to_read = [  'Fabrica.tapetelinear_ART1.Ocupado.x',
                        'Fabrica.tapetelinear_ART1.inf_tapete.piece_id', 
                        'Fabrica.tapetelinear_ART1.inf_tapete.transformation', 
                        'Fabrica.tapetelinear_ART1.inf_tapete.done', 
                        'Fabrica.tapetelinear_ART1.inf_tapete.piece_type',
                        'Fabrica.tapetelinear_ART1.inf_tapete.unload' ]
    

    values = client.read_variables(values_to_read)

    if values['Fabrica.tapetelinear_ART1.Ocupado.x']:

        with session_manager() as session:

            if values['Fabrica.tapetelinear_ART1.inf_tapete.piece_id']:

                piece_id = values['Fabrica.tapetelinear_ART1.inf_tapete.piece_id']
                piece = Piece(piece_id = piece_id).object_get(session)
                piece.location = True

                piece_type = values['Fabrica.tapetelinear_ART1.inf_tapete.piece_type'] 
                piece.list_states = [elem for elem in [*piece.list_states, f'P{str(piece_type)}']]

                session.commit()

            else:
                
                piece_type = values['Fabrica.tapetelinear_ART1.inf_tapete.piece_type']
                piece = Piece()

                piece.list_states = [piece_type]

                piece.object_add(session)
                
        client.update_unique_variable('Fabrica.tapetelinear_ART1.mete_armazem', True)



def read_warehouse_entry_left(client):

    values_to_read = [  'Fabrica.tapetelinear_ALT5.Ocupado.x',
                        'Fabrica.tapetelinear_ALT5.inf_tapete.piece_id', 
                        'Fabrica.tapetelinear_ALT5.inf_tapete.transformation', 
                        'Fabrica.tapetelinear_ALT5.inf_tapete.done', 
                        'Fabrica.tapetelinear_ALT5.inf_tapete.piece_type',
                        'Fabrica.tapetelinear_ALT5.inf_tapete.unload' ]

    values = client.read_variables(values_to_read)

    if values['Fabrica.tapetelinear_ALT5.Ocupado.x']:

        with session_manager() as session:

            if values['Fabrica.tapetelinear_ALT5.inf_tapete.piece_id']:
                
                piece_id = values['Fabrica.tapetelinear_ALT5.inf_tapete.piece_id']
                piece = Piece(piece_id = piece_id).object_get(session)
                piece.location = True

                piece_type = values['Fabrica.tapetelinear_ALT5.inf_tapete.piece_type'] 
                piece.list_states = [elem for elem in [*piece.list_states, f'P{str(piece_type)}']]

                session.commit()

            else:
                
                piece_type = values['Fabrica.tapetelinear_ALT5.inf_tapete.piece_type']
                piece = Piece()

                piece.list_states = [piece_type]

                piece.object_add(session)
                
        client.update_unique_variable('Fabrica.tapetelinear_ALT5.mete_armazem', True)


def vacancies_right(client):

    variables = [   'Right_Cell_Control.contador1_right', 
                    'Right_Cell_Control.contador2_right' ]

    state = client.read_variables(variables)
    state['1'] = state.pop('Right_Cell_Control.contador1_right')
    state['2'] = state.pop('Right_Cell_Control.contador2_right')

    return state


def vacancies_left(client):

    variables = ['Left_Cell_Control.contador2_left', 
                 'Left_Cell_Control.contador3_left']

    state = client.read_variables(variables)

    state['2'] = state.pop('Left_Cell_Control.contador2_left')
    state['3'] = state.pop('Left_Cell_Control.contador3_left')

    return state

def unload_vacancies(client):

    variables = ['Unload.nmr_unload_points_1', 
                 'Unload.nmr_unload_points_2', 
                 'Unload.nmr_unload_points_3']

    state = client.read_variables(variables)

    state['PM1'] = state.pop('Unload.nmr_unload_points_1')
    state['PM2'] = state.pop('Unload.nmr_unload_points_2')
    state['PM3'] = state.pop('Unload.nmr_unload_points_3')

    return state





