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
For one side
1. Determine the machine's that have vacancies > 0 
2. Elaborate a query which searches for the next piece to go to the shop floor:
```sql


with 
	current_final_state as (
		select 
			initial_type as current_state, 
			final_type
		from mes.transformations_machine
		where machine = 2
	),
	piece_table as (
		select 
			p.piece_id, 
			t.transform_id,
			p.piece_type as current_state,
			t.list_states[
				least(
					array_position(t.list_states, p.piece_type) + 1, 
					array_length(t.list_states,1)	
				)
			] as next_state
		from mes.piece as p
		inner join mes.transform as t 
			using (transform_id)	
	)
select p.piece_id, p.current_state, p.next_state
from piece_table as p
inner join current_final_state as c 
	on p.current_state = c.current_state 
	and p.next_state = c.final_type

```