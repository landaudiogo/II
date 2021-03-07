from ..exceptions import TypeException

def verify_input(received_object, expected_type):
    if not isinstance(received_object, expected_type): 
        raise TypeException(
            expected_type = f'{expected_type.__name__}', 
            message       = f'Expected an instance of {expected_type.__name__}, Input was {received_object.__class__.__name__}'
        )

    return True
