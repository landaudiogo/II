from path import Graph, Node

node_list = [Node(f'P{i}') for i in range(1,10)]
for i in range(6):
    node_list[i].add_node_next(node_list[i+1])
node_list[4].add_node_next(node_list[8])
node_list[5].add_node_next(node_list[7])

G = Graph(node_list)
print(G.find_path('P2', 'P9'))
