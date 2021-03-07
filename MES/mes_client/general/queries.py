

def insert_nothing_query(object_to_insert, connection):
        # CONSTRUCTING THE INSERT QUERY
        # https://stackoverflow.com/questions/34708509/how-to-use-returning-with-on-conflict-in-postgresql
        primary_string  = ', '.join(object_to_insert.primary_keys)
        column_value_pairs = object_to_insert._to_dict()
        column_keys = column_value_pairs.keys()
        columns_string = ', '.join(column_keys)

        safe_insert = [
            '%(' + cname + ')s'
            for cname in column_keys
        ]
        safe_insert_format = ', '.join(safe_insert)

        individual_condition = [
            cname + "=%(" + cname + ")s"
            for cname in column_keys
        ]
        combined_condition = ' AND '.join(individual_condition)

        query = f'''
            WITH input_rows({columns_string}) AS (
                    VALUES ({safe_insert_format}) 
                 ),
                 insert_statement AS (
                    INSERT INTO {object_to_insert.schema}.\"{object_to_insert.table.name}\" ({columns_string})
                    SELECT * FROM input_rows
                    ON CONFLICT ({primary_string}) DO NOTHING
                    RETURNING *
                 )
            SELECT *
            FROM insert_statement
            UNION ALL
            SELECT *
            FROM {object_to_insert.schema}.\"{object_to_insert.table.name}\"
            WHERE {combined_condition} 
              AND NOT EXISTS (SELECT * FROM insert_statement)
        '''
        print(query)
        res = (
            connection
            .execute(query, column_value_pairs)
            .first()
        )
        for cname in object_to_insert.columns: 
            setattr(
                object_to_insert, 
                cname, 
                res[cname]
            )


        
