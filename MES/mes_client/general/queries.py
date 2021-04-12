

def insert_nothing_query(object_to_insert, connection):
        # CONSTRUCTING THE INSERT QUERY
        # https://stackoverflow.com/questions/34708509/how-to-use-returning-with-on-conflict-in-postgresql
        print(object_to_insert)
        primary_string  = ', '.join(object_to_insert.primary_keys)
        column_value_pairs = object_to_insert._to_dict()
        column_keys = column_value_pairs.keys()
        column_names = [f'\"{c_name}\"' for c_name in column_value_pairs.keys()]
        columns_string = ', '.join(column_names)

        safe_insert = [
            '%(' + cname + ')s'
            for cname in column_keys
        ]
        safe_insert_format = ', '.join(safe_insert)

        individual_condition = [
            f'\"{cname}\"' + "=%(" + cname + ")s"
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


def next_piece_query(machine_list, connection):        
    str_list = [str(elem) for elem in machine_list]
    machine_list_str = ', '.join(str_list)
    query = f'''
        with 
            current_final_state as (
                select 
                    initial_type as current_state, 
                    final_type, 
                    machine
                from mes.transformations_machine
                where machine in ({machine_list_str})
            ),
            piece_table as (
                select 
                    p.piece_id, 
                    t.transform_id,
                    p.list_states[array_upper(p.list_states, 1)] as current_state,
                    t.priority,
                    t.list_states[ -- indexing the array
                        least(
                            array_position(
                                                        t.list_states, 
                                                        p.list_states[array_upper(p.list_states, 1)]
                                                ) + 1, 
                            array_length(t.list_states,1)   
                        )
                    ] as next_state
                from mes.piece as p
                inner join mes.transform as t 
                    using (transform_id)    
            ), 
            order_transform as (
                select 
                    transform_id, 
                    order_number,
                    row_number() over(
                            partition by order_number order by transform_id
                    ) as arrival_order
                from mes.transform
                where processed = false
            )
        select p.piece_id as id, p.current_state as piece_type, c.machine as machine
        from piece_table as p
        inner join current_final_state as c 
            on p.current_state = c.current_state 
            and p.next_state = c.final_type
        inner join order_transform as o
                on p.transform_id = o.transform_id
        where o.arrival_order = 1
        order by p.priority desc, p.current_state desc
    '''

    res = (
        connection
        .execute(query)
        .first()
    )
    return res[0]

def order_quantity_query(order_number, connection):
    query = f"""
        select order_number, sum(quantity) as total_quantity
        from mes.transform
        where order_number = {order_number}
        group by order_number        
    """
    res = (
        connection
        .execute(query)
        .first()
    )
    print(res)
    return res['total_quantity']



def pieces_for_transformation_query(transform_id, quantity, connection):
    query = f"""
        with 
	transformation as (
		select transform_id, list_states, priority
		from mes.transform
		where transform_id = {transform_id}
	)
        select * from (
                select p.*, p.list_states[array_upper(p.list_states, 1)] as last_elem, t.priority
                from mes.piece as p 
                left join mes.transform as t using(transform_id)
                where 
                        array[p.list_states[array_upper(p.list_states, 1)]] <@ (select list_states from transformation)
                        and array[(select list_states[1] from transformation)] <@ p.list_states
                        and coalesce(t.priority, 0) < (select priority from transformation)
                        and coalesce(t.processed, false) = false
        ) as t1
        order by last_elem desc
        limit {quantity}
    """
    res = (
        connection
        .execute(query)
    )
    return [row['piece_id'] for row in res]


def unset_pieces_query(transform_id, piece_ids, connection):
    if not piece_ids: 
        return
    list_string = ', '.join([str(piece) for piece in piece_ids])
    query = f"""
        update mes.piece
        set transform_id = null 
        where not piece_id in ({list_string})
        and transform_id = {transform_id}
    """
    res = (
        connection
        .execute(query)
    )



