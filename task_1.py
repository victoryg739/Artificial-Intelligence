import json
import heapq

#constants
START = '1'
END = '50'

def load_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)
    
def ucs(graph, dist, cost, start, end):
    path = []
    pq = []
    parent = {}
    dist_from_source = {}
    energy_from_source = {}
    
    dist_from_source[start] = 0
    energy_from_source[start] = 0
    parent[start] = "-1"
    heapq.heappush(pq, (0, start)) #pushing start node to pq

    while pq:
        g_cost, curNode = heapq.heappop(pq)
        if(curNode == end): #reached goal
            break
        
        for neighbour in graph[curNode]:
            pair = curNode + ',' + neighbour
            g_cost = dist_from_source[curNode] + dist[pair] #g cost to neighbour node via cur node
            energy_cost = energy_from_source[curNode] + cost[pair] #real energy cost to neighbour node via cur node

            if(neighbour not in dist_from_source): #node has not been generated before
                dist_from_source[neighbour] = g_cost
                energy_from_source[neighbour] = energy_cost
                parent[neighbour] = curNode
                heapq.heappush(pq, (g_cost, neighbour))
            elif(neighbour in dist_from_source): #node has been generated from another parent (expanded node) before
                if(dist_from_source[neighbour] > g_cost): #g cost to the node is a longer path via the prev parent.. we will go through cur node instead since h_cost is the same
                    dist_from_source[neighbour] = g_cost
                    energy_from_source[neighbour] = energy_cost
                    parent[neighbour] = curNode
                    heapq.heappush(pq, (g_cost, neighbour))

    #building the full path
    curNode = end
    while curNode != "-1":
        path.append(curNode)
        curNode = parent[curNode]
    path.reverse()

    #printing results
    print("Shortest path:", "->".join(path))
    print("Shortest distance:", dist_from_source[end])
    print("Total energy cost:", energy_from_source[end])
    print()

#Main Execution
#loading files
graph = load_data("G.json")
cost = load_data("Cost.json")
dist = load_data("Dist.json")

print("------ Task 1: UCS ------")
ucs(graph, dist, cost, START, END)