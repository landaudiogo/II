

class Node:


    def __init__(self, node_id):
        self.id = node_id
        self.visited = False
        self.next_nodes = []

    def add_node_next(self, next_node): 
        self.next_nodes.append(next_node)



class Graph:


    def __init__(self, node_list=[]): 
        self.node_list = node_list

    def get_node(self, node_id):
        for node in self.node_list: 
            if node.id == node_id: 
                return node
        return None

    
    def get_path(self, start, node_id_end):
        # arrived at destination
        print(start.id)
        if start.id == node_id_end: 
            return [start.id]
        
        start.visited = True
        for next_node in start.next_nodes:
            if next_node.visited == False: 
                res = self.get_path(next_node, node_id_end)
                print(res)
                if res != None:
                    res.insert(0, start.id)
                    return res
    
    def find_path(self, start_node_id, end_node_id):
        start_node = self.get_node(start_node_id)
        res = self.get_path(start_node, end_node_id)
        self.reset()
        return res
        
    def reset(self):
        for node in self.node_list: 
            node.visited = False
