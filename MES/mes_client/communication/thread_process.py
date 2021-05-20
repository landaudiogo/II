import threading
import signal
import sys

from .mes_erp import thread2
from .mes_plc import thread1



class ThreadSafeList:
    """Created to share resources between threads in a controlled manner,
    allowing for atomic operations without the threads disagreeing with the
    value of a provided object at a given instance

    """


    def __init__(self):
        self.lock = threading.Lock()


    def list_init(self, initial_list): 
        """This function is used to write the first elements of a list. 

        This function call occurs on the second thread's start up to insert the
        elements that already exist in the database

        """
        
        with self.lock:
            self.list = initial_list


    def extend(self, element_list):
        """This function is to be used by thread2 to update one of the lists as
        they are sent by the ERP

        """
        if not getattr(self, 'list', None):
            self.list_init([])

        with self.lock:
            self.list.extend(element_list)


    def read(self):
        """This function is used by the second thread to read the elements in
        the list

        """

        with self.lock: 
            if not getattr(self, 'list', None): 
                return None
            return self.list

shared_lock = threading.Lock()

thread_mes_plc = threading.Thread(
    target=thread1, 
    args=(shared_lock,),
    daemon=True
)
thread_mes_erp = threading.Thread(
    target=thread2, 
    args=(shared_lock,),
    daemon=True
)

thread_mes_plc.start()
thread_mes_erp.start()


def signal_handler(sig, frame):
    with shared_lock:
        print('Closing safely')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
while True: 
    pass

