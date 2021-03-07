from flask import request
from contextlib import contextmanager

from ...models import Session, User
from ..endpoints import request_metadata
from ..exceptions import DataException
from ..utils import (
    verify_input,
    response_generate_ok,
    response_generate_exception,
    token_required,
)




@contextmanager
def session_manager():
    session = Session()
    try:
        yield session
    except Exception as e:
        raise e
    finally:
        session.close()


class ResourceEndpoints:
    """Creates Endpoints for a given resource which by dafault will have
    similar behaviours.

    """

    def __init__(
        self, 
        resource_cls, 
        blueprint_mod,
    ):
        self.resource_cls = resource_cls
        self.blueprint_mod = blueprint_mod

    def get(self): 
        obj_dict = request.args
        try:
            with session_manager() as session:
                obj = self.resource_cls(**obj_dict)
                obj.primary_key_set()
                obj = obj.object_get(session)
                return response_generate_ok(body=obj, status_code=200)
        except Exception as e:
            return response_generate_exception(e)

    def post(self): 
        obj_dict = request.get_json(silent=True)
        try: 
            verify_input(obj_dict, dict)
            obj = self.resource_cls(**obj_dict)
            with session_manager() as session: 
                obj.object_add(session)
                return response_generate_ok(body={}, status_code=201)
        except Exception as e:
            return response_generate_exception(e)

    def patch(self):
        obj_dict = request.get_json(silent=True)
        try:
            with session_manager() as session: 
                verify_input(obj_dict, dict)
                obj=self.resource_cls(**obj_dict)
                obj.object_update(session)
                return response_generate_ok(body={}, status_code=200)
        except Exception as e:
            return response_generate_exception(e)


    def delete(self):
        obj_dict = request.args
        try: 
            with session_manager() as session:
                obj = (
                    self.resource_cls(**obj_dict)
                    .object_get(session)
                )
                obj.object_remove(session)
                return response_generate_ok(body={}, status_code=200)
        except Exception as e:
            return response_generate_exception(e)


    def post_resources(self):
        try: 
            obj_dict = request.get_json(silent=True)
            if not obj_dict:
                raise DataException(
                    data_exception_type='Missing Body',
                    message='Body required when attempting to POST',
                    status_code=422,
                )
            request_metadata.REQUESTING_USER = User(**token_required())            
            verify_input(obj_dict, dict)
            obj = self.resource_cls(**obj_dict)
            print(obj)
            with session_manager() as session: 
                obj.object_insert_or_nothing(session)
                return response_generate_ok(status_code=201)
        except Exception as e: 
            # raise e
            return response_generate_exception(e)

    def get_substrings(self): 
        try: 
            request_metadata.REQUESTING_USER = User(**token_required())            
            params = request.args
            obj = self.resource_cls(**params)
            with session_manager() as session: 
                list_objs_query = obj.object_get_attr_substrings(session)
                list_objs = list_objs_query.all() if list_objs_query else []
            return response_generate_ok(body=list_objs, status_code=200)
        except Exception as e: 
            raise e
            return response_generate_exception(e)


    def setup_endpoint(
        self, 
        appending_url,
        unique_name,
        function, 
        methods
    ):
        self.blueprint_mod.add_url_rule(appending_url, unique_name, function, methods=methods)


    def setup_default(self):
        self.setup_endpoint('/', f'{self.resource_cls.__name__}_GET', self.get, methods=['GET'])
        self.setup_endpoint('/', f'{self.resource_cls.__name__}_POST', self.post, methods=['POST'])
        self.setup_endpoint('/', f'{self.resource_cls.__name__}_PATCH', self.patch, methods=['PATCH'])
        self.setup_endpoint('/', f'{self.resource_cls.__name__}_DELETE', self.delete, methods=['DELETE'])

