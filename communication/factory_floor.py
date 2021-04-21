from opcua import Client
from opcua import ua
from ..models import Piece, session_manager

from .opcua_connection import StartClient


def warehouse_exit_ART2_state(client):

    conveyer = ['GVL.ART2_S', 'Fabrica.tapetelinear_ART2.Ready', 'GVL.MOVER_R']

    state = client.read_variables(conveyer)

    return state['GVL.ART2_S'], state['Fabrica.tapetelinear_ART2.Ready'], state['GVL.MOVER_R']


def warehouse_exit_ALT6_state(client):

    conveyer = ['GVL.ALT6_S', 'Fabrica.tapetelinear_ALT6.Ready', 'GVL.MOVER_L']

    state = client.read_variables(conveyer)

    return state['GVL.ALT6_S'], state['Fabrica.tapetelinear_ALT6.Ready'], state['GVL.MOVER_L']


def update_warehouse_exit(side, id, transformation, piece_type, client, unload=0, piece_state=False):

    where_to_move = 'R' if side == 'right' else 'L'

    values_to_update = {f'GVL.piece_id_{where_to_move}' : id, 
                        f'GVL.tranformation_{where_to_move}' : transformation, 
                        f'GVL.done_{where_to_move}' : piece_state, 
                        f'GVL.piece_type_{where_to_move}' : int(piece_type[1]), 
                        f'GVL.unload_{where_to_move}' : unload,
                        f'GVL.MOVER_{where_to_move}' : True}
    if side == 'right':
        print('values right side')
        print(values_to_update)

    if side == 'left':
        print('values left side')
        print(values_to_update)

    for key, value in values_to_update.items():
        client.update_unique_variable(key, value)

    

def read_warehouse_entry_right(client):


    values_to_read = [  'GVL.ART1_S',
                        'Fabrica.tapetelinear_ART1.piece.piece_id',
                        'Fabrica.tapetelinear_ART1.piece.transformation', 
                        'Fabrica.tapetelinear_ART1.piece.done', 'Fabrica.tapetelinear_ART1.piece.piece_type' ]

    values = client.read_variables(values_to_read)

    if values['GVL.ART1_S']:

        with session_manager() as session:

            if values['Fabrica.tapetelinear_ART1.piece.piece_id']:

                id = values['Fabrica.tapetelinear_ART1.piece.piece_id']
                piece = Piece(piece_id = id).object_get(session)

                piece_type = values_to_read['Fabrica.tapetelinear_ART1.piece.piece_type'] 
                piece.list_states.append(piece_type)

                session.merge(piece)
                session.commit()

            else:
                
                piece_type = values_to_read['Fabrica.tapetelinear_ART1.piece.piece_type']
                piece = Piece()

                piece.list_states = [piece_type]

                piece.object_add(session)
                
    
    client.update_unique_variable('GVL.ART1_I', True)



def read_warehouse_entry_left(client):

    values_to_read = [  'GVL.ALT5_S',
                        'Fabrica.tapetelinear_ALT5.inf_tapete.piece_id', 
                        'Fabrica.tapetelinear_ALT5.inf_tapete.transformation', 
                        'Fabrica.tapetelinear_ALT5.inf_tapete.done', 
                        'Fabrica.tapetelinear_ALT5.inf_tapete.piece_type',
                        'Fabrica.tapetelinear_ALT5.inf_tapete.unload' ]

    values = client.read_variables(values_to_read)

    if values['GVL.ALT5_S']:

        with session_manager() as session:

            if values['Fabrica.tapetelinear_ALT5.inf_tapete.piece_id']:

                id = values['Fabrica.tapetelinear_ALT5.inf_tapete.piece_id']
                piece = Piece(piece_id = id).object_get(session)

                piece_type = values['Fabrica.tapetelinear_ALT5.inf_tapete.piece_type'] 
                piece.list_states.append(piece_type)

                session.merge(piece)
                session.commit()

            else:
                
                piece_type = values['Fabrica.tapetelinear_ALT5.inf_tapete.piece_type']
                piece = Piece()

                piece.list_states = [piece_type]

                piece.object_add(session)
                

    client.update_unique_variable('GVL.ALT5_I', True)


def vacancies_right(client):

    variables = [   'Right_Cell_Control.contador1_right', 
                    'Right_Cell_Control.contador2_right' ]

    state = client.read_variables(variables)
    state['1'] = state.pop('Right_Cell_Control.contador1_right')
    state['2'] = state.pop('Right_Cell_Control.contador2_right')

    return state


def vacancies_left(client):

    variables = ['Left_Cell_Control.contador2_left', 'Left_Cell_Control.contador3_left']

    state = client.read_variables(variables)

    state['2'] = state.pop('Left_Cell_Control.contador2_left')
    state['3'] = state.pop('Left_Cell_Control.contador3_left')

    return state





