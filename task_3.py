import heapq
import json

# load data from JSON files
def load_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

graph = load_data("G.json")
dist = load_data("Dist.json")
coord = load_data("Coord.json")
cost = load_data("Cost.json")

# Heuristic: euclidean distance
def heuristic(node, target):
    x1, y1 = coord[node]
    x2, y2 = coord[target]
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

# calculate the total distance of a path using the 'dist' dictionary
def get_path_distance(path, dist):
    return sum(dist[f"{path[i]},{path[i+1]}"] if f"{path[i]},{path[i+1]}" in dist else dist[f"{path[i+1]},{path[i]}"] for i in range(len(path)-1))

# Astar algo
def a_star_search(start, goal, gamma=1):
    # Initialize the open list with start node... each tuple has 3 values: 
    # 1. total estimated cost to goal.. aka f cost (score)
    # 2. actual energy to reach current node (energy_used)
    # 3. path taken to current node (path)
    open_list = [(0, 0, [start])]
    visited_edges = set()  # Set to store visited edges to avoid revisiting

    while open_list:
        score, energy_used, path = heapq.heappop(open_list) # pop lowest score from heap
        current_node = path[-1] # current node is last node in path

        # check if the current node is the goal
        if current_node == goal:
            return path, energy_used

        # expand neighbors of the current node
        for neighbor in graph[current_node]:
            if (current_node, neighbor) not in visited_edges:
                visited_edges.add((current_node, neighbor)) # prevent same edge from being taken
                visited_edges.add((neighbor, current_node))

                edge_key = f"{current_node},{neighbor}" # format string for cost dict and dist dict
                new_energy = energy_used + cost[edge_key] # total energy if traverse this edge

                # Ensure the energy used is within the budget
                if new_energy <= 287932:
                    path_dist = score + dist[edge_key]
                    h_dist = heuristic(neighbor, goal) * gamma
                    new_score = path_dist + h_dist

                    new_path = path + [neighbor]
                    heapq.heappush(open_list, (new_score, new_energy, new_path))

    return None, float('inf')

# Main execution
start, goal = '1', '50'
path, total_energy_cost = a_star_search(start, goal)

if path:
    shortest_distance = get_path_distance(path, dist)
    print(f"Shortest path: {'->'.join(path)}")
    print(f"Shortest distance: {shortest_distance}")
    print(f"Total energy cost: {total_energy_cost}")
else:
    print("No path found within the energy budget.")