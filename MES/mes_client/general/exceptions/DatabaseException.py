

class DatabaseException(Exception):
    def __init__(self, 
        database_exception='', 
        message='', 
        status_code=500
    ):
        self.message = message
        self.database_exception = database_exception
        self.status_code = status_code

    def __getstate__(self):
        return {
            'database_exception': self.database_exception,
            'message': self.message
        }

