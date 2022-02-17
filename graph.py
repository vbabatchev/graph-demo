"""
File: graph.py

Classes: LinkedEdge, LinkedVertex, LinkedDirectedGraph
"""

from abstractcollection import AbstractCollection
from typing import Iterable


class LinkedEdge():
    """Represents an edge with a source vertex, destination vertex,
    weight, and mark attribute.
    """

    def __init__(self, from_vertex, to_vertex, weight=None):         
        self._src = from_vertex
        self._dest = to_vertex
        self._weight = weight 
        self._mark = False

    def clear_mark(self):
        """Clears the mark on the edge."""
        self._mark = False

    def set_mark(self):
        """Marks the edge."""
        self._mark = True
    
    def set_weight(self, weight):
        """Sets the weight on the edge to weight."""
        self._weight = weight  

    def __eq__(self, other) -> bool:
        """Two edges are equal if they connect the same vertices."""
        if self is other: return True
        if type(self) != type(other):
            return False
        return (self._src == other._src and 
                self._dest == other._dest)

    def __lt__(self, other: 'LinkedEdge') -> bool:
        """An edge is less than another edge if its weight is 
        less than the other edge's weight.
        """
        return self._weight < other._weight

    def __le__(self, other: 'LinkedEdge') -> bool:
        """An edge is less than  or equal to another edge if its weight 
        is less than or equal the other edge's weight.
        """
        return self._weight <= other._weight

    def __hash__(self):
        """Returns the hash code of the edge."""
        return hash((self._src, self._dest))
    
    def get_other_vertex(self, this_vertex):
        """Returns the vertex opposite this_vertex."""
        if this_vertex == None or this_vertex == self._dest:
            return self._src
        else:
            return self._dest

    def get_to_vertex(self):
        """Returns the edge's destination vertex."""
        return self._dest
    
    def get_weight(self):
        """Returns the weight of the edge."""
        return self._weight
    
    def is_marked(self) -> bool:
        """Returns True if the edge is marked, or False otherwise."""
        return self._mark   
          
    def __str__(self):
        """Returns the string representation of the edge."""
        return f"{str(self._src)}>{str(self._dest)}:{str(self._weight)}"


class LinkedVertex():
    """Represents a vertex that has a label, list of incident edges,
    and mark attribute.
    """

    def __init__(self, label):
        self._label = label
        self._edge_list = list()
        self._mark = False

    def clear_mark(self):
        """Unmarks the vertex."""
        self._mark = False

    def set_mark(self):
        """Marks the vertex."""
        self._mark = True

    def set_label(self, label, graph):
        """Sets the label of the vertex in graph to label."""
        graph._vertices.pop(self._label, None)
        graph._vertices[label] = self
        self._label = label          

    def get_label(self):
        """Returns the label of the vertex."""
        return self._label
    
    def is_marked(self) -> bool:
        """Returns True if the vertex is marked, or False otherwise."""
        return self._mark
     
    def __str__(self):
        """Returns the string representation of the vertex."""
        return str(self._label)

    def __eq__(self, other):
        """Two vertices are equal if they have the same labels."""
        if self is other: return True
        if type(self) != type(other): return False
        return self.get_label() == other.get_label()

    def __hash__(self):
        """Returns the hash code of the vertex."""
        return hash(self._label)

    # Methods used by LinkedGraph

    def add_edge_to(self, to_vertex: 'LinkedVertex', weight):
        """Connects self with to_vertex with an edge."""
        edge = LinkedEdge(self, to_vertex, weight)
        self._edge_list.append(edge)
    
    def get_edge_to(self, to_vertex: 'LinkedVertex'):
        """Returns the connecting edge if it exists, 
        or None otherwise.
        """
        edge = LinkedEdge(self, to_vertex)
        try:
            return self._edge_list[self._edge_list.index(edge)]
        except:
            return None

    def incident_edges(self) -> Iterable[list]:
        """Returns an iterator over the incident edges of the vertex."""
        return iter(self._edge_list)
        
    def neighboring_vertices(self) -> Iterable[list]:
        """Returns an iterator over the neighboring vertices of the 
        vertex.
        """
        vertices = list()
        for edge in self._edge_list:
            vertices.append(edge.get_other_vertex(self))
        return iter(vertices)
            
    def remove_edge_to(self, to_vertex: 'LinkedVertex') -> bool:
        """Returns True if the edge exists and is removed, 
        or False otherwise.
        """
        edge = LinkedEdge(self, to_vertex)
        if edge in self._edge_list:
            self._edge_list.remove(edge)
            return True
        else:
            return False


class LinkedDirectedGraph(AbstractCollection):
    """Represents a directed graph using an adjacency list. Accepts an
    optional collection of labels as an argument and adds vertices with
    these labels.
    """

    def __init__(self, source_collection=None):
        self._edge_count = 0
        self._vertices = {}
        AbstractCollection.__init__(self, source_collection)

    def clear(self):
        """Removes all the vertices from the graph."""
        self._size = 0
        self._edge_count = 0
        self._vertices = {}        

    def clear_edge_marks(self):
        """Clears all edge marks."""
        for edge in self.edges():
            edge.clear_mark()
    
    def clear_vertex_marks(self):
        """Clears all vertex marks."""
        for vertex in self.get_vertices():
            vertex.clear_mark()
    
    def size_edges(self) -> int:
        """Returns the number of edges in the graph."""
        return self._edge_count
    
    def size_vertices(self) -> int:
        """Returns the number of vertices in the graph."""
        return len(self)
    
    def __str__(self) -> str:
        """Returns the string representation of the graph."""
        result = f"{str(self.size_vertices())} Vertices: "
        for vertex in self._vertices:
            result += f" {str(vertex)}"
        result += "\n"
        result += f"{str(self.size_edges())} Edges: "
        for edge in self.edges():
            result += f" {str(edge)}"
        return result

    def add(self, label):
        """For compatibility with other collections."""
        self.add_vertex(label)

    # Vertex-related methods
    
    def add_vertex(self, label):
        """Adds a vertex with the given label to the graph."""
        self._vertices[label] = LinkedVertex(label)
        self._size += 1
        
    def contains_vertex (self, label) -> bool:
        """Returns True if the graph contains a vertex with the given
        label, or False otherwise.
        """
        return label in self._vertices
    
    def get_vertex(self, label):
        """Returns the vertex with the given label,
        or None of there is no such vertex.
        """
        try:
            return self._vertices[label]
        except:
            return None
    
    def remove_vertex(self,  label) -> bool:
        """Returns True if the vertex was removed, or False otherwise."""
        removed_vertex = self._vertices.pop(label, None)
        if removed_vertex is None: 
            return False
        
        """Examine all other vertices to remove edges directed at the 
        removed vertex"""
        for vertex in self.get_vertices():
            if vertex.remove_edge_to(removed_vertex): 
                self._edge_count -= 1

        # Examine all edges from the removed vertex to others
        for edge in removed_vertex.incident_edges():
            self._edge_count -= 1           
        self._size -= 1
        return True
    
    # Edge-related methods

    def add_edge(self, from_label, to_label, weight):
        """Adds an edge with the given weight between a vertex with
        from_label and a vertex with to_label.
        """
        from_vertex = self.get_vertex(from_label)
        to_vertex   = self.get_vertex(to_label)
        from_vertex.add_edge_to(to_vertex, weight)
        self._edge_count += 1
    
    def contains_edge(self, from_label, to_label) -> bool:
        """Returns True if the graph contains an edge with given weight 
        from a vertex with from_label to a vertex with to_label,
        or False otherwise.
        """
        return self.get_edge(from_label, to_label) != None
    
    def get_edge(self, from_label, to_label):
        """Returns the edge with given weight connecting the vertex with 
        from_label to the vertex with to_label, 
        or None if no edge exists.
        """
        from_vertex = self.get_vertex(from_label)
        to_vertex   = self.get_vertex(to_label)
        return from_vertex.get_edge_to(to_vertex)
    
    def remove_edge(self, from_label, to_label): 
        """Removes the edge with given weight connecting vertices with 
        from_label and to_label and returns True, 
        or False if there is no such edge.
        """
        from_vertex = self.get_vertex(from_label)     
        to_vertex   = self.get_vertex(to_label)     
        edge_removed_flg = from_vertex.remove_edge_to(to_vertex)
        if edge_removed_flg: 
            self._edgeCount -= 1
        return edge_removed_flg

    # Iterators
    
    def __iter__(self):
        """Supports iteration over a view of self (the vertices)."""
        return self.get_vertices()

    def edges(self) -> Iterable[set]:
        """Returns an iterator over the edges in the graph."""
        result = set()
        for vertex in self.get_vertices():
            edges = vertex.incident_edges()
            result = result.union(set(edges))
        return iter(result)
    
    def get_vertices(self) -> Iterable[LinkedVertex]:
        """Returns an iterator over the vertices in the graph."""
        return iter(self._vertices.values())

    def incident_edges(self, label):
        """Returns an iterator over the neighboring vertices of the
        vertex with given label.
        """
        return self.get_vertex(label).incident_edges()
    
    def neighboring_vertices(self, label):
        """Returns an iterator over the neighboring vertices of the
        vertex with given label.
        """
        return self.get_vertex(label).neighboring_vertices()