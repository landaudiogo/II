from sqlalchemy.inspection import inspect

from typing import Type

from ...config      import Base
from ..exceptions   import DataException
from ..utils        import verify_input


def convert_to_type(string, col_type):
    col_type_string = col_type.__class__.__name__
    if col_type_string == 'INTEGER': 
        return int(string)
    if col_type_string == 'Integer': 
        return int(string)
    if col_type_string == 'TEXT':
        return string
    if col_type_string == 'ARRAY':
        return list(string)
    if col_type_string == 'BOOLEAN':
        return bool(string)
    print(string, col_type_string)
    raise NotImplementedError()




class MixinsClass:

    @classmethod
    def _class_init(cls):
        if not cls.cls_metadata_set:
            cls.cls_metadata_set = True
            cls.table = cls.__table__
            cls.schema = cls.__table_args__['schema']
            cls.primary_keys = cls._class_primary_key()
            cls.foreign_keys = cls._class_foreign_keys()
            cls.columns = cls._class_column_names()
            cls.relationships = cls._class_relationship_class_dict()
            cls.attributes = cls._class_attributes()
            cls.foreign_key_relationship = cls._class_foreign_key_relationship()
        elif not cls.cls_relationships_data:
            cls.cls_relationships_data = True
            cls.relationships_columns = cls._class_relationships_columns()


    def __init__(self: Type[Base], **kwargs: dict):
        """Initializes the calling object with the keyword arguments provided. 
        The resulting object will contain all relationships specified as well if
        provided in the keyword arguments

        Input
        -----
        :kwargs: keyword arguments which match the Class's instance 
                attributes;
        """

        verify_input(self, Base)
        object_dictionary = self.__process_input(**kwargs)
        for key, value in object_dictionary.items():
            # 1. Key is belongs to the caller's columns
            if key in self.columns:
                col_type = getattr(getattr(self.__class__, key), "type")
                value = convert_to_type(value, col_type)
                setattr(self, key, value)

            # 2. Key is a relationship name
            elif key in self.relationships.keys():
                relationship_cls    = self.relationships[key]
                local_common_fkeys  = self._foreign_keys_from_table(relationship_cls.table)
                for fkey, table_pointed in local_common_fkeys.items():                                       
                    setattr(
                        self, 
                        fkey, 
                        value.get(table_pointed['referenced_column_name'])
                    )

                relationship_common_fkeys = relationship_cls._foreign_keys_from_table(self.table)
                add_attrs = {fkey: object_dictionary.get(table_pointed['referenced_column_name'])
                    for fkey, table_pointed in relationship_common_fkeys.items()
                }
                if getattr(self.__class__, key).property.uselist == True:
                    verify_input(value, list)
                    setattr(self, key, [])
                    for second_layer_object in value:
                        verify_input(second_layer_object, dict)
                        collection_object = relationship_cls(**second_layer_object, **add_attrs)
                        getattr(self, key).append(collection_object)
                elif getattr(self.__class__, key).property.uselist == False:
                    verify_input(value, dict)
                    setattr(
                        self, key, relationship_cls(**value, **add_attrs)
                    )

            # 3. key does not belong to this caller
            else:
                raise DataException(
                    data_exception_type = 'Attribute Exception',
                    message             = 'Accepted Attributes: ' + ', '.join(self.attributes)
                )



    def __process_input(self, **kwargs: dict):
        """This function is used by __init__ to process input for an instance of a relational_table

        Input
        -----
        kwargs: keyword arguments passed as input to the __init__ method

        Output
        ------
        dict: All attributes defined in the final dictionary can be correctly atrtibuted to the object's attributes

        Example 
        -------
        In the following example, exercise_name and exercise_description do not belong to an Exercise_Sport instance, 
        but are passed as attributes. This is a behavious handled by this function

        Sport(**{
          sport_name: calis, 
          exercises: [
              {
                  'exercise_name': 'pull-ups'
                  'exercise_description': 'great for back'
              },
              {
                  'exercise_name': 'push-ups'
                  'exercise_description': 'great for chest'
              }
          ]
        })
        """

        # Attribute defined for relational_tables in it's class
        if getattr(self, 'association_table', False) == True:
            object_dictionary = dict()
            for key, value in kwargs.items():

                key_in_relationship_columns = [key in columns 
                    for columns in self.relationships_columns.values()
                ]
                if True in key_in_relationship_columns:
                    # 1. Determine the relationship the attribute belongs to
                    [relationship_name, relationship_class] = list(
                        self.relationships.items()
                    )[key_in_relationship_columns.index(True)]
                    object_dictionary[relationship_name] = dict(**{key: value})\
                        if object_dictionary.get(relationship_name)==None\
                        else dict(
                            **object_dictionary.get(relationship_name), 
                            **{key: value}
                        )

                    # 2. Check whether the relational table has a foreign key that points to this key
                    local_common_fkeys = self.__class__._foreign_keys_from_table(relationship_class.table)
                    for fkey, referenced in local_common_fkeys.items(): 
                        object_dictionary[fkey] = kwargs.get(referenced['referenced_column_name'])
                # The key just belongs to the relational_table
                elif key in self.columns:
                    object_dictionary[key] = value
                else: 
                    raise DataException(
                        data_exception_type = 'Attribute Exception',
                        message             = 'Accepted Attributes: ' + ', '.join(self.attributes))

            return object_dictionary
        return kwargs



    def __getstate__(self):
        """This function is used by jsonpickle.encode to determine how to convert this object to a json object"""

        return {c.name: getattr(self, c.name) 
            for c in self.__table__.columns
        }


    def __repr__(self):
        """How an instance of this class is represented when printed"""

        class_attr = {c.name: getattr(self, c.name)  if type(getattr(self, c.name))!=str else '\"'+getattr(self, c.name)+'\"'
            for c in self.__table__.columns
        }
        attr_value_string = ', '.join([f'{key}={value}' for key, value in class_attr.items()])
        return f"{self.__class__.__name__}({attr_value_string})"


    def _to_dict(self):
        return {c.name: getattr(self, c.name, None)
            for c in self.__table__.columns
                if getattr(self, c.name, None) != None
        }

    def object_getattrs(self, attrs: list) -> dict: 
        return {attr_key: getattr(self, attr_key)
            for attr_key in attrs
        }


    @classmethod
    def _class_primary_key(cls):
        return [pkey.name for pkey in cls.__table__.primary_key.columns]

    @classmethod
    def _class_column_names(cls):
        return [c.name for c in cls.__table__.columns]


    @classmethod
    def _class_foreign_keys(cls: Type[Base]) -> dict:
        """Provides a dictionary containing the foreign key string and information
        regarging the original pointed at column

        Output
        ------
        - foreign key string:  xxx
            - referenced table string: yyy 
              referenced column name: zzz
        ...
        """

        return {
            f_key.parent.name: {
                'referenced_table': f_key._column_tokens[1],
                'referenced_column_name': f_key._column_tokens[2]
            }
            for f_key in cls.__table__.foreign_keys
        }


    @classmethod
    def _class_foreign_key_relationship(cls: Type[Base]) -> dict:
        """Based on the attribute relationship each foreign_key contains, this
        function returns the foreign_key - relationship association

        Output
        ------
        - foreign key string: relationship string associated
        ...
        """

        return {f_key.parent.name: getattr(cls, f_key.parent.name)._relationship
            for f_key in cls.__table__.foreign_keys
        }



    @classmethod
    def _class_relationship_class_dict(cls) -> dict:
        return {key: value.mapper.class_ 
            for key, value in cls.__mapper__.relationships.items()
        }

    @classmethod
    def _class_relationships_columns(cls):
        return {key: rel_class.columns
            for key, rel_class in cls.relationships.items()
        }
        
    @classmethod
    def _class_attributes(cls):
        attributes = [c.name + ": " + c.type.__class__.__name__ 
            for c in cls.__table__.columns
        ]
        attributes.extend(
            [key+': '+value.mapper.class_.__name__ 
                for key, value in cls.__mapper__.relationships.items()
            ]
        )
        return attributes

    @classmethod
    def _foreign_keys_from_table(self, table):
        return {
            f_key.parent.name: {
                'referenced_table': f_key._column_tokens[1],
                'referenced_column_name': f_key._column_tokens[2]
            }
            for f_key in self.table.foreign_keys
                if f_key._column_tokens[1] == table.name
        }

    def print_relationships(self):
        for rel_key in self.relationships.keys():
            rel_value = getattr(self, rel_key, None)
            if rel_value:
                print(' === ' + rel_key + ' === ')
                print(rel_value)
        print('\n\n')

    def primary_key_set(self):
        """This function verifies whether the primary keys of calling object 
        are set.

        """

        for pkey in self.primary_keys:
            if getattr(self, pkey) == None:
                pkey_string = ', '.join(self.primary_keys)
                raise DataException(
                    data_exception_type='Missing Primary Key',
                    message=f'{self.__class__.__name__} is missing attributes: {pkey_string}',
                    status_code=422
                )
