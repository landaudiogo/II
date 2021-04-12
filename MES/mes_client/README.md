# MES Client

Is responsible for handling the PLC control, and tracking the existing orders
sent by the ERP

## Threads
Both threads will be in charge of different responsabilities. We separated the concerns into 2 different threads as both will be responsible with the communication with different entities. 

The first thread is responsible for communicating with the PLC, whereas the second, will handle all the communication with the ERP.

### MES_ERP

#### ERP Order

On reception of an order request, this thread is responsible for persisting the information on the database regardless of weather it is a transformation or an unload request.

On the case the order received is of transformation, there are a few additional steps to be taken. 

##### Transform

When receiving a transformation order, these are the steps to be followed: 
1. When inserting the Transformation, include the list of piece states a piece has to go through.
2. Prioritize the list of all unfinished transformations.
3. For each transformation order, determine which pieces already in the database that can be associated to a given transformation.

### mes_plc

1. Read the relevant variables to determine the machine vacancies and update the data structures holding this information.
2. For every available machine, determine the highest priority piece to leave next. 

#### Next Piece

This is a proposed solution to the problem of determining the next piece to leave onto the shop floor.

**Assumptions**
1. There is an ordered list (by priority) of the unfinished transformations.
2. Each piece has associated to itself the machine that leads it to the next transformation.
3. A datastructure that keeps track of the vacancies on a given cell.

Example of the datastructure mentioned in 3:
```python
right_cell = {
	1: 3,
	2: 0
}
lef_cell = {
	2: 0,
	3: 1
}
```

To achieve the 2nd assumption, a table is created transform_machine which indicates which machine has to be used to transform a piece from one type to another.

Each transformation also has to have associated to itself an array of piece types 
through which a piece has to go through, to reach the final state.

**Algorithm**
1. Read the variables from the PLC, which allow us to determine the vacancies in each cell of the shop floor. (pieces in the cell, machine timer's to determine if it is below the threshold)
1. Compute the machine's that have vacancies > 0 
2. Considering only the right side of the factory floor, do the next steps, until mentioned otherwise.
3. Elaborate a query which searches for the next piece to go to the shop floor:
```sql
with 
    current_final_state as (
        select 
            initial_type as current_state, 
            final_type, 
            machine
        from mes.transformations_machine
        where machine in (1)
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
select p.piece_id, p.current_state, p.next_state, c.machine
from piece_table as p
inner join current_final_state as c 
    on p.current_state = c.current_state 
    and p.next_state = c.final_type
inner join order_transform as o
	on p.transform_id = o.transform_id
where o.arrival_order = 1
order by p.priority desc, p.current_state desc
```
3. Based on the machine(s) that have vacancies, determine which is the next piece that should go onto the shop floor, by executing the query.
4. send the piece to the next piece to the warehouse.
5. considering only the left side of the shop floor, repeat steps 2 to 4.

When receiving the transformations from the erp, the following steps are preformed on all transformations


#### Piece eligibility query

This query is used to assign a piece to determine the pieces to assign to a given transformation.

For a given transformation, we search for the pieces we can assign to it which either don't belong to a given transformation, or if it does, that the assigned transformation has lower priority than the this transformation.

```sql
with 
	transformation as (
		select transform_id, list_states, priority
		from mes.transform
		where transform_id = 199
	)
select * from (
	select p.*, p.list_states[array_upper(p.list_states, 1)] as last_elem, t.priority
	from mes.piece as p 
	left join mes.transform as t using(transform_id)
	where 
		array[p.list_states[array_upper(p.list_states, 1)]] <@ (select list_states from transformation)
		and array[(select list_states[1] from transformation)] <@ p.list_states
		and coalesce(t.priority, 0) < (select priority from transformation)
) as t1
order by last_elem desc
```

the query is then used by the MES_ERP to determine which pieces to associate to a given ID limitted to a certain quantity of that transformation.

```sql
delete from mes.mes_session where true;
delete from mes.piece where true; 
delete from mes.transform where true;
delete from mes.unload where true;
delete from mes.order where true;
```

```sql
select transform_id from (
	select t.*, t.quantity - count(*) as diff
	from (
		select transform_id, list_states[1] as first_state, priority, quantity
		from mes.transform
	) as t
	inner join mes.piece as p
		using (transform_id)
	group by t.transform_id, t.first_state, t.priority, t.quantity
	order by t.priority desc
) as t1
where diff > 0
order by priority desc, diff
limit 1
```