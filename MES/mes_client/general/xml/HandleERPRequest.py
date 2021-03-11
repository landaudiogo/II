import xmltodict
from jsonpickle import decode
import json

def parseXML(xml_string, force_list={}): 
    """Função cujo objetivo é o de converter um objeto xml para um objeto
    dictionary para ser posteriormente processado pela função de inicialização
    das Classes relacionadas com a Base de Dados
    
    Argumentos
    ----------

    xml_string: a string xml que deve ser transformado num dicionário python
    force_list: um dicionário que através das chaves indica que objetos, dentro
        da string XML, devem ser transformados para listas. Útil para as relações
        que temos definidas para um para muitos.
        E.g. 
            parseXML('''
                <Order order_number='nnn'>
                    <Transform .../>
                    <Transform .../>
                </Order>''',
                force_list={'Transform': 'transformations'}
            )

    """

    xml_obj = decode(
        json.dumps(
            xmltodict.parse(xml_string, force_list=list(force_list.keys()))
        )
    )
    return handle_object(xml_obj, substitute_keys=force_list)


def handle_object(obj, substitute_keys={}):
    """Formata `obj` por forma a que consiga ser processado pela
    função de inicialização genérica.

    Este processamento passa por remover characteres desconhecidos à função
    ('@', '#'), e por alterar as chaves do dicionário para para os attributos
    definidos em cada classe, relacionados com as colunas da base de dados.
    """

    if isinstance(obj, dict):
        ret_dict = dict()
        for key, value in obj.items(): 
            if key[0] == '#': 
                continue
            elif key[0] == '@':
                key = key[1:]
                hash_key = (
                    substitute_keys[key] 
                    if substitute_keys.get(key) 
                    else key.lower() 
                )
                ret_dict[hash_key] = handle_object(value, substitute_keys)
            else: 
                hash_key = (
                    substitute_keys[key] 
                    if substitute_keys.get(key) 
                    else key.lower()
                )
                ret_dict[hash_key] = handle_object(value, substitute_keys)
        return ret_dict

    if isinstance(obj, list): 
        ret_list = []
        for item in obj: 
            ret_list.append(handle_object(item, substitute_keys))
        return ret_list

    else: 
        return obj
