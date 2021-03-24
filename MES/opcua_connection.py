from opcua import Client
from opcua import ua

class StartClient:
    
    def __init__(self, endpoint):
        self.client = Client(endpoint)

    def conectar(self):
        self.client.connect()

    def read_variables(self, variaveis_para_ler):
        
        node_list = list()

        for key in variaveis_para_ler:

            val = self.client.get_node(f"ns=4;s=|var|CODESYS Control Win V3 x64.Application.{key}")
            node_list.append(val)


        return  {
            variaveis_para_ler[i] : value
            for i, value in enumerate(self.client.get_values(node_list))
        }

        

    def update_variables(self, lista_de_updates):

        nodes, values = [], []

        for key, value in lista_de_updates.items():
            
            node = self.client.get_node(f"ns=4;s=|var|CODESYS Control Win V3 x64.Application.{key}")
            nodes.append(node)
            values.append(value)
        
        self.client.set_values(nodes, values)

    def desconectar(self):
        self.client.disconnect()


client = StartClient('opc.tcp://localhost:4840')
client.conectar()


variables = ['GVL.s1', 'GVL.s3' , 'GVL.teste']

values_to_uptade = {'GVL.teste' : 'OK', 'GVL.teste1' : 'OK'}

print(client.read_variables(variables))


client.update_variables(values_to_uptade)


client.desconectar()

