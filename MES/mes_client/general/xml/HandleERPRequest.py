import xmltodict
from jsonpickle import decode
import json

def parseXML(xml_string, force_list=()) -> dict: 
    xml_obj = decode(
        json.dumps(
            xmltodict.parse(xml_string, force_list=force_list)
        )
    )
    return handle_object(xml_obj)

def handle_object(obj):
    if isinstance(obj, dict):
        ret_dict = dict()
        for key, value in obj.items(): 
            print(key, value)
            if key[0] == '#': 
                continue
            elif key[0] == '@':
                ret_dict[key[1:].lower()] = handle_object(value)
            else: 
                ret_dict[key.lower()] = handle_object(value)
        return ret_dict

    if isinstance(obj, list): 
        ret_list = []
        for item in obj: 
            ret_list.append(handle_object(item))
        return ret_list

    else: 
        return obj
