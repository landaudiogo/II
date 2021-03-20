from time import sleep

def thread1(list_transformations, list_unloads):
    while True: 
        transformations = list_transformations.read()
        print(transformations)
        unloads = list_unloads.read()
        print(unloads)
        sleep(0.5)
    return
