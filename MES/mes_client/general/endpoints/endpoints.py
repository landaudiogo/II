from flask import request




class ResourceEndpoints:

    def __init__(
        self, 
        resource_cls=None, 
        blueprint_mod=None,
    ):
        self.resource_cls = resource_cls
        self.blueprint_mod = blueprint_mod
        self.setup_endpoint()

    def get(): 
        return 'get'

    def post(): 
        return 'post'

    def update():
        return 'update'

    def delete():
        return 'delete'

    def setup_enpoint(self):
        """This is the function that sets the default enpoints"""
        blueprint_mod.add_url_rule('/', f'{resource_cls.__name__}', self.get, methods=['GET'])
        blueprint_mod.add_url_rule('/', f'{resource_cls.__name__}', self.post, methods=['POST'])
        blueprint_mod.add_url_rule('/', f'{resource_cls.__name__}', self.delete, methods=['DELETE'])
        blueprint_mod.add_url_rule('/', f'{resource_cls.__name__}', self.update, methods=['UPDATE'])

