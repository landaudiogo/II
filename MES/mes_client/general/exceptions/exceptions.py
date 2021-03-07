from flask import Response
from jsonpickle import encode, decode


class NotFound(Exception):
    def __init__(self, message=None):
        self.message = message if message != None else self.__class__.__name__
        super().__init__(self.message)

    def __getstate__(self):
        d = {
            'error': self.message,
        }
        return d

    def response(self):
        return Response(response=encode(self, unpicklable=False), status=404)


class FailedTokenValidation(Exception):
    def __init__(self, message=None):
        self.message = message if message != None else self.__class__.__name__
        super().__init__(self.message)

    def __getstate__(self):
        d = {
            'error': self.message,
        }
        return d

    def response(self):
        return Response(response=encode(self, unpicklable=False), status=401)


class DatabaseException(Exception):
    def __init__(self, orig, message=None):
        self.orig = orig
        self.message = message if message != None else self.__class__.__name__
        super().__init__(self.message)

    def __getstate__(self):
        d = {
            'error': self.message,
            'database': str(self.orig)
        }
        return d

    def response(self):
        return Response(response=encode(self, unpicklable=False), status=400)


class MissingData(Exception):
    def __init__(self, data_missing, message=None):
        self.data_missing = data_missing
        self.message = message if message != None else self.__class__.__name__
        super().__init__(self.message)

    def __getstate__(self):
        d = {
            'error': self.message,
            'data_missing': self.data_missing
        }
        return d

    def response(self):
        return Response(response=encode(self, unpicklable=False), status=400)



class UnexpectedParameter(Exception):
    def __init__(self, parameter, message=None):
        self.parameter = parameter
        self.message = message if message != None else self.__class__.__name__
        super().__init__(self.message)

    def __getstate__(self):
        d = {
            'error': self.message,
            'parameter': self.parameter
        }
        return d

    def response(self):
        return Response(response=encode(self, unpicklable=False), status=400)


class NotUniqueIdentifier(Exception):
    def __init__(self, name, message=None):
        self.name = name
        self.message = message if message != None else self.__class__.__name__
        super().__init__(self.message)

    def __getstate__(self):
        d = {
            'error': self.message,
            'received': decode(encode(self.name, unpicklable=False))
        }
        return d

    def response(self):
        return Response(response=encode(self.name, unpicklable=False), status=404)


class WrongFunctionInput(Exception):
    def __init__(self, message=None):
        self.message = message if message != None else self.__class__.__name__
        super().__init__(self.message)

    def __getstate__(self):
        d = {
            'error': self.message,
        }
        return d

    def response(self):
        return Response(reponse=encode({'error': 'Internal server error occurred'}), status=500)


class MissingFunctionParameters(Exception):
    def __init__(self, parameter=None, message=None):
        self.message = message if message != None else self.__class__.__name__
        self.parameter=parameter
        super().__init__(self.message)

    def __getstate__(self):
        d = {
            'error': self.message,
            'parameter': self.parameter
        }
        return d

    def response(self):
        return Response(reponse=encode({'error': 'Internal server error occurred'}), status=500)
