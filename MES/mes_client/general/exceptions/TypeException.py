
class TypeException(Exception): 

    def __init__(self, expected_type='', message=''): 
        self.expected_type  = expected_type
        self.message        = message

