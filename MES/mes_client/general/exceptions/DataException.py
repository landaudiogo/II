
class DataException(Exception):
    
    def __init__(self, 
        data_exception_type='', 
        message='', 
        status_code=500
    ):
        self.message = message
        self.data_exception_type = data_exception_type
        self.status_code = status_code

    def __getstate__(self):
        return {
            'data_exception_type': self.data_exception_type,
            'message': self.message
        }

