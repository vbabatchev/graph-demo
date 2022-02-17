"""
File: algorithms.py

This module contains methods that implement depth-first traversal, the 
topological sort, minimum spanning tree and single-source shortest paths 
graph processing algorithms. Also includes methods for working with
infinity.
"""

from linkedstack import LinkedStack
from arrayheap import ArrayHeap
from node import Node

INFINITY = "-"


def topo_sort(graph, start_label: str = None) -> LinkedStack:
    """Returns a stack of vertices representing a topological order of
    vertices in the graph.
    """  
    stack = LinkedStack()
    graph.clear_vertex_marks()
    for vertex in graph.get_vertices():
        if not vertex.is_marked():
            dfs(graph, vertex, stack)
    return stack


def dfs(graph, vertex: Node, stack: LinkedStack):
    """Recursive depth-first traversal."""
    vertex.set_mark()
    stack.push(vertex)
    for neighbor in graph.neighboring_vertices(vertex.get_label()):
        if not neighbor.is_marked():
            dfs(graph, neighbor, stack)


def shortest_paths(graph, start_label: str) -> list[list]:
    """Returns a two-dimensional grid of N rows and three columns, 
    where N is the number of vertices. The first column contains the 
    vertices. The second column contains the distance from the start 
    vertex to this vertex. The third column contains the immediate 
    parent vertex of this vertex, if there is one, or None otherwise.
    """

    # Initialization Step
    n = len(graph)
    included = [False] * n
    results = [[None] * 3 for i in range(n)]
    source = graph.get_vertex(start_label)
    row = 0
    for vertex in graph.get_vertices():
        to_vertex = vertex.get_label()
        results[row][0] = to_vertex
        if vertex == source:
            results[row][1] = 0
            included[row] = True
        elif graph.contains_edge(start_label, to_vertex):
            weight = source.get_edge_to(vertex).get_weight()
            results[row][1] = weight
            results[row][2] = start_label
        else:
            results[row][1] = INFINITY
        row += 1

    # Computation Step
    while False in included:
        f = results[included.index(False)]
        for i in range(n):
            if not included[i] and is_less_with_infinity(results[i][1], f[1]):
                f = results[i]
        included[results.index(f)] = True
        for i in range(n):
            if not included[i]:
                t = results[i]
                if graph.contains_edge(f[0], t[0]):
                    new_distance = (f[1] 
                                    + graph.get_edge(f[0], t[0]).get_weight())
                    if is_less_with_infinity(new_distance, t[1]):
                        t[1] = new_distance
                        t[2] = f[0]
    return results


def add_with_infinity(a, b):
    """If a == INFINITY or b == INFINITY, returns INFINITY.
    Otherwise, returns a + b.
    """
    if a == INFINITY or b == INFINITY: return INFINITY
    else: return a + b    


def is_less_with_infinity(a, b) -> bool:
    """If a == INFINITY, returns FALSE. If b == INFINITY, returns TRUE.
    Otherwise, returns a < b.
    """
    if a == INFINITY: return False
    elif b == INFINITY: return True
    else: return a < b


def span_tree(graph, start_label: str) -> list:
    """Returns a list containing the edges in the minimum spanning tree
    of the graph.
    """
    graph.clear_vertex_marks()
    graph.clear_edge_marks()
    vertex = graph.get_vertex(start_label)
    vertex.set_mark()
    heap = ArrayHeap()
    for edge in vertex.incident_edges():
        heap.add(edge)
    k = 1
    while k < len(graph):
        edge = heap.pop()
        w = edge.get_to_vertex()
        if not w.is_marked():
            edge.set_mark()
            w.set_mark()
            for e in w.incident_edges():
                heap.add(e)
            k += 1
    return [edge for edge in graph.edges() if edge.is_marked()]