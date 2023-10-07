import json
import math
import heapq

#constants
START = '1'
END = '50'
MAX_ENERGY = 287932

def load_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)
    
def astar(graph, dist, cost, coord, start, end, max_energy):
    path = []
    pq = []
    parent = {}
    dist_from_source = {}
    energy_from_source = {}
    
    dist_from_source[start] = 0
    energy_from_source[start] = 0
    parent[start] = "-1"
    nodes_expanded = 0 #counter for num of nodes expanded
    heapq.heappush(pq, (0, start)) #pushing start node to pq

    while pq:
        f_score, curNode = heapq.heappop(pq)
        nodes_expanded += 1
        if(curNode == end): #reached goal
            break
        
        for neighbour in graph[curNode]:
            pair = curNode + ',' + neighbour
            g_cost = dist_from_source[curNode] + dist[pair] #g cost to neighbour node via cur node
            energy_cost = energy_from_source[curNode] + cost[pair] #real energy cost to neighbour node via cur node
            
            if energy_cost > max_energy: #taking this path will blow our energy limit... we dont take this path
                continue

            h_cost = heuristic(coord[neighbour], coord[end])
            f_score = g_cost + h_cost

            if(neighbour not in dist_from_source): #node has not been generated before
                dist_from_source[neighbour] = g_cost
                energy_from_source[neighbour] = energy_cost
                parent[neighbour] = curNode
                heapq.heappush(pq, (f_score, neighbour))
            elif(neighbour in dist_from_source): #node has been generated from another parent (expanded node) before
                if(dist_from_source[neighbour] > g_cost): #g cost to the node is a longer path via the prev parent.. we will go through cur node instead since h_cost is the same
                    dist_from_source[neighbour] = g_cost
                    energy_from_source[neighbour] = energy_cost
                    parent[neighbour] = curNode
                    heapq.heappush(pq, (f_score, neighbour))

    #building the full path
    curNode = end
    while curNode != "-1":
        path.append(curNode)
        curNode = parent[curNode]
    path.reverse()

    #printing results
    print("Shortest path:", " -> ".join(path))
    print("Shortest distance:", dist_from_source[end])
    print("Total energy cost:", energy_from_source[end])
    print("Nodes expanded:", nodes_expanded)

def heuristic(neighbour_coord, end_coord):
    x_dist = end_coord[0] - neighbour_coord[0]
    y_dist = end_coord[1] - neighbour_coord[1]

    manhattan = abs(x_dist) + abs(y_dist)
    euclidean = math.sqrt(x_dist**2 + y_dist**2)

    average = (manhattan + euclidean) / 2 #average of manhattan and euclidean

    #return manhattan
    #return euclidean
    return average

#Main Execution
#loading files
graph = load_data("G.json")
cost = load_data("Cost.json")
dist = load_data("Dist.json")
coord = load_data("Coord.json")

print("------ Task 3: A* with energy budget ------")
astar(graph, dist, cost, coord, START, END, MAX_ENERGY)