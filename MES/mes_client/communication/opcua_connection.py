from opcua import Client
from opcua import ua

class StartClient:
    
    def __init__(self, endpoint):
        self.client = Client(endpoint)


    def __enter__(self):
        self.client.connect()
        return self

    def read_variables(self, variaveis_para_ler):
        
        node_list = list()

        for key in variaveis_para_ler:
            
            val = self.client.get_node(f"ns=4;s=|var|CODESYS Control Win V3 x64.Application.{key}")
            
            #print(val.get_data_type_as_variant_type())
            
            node_list.append(val)

        return  {
            variaveis_para_ler[i] : value
            for i, value in enumerate(self.client.get_values(node_list))
        }

        

    def update_variables(self, lista_de_updates):

        nodes, values, types = [], [], []

        for key, value in lista_de_updates.items():
            
            node = self.client.get_node(f"ns=4;s=|var|CODESYS Control Win V3 x64.Application.{key}")
            nodes.append(node)
            values.append(value)
        
        self.client.set_values(nodes, values)


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.disconnect()


    def update_unique_variable(self, key, value):

        node = self.client.get_node(f"ns=4;s=|var|CODESYS Control Win V3 x64.Application.{key}")

        type = node.get_data_type_as_variant_type()

        node.set_value(value, type)
