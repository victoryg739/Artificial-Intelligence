import json
import heapq

# Load data from .json files
def load_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

graph = load_data("G.json")
Dist = load_data("Dist.json")
Cost = load_data("Cost.json")

def ucs(graph, start, end, max_energy_cost):
    # Using a priority queue to store nodes with their cumulative costs
    #Tuple contents:
    #1. total path cost to node (g cost)
    #2. node itself
    #3. path taken to reach node
    #4. total energy cost to node
    pq = [(0, start, [], 0)]
    visited = set()
    nodes_expanded = 0

    while pq:
        cost, current_node, path, energy_cost = heapq.heappop(pq)
        nodes_expanded += 1

        if current_node == end:
            return path + [end], cost, energy_cost, nodes_expanded

        if current_node in visited:
            continue

        visited.add(current_node)

        for neighbor in graph[current_node]:
            edge_key = f"{current_node},{neighbor}"
            new_cost = cost + Dist[edge_key]
            new_energy_cost = energy_cost + Cost[edge_key]

            # Check the energy constraint
            if new_energy_cost <= max_energy_cost:
                heapq.heappush(pq, (new_cost, neighbor, path + [current_node], new_energy_cost))

    return [], float('inf'), float('inf'), float('inf') # no valid path found

start_node = '1'
end_node = '50'
energy_budget = 287932

path, cost, energy_used, nodes_expanded = ucs(graph, start_node, end_node, energy_budget)
if path:
    print(f"Shortest path: {'->'.join(path)}")
    print(f"Shortest distance: {cost}")
    print(f"Total energy cost: {energy_used}")
    print("Nodes expanded:", nodes_expanded)
else:
    print(f"No feasible path found from {start_node} to {end_node} within the energy budget")