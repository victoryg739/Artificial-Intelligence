import json

# Load data from JSON files
with open('G.json', 'r') as f:
    G = json.load(f)

with open('Dist.json', 'r') as f:
    Dist = json.load(f)

# Dijkstra's algorithm
def dijkstra(graph, start, end):
    # initialize distances and predecessors
    distances = {node: float('infinity') for node in graph}
    predecessors = {node: None for node in graph}
    distances[start] = 0

    nodes = list(graph.keys())

    while nodes:
        # get node with smallest distance
        current_node = min(nodes, key=lambda node: distances[node])
        nodes.remove(current_node)

        if distances[current_node] == float('infinity'):
            break

        # check if reached the destination
        if current_node == end:
            return distances[current_node], get_path(predecessors, start, end)

        # update distances for neighbors
        for neighbor in graph[current_node]:
            new_dist = distances[current_node] + Dist.get(f"{current_node},{neighbor}", float('infinity'))
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                predecessors[neighbor] = current_node

    return float('infinity'), []

def get_path(predecessors, start, end):
    path = [end]
    while path[-1] != start:
        path.append(predecessors[path[-1]])
    return path[::-1]

distance, path = dijkstra(G, '1', '50')
print("Shortest path:", "->".join(path))
print("Shortest distance:", distance)
