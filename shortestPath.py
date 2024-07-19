import storeLayout
from math import inf

shortestPathsList = []



def dijkstrasShortestPath(graph, paths):
    """
    Finds the distances of all provided paths.
    
    Args:
        graph: the graph, stored as an adjency matrix
        paths: A list of pathways in the graph

    Returns:
        a list of paths, with the last element being the distance travelled in that path

    """
    for path in paths:
        path.reverse()
        distance = 0 
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            distance += graph[u][v]
        path.append(distance)
    return paths

        
            

#the reasoning for this is that it's slower initially but then you dont need to run a prize collecting travelling salesman problem every time. just run through the list. O(n) > O(n^2 2^n)
def all_paths(graph, min_len=3, path=None):
    """
    Finds all possible paths in the graph

    Args:
        graph: the graph, stored as an adjency matrix
        min_len: the minimum length of paths to return. Default is 3.
        path: used in recursion. Leave empty
    """
    if not path:
        for source in range(len(graph)):
            yield from all_paths(graph, min_len, [source])
    else:
        if len(path) >= min_len: yield path
        current = path[-1]
        for next_node in range(len(graph)):
            if next_node in path: return #dont want to visit a node twice
            if graph[current][next_node] != 0: yield from all_paths(graph, min_len, path + [next_node])

def findOptimalPath(shelfs):
    """
    Finds the optimal path to take for a list of shelves

    Args:
        shelfs: the list of shelfs needed to visit

    Returns:
        The optimal path to take to visit all shelves in the least distance
    """
    #fix shelf numbers. strip leading zero and subtract 1
    shelfsFixed = []
    for shelf in shelfs:
        shelfsFixed.append(int(shelf) - 1)
    shelfsFixed.sort()
    minDistance = 999999999 #i hate python
    optimalPath = None
    shortestPathsList = dijkstrasShortestPath(storeLayout.layout, list(all_paths(storeLayout.layout)))
    for path in shortestPathsList:
        distance = path[-1]
        path.pop()
        validPath = True

        for shelf in shelfsFixed:
            if shelf not in path:
                validPath = False
        #all shelves in path
        if distance < minDistance and validPath: 
            optimalPath = path
            minDistance = distance
    return optimalPath
        


#print(list(all_paths(storeLayout.layout)))
shorestPathsList = dijkstrasShortestPath(storeLayout.layout, list(all_paths(storeLayout.layout)))
#print(shorestPathsList)
#print(dijkstrasShortestPath(storeLayout.layout))

