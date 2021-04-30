from sqlalchemy.sql.expression import func


from ...config import engine
from ..queries import insert_nothing_query
from ..exceptions import DatabaseException


class MixinsDatabase:


    def object_get(self, session):
        """Get a unique object using it's primary key"""

        primary_key_values = tuple(
            getattr(self, key) 
            for key in self.primary_keys
        )
        try:
            obj = session.query(self.__class__).get(primary_key_values)
            return obj
        except NotFound as nf:
            raise nf
        except Exception as e:
            if 'orig' in e.__dict__:
                raise DatabaseException(e.orig)
            raise DatabaseException(e.__class__.__name__)


    def object_add(self, session):
        """Persist calling object to the database"""

        session.add(self)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            if getattr(e, 'orig'): 
                message = e.orig.__class__.__name__
            else: 
                message = ''
            raise DatabaseException(
                database_exception=e.__class__.__name__,
                message=message,
                status_code=409
            )


    def object_update(self, session):
        """Update the calling object based on it's primary_keys, and the defined
        attributes it contains. 

        """

        session.merge(self)
        try: 
            session.commit()
        except Exception as e:
            session.rollback()
            raise DatabaseException(
                database_exception=e.__class__.__name__, 
                message=str(e)
            )


    def object_remove(self, session):
        """Remove calling object persisted in the session argument from the
        database

        """

        session.delete(self)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise DatabaseException(
                database_exception=e.__class__.__name__, 
                message=str(e)
            )


    def get_objects_using_attrs(self, session):
        """Search for an object in it's table with the attributes defined in
        it's instance. 

        Returns
        =======

        This function returns a query object which can then be used to apply
        either one of the following functions for it's intended purpose, and
        many others: one(), all(), adding filters ...

        """

        return (
            session.query(self.__class__)
            .filter(*[getattr(self.__class__, key)==value
                for key, value in self._to_dict().items()
            ])
        )

        
    def object_get_attr_substrings(self, session):
        """Using the string attributes of the object, search in the instance's 
        table for an object with matching substrings.

        For a given attribute, the search method goes through finding words that
        belong to it's column, that start with the substring provided


        Future Implementations
        ======================

        Consider implementing a fuzzy searcher

        """

        key_substrings = {c.name: getattr(self, c.name).split(' ')
            for c in self.table.columns
                if c.type.__class__.__name__ == 'VARCHAR'
                and getattr(self, c.name) != None
        }
        try:
            query_filter = [
                func.lower(getattr(self.__class__, key)).op('~')(f'[[:<:]]{sub.lower()}')
                for key, subs in key_substrings.items()
                    for sub in subs
            ]
            query = session.query(self.__class__).filter(*query_filter)
            print(query)
            return query
        except Exception as e:
            session.rollback()
            if 'orig' in e.__dict__:
                raise DatabaseException(e.orig)
            raise DatabaseException(e.__class__.__name__)
    

    def object_insert_or_nothing(self, session, connection=None, stack=[]):
        """Attempts to create the calling object and it's relationships in a
        recursive manner. 

        In the case of conflict with an existing object's primary key, nothing 
        is changed in the database. (ON CONFLICT NOTHING)

        THE FIRST CALL TO THIS OBJECT, NO PARAMETERS SHOULD BE GIVEN except for
        the session

        When calling this method, the caller has to contain all it's foreign_keys
        in the relationship's field. If this is not taken into consideration, the
        original object will be inserted with a null value in the foreign_key 
        column.

        each resource Class should contain this same method with it's own
        security concerns implemented

        There are 3 phases in this function: 
        1. Discover if the object already exists in the database
        2. Insert the relationship's the caller depends on. 
        3. Insert the relationships that haven't been added yet.

        Phase 1:
            If the primary key of the object is set, either the object already
            exists, or it id to be inserted with that key.
            In the first scenario, we copy the existing to the caller.
            In the second, the rest of the phases run normally, wihtout this
            phase having any effect on the final result.

        Phase 2: 
            Insert the foreign_keys the object depends on.

            for each foreign key in the caller's columns:
            Check whether the relationship connected to the foreign key
            exists. If the relationship exists, populate it, and insert it's
            primary keys in the caller's foreign key. 

            if the relationship connected to the foreign key does not exist, we
            populate the relationship given the foreign key already in the
            caller's column.

            In the scenario neither the relationship nor the caller foreign key is
            defined, the caller will be inserted without any foreign_keys
            defined (set to NULL).
        Phase 3: 


        Args: 
            self: expected to be an instance of a class that has inherited from
              a declarative_base class (Base) from sqlalchemy
            session: instance of Session
            connection: a connection instance from sqlalchemy that can directly 
              execute SQL strings via the connection.execute()
            stack: a list of id's of object's that have already been added to
              the database. This parameter has to be included as without an
              infinite loop could occur, with the back_populates parameter set
              in a class's relationship.
            
        """
        # creates a global connection to be used when populating each object
        # recursively
        if connection == None: 
            with engine.connect() as conn: 
                trans = conn.begin()
                MixinsDatabase.object_insert_or_nothing(self, session,
                                                        connection=conn,
                                                        stack=[])
                trans.commit()
            return

        # verify if primary keys are set. If that's the case then we shallow
        # copy the existing object to the caller
        pkey_values = {pkey: getattr(self, pkey) for pkey in self.primary_keys}
        if not (None in pkey_values.values()):
            existing_objs = (
                self.__class__(**pkey_values)
                .get_objects_using_attrs(session).all()
            )
            if len(existing_objs) > 0:
                existing_obj = existing_objs[0]
                for key, value in existing_obj._to_dict().items():
                    setattr(self, key, value)

        # insert the relationships the caller depends on (foreign keys)
        for fkey, table_pointed in self.foreign_keys.items():
            # object contains a foreign_key value
            relationship_string = getattr(self.__class__, fkey)._relationship
            relationship_ = getattr(self, relationship_string)
            if (relationship_ != None
                and id(relationship_) not in stack
            ):
                relationship_.object_insert_or_nothing(
                    session, 
                    connection=connection, 
                    stack=stack
                )
                
            # missing relationship object
            elif relationship_ == None: 
                relationship_cls = self.relationships.get(relationship_string)
                rel_dict = {
                    table_pointed['referenced_column_name']: getattr(self, fkey)
                    for fkey, table_pointed in self.foreign_keys.items()
                        if table_pointed['referenced_table'] == relationship_cls.table.name
                }
                if rel_dict and (None not in rel_dict.values()):
                    relationship_ = relationship_cls(**rel_dict)
                    relationship_.object_insert_or_nothing(
                        session, 
                        connection=connection,
                        stack=stack
                    )

            fkey_value = getattr(
                relationship_, 
                table_pointed['referenced_column_name'], 
                None
            )
            setattr(self, fkey, fkey_value)

        # insert the caller 
        if id(self) not in stack:
            insert_nothing_query(self, connection)
            stack.append(id(self))
            
        # insert the relationships related to the caller
        for rel_key in self.relationships: 
            relationship_ = getattr(self, rel_key, None)
            if getattr(self.__class__, rel_key).property.uselist == False:

                if (relationship_ != None
                    and id(relationship_) not in stack
                ): 
                    relationship_.object_insert_or_nothing(session, connection, stack)

            elif getattr(self.__class__, rel_key).property.uselist == True: 
                for obj in relationship_:
                    if (obj != None
                        and id(obj) not in stack
                    ): 
                        obj.object_insert_or_nothing(session, connection, stack)

