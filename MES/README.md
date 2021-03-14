# MES

Manufacturing Execution System


## Class Diagram

### Database Package

### Communication Package

## Sequence Diagram Process 2

When an order is received it would be convenient if there were a way of communicating between the 2 processes.

To run the 2 processes, we can use the multiprocess python module, which allows to share memory between processes, and to run these processes in parallel.

Because sharing a list of transformations would be too complex for the multiprocessing manager, a simple boolean variable is proposed, to which the second process writes when there is a new order entering, and the second process is always checking whether this value is set to true.


### Transform Order

1. Receive the Order
2. Create an Order object
3. Create the Transform Object
4. Re-prioritize the Transformations based on a cost
5. Populate the database

### Unload Order

1. Receive the Order
2. Create an Order object
3. Create the Unload Object
4. Populate the database

## Sequence Diagram Process 1

This process is responsible for interacting with the PLC. 

On start up, the process must first fetch the prioritized order, and the do the simple polling operation.

1 unit of time is the time granularity our MES is aware of, and performs it's operations at rates defined by multiples of this value.

To be discussed: 
- How periodic do we want our application to be? 
	- synchronous communication, and after successfully performing the communication we count the units of time for the next execution?
	- asynchronous communication, and everytime the unit of time trigger occurs we start the operations.

> asynchronous programming in python:
> https://realpython.com/async-io-python/
> 
> asynchronous opc-ua
> https://github.com/FreeOpcUa/opcua-asyncio
>
> threading in python
> https://realpython.com/intro-to-python-threading/#what-is-a-thread
 

### Simple polling operation

This is a periodic operation, and occurs every 1 unit of time.


1. Determine the next piece to be sent from the list of prioritized transformations
2. Read the PLC state
	- Reading all component's piece address to determine which piece is where in the wearhouse (location)
3. Write to the PLC values
	- Writing to the wearhouse address


### Fetch the Prioritized Orders 

This operation would occur every 10 units of time

1. Fetch the ordered transformations from the database
2. store the values in a list which is accessed by the whole process.


