"""
File: model.py

This module defines a GraphDemoModel class for testing graph-processing 
algorithms.
"""

from graph import LinkedDirectedGraph


class GraphDemoModel():
    """The model class for the application includes methods to create a
    graph and run a graph-processing algorithm.
    """

    def __init__(self):
        self._graph = None
        self._start_label = None

    def create_graph(self, rep: str, start_label: str) -> str:
        """Creates a graph from rep and start_label. Returns a message 
        if the graph was successfully created, or an error message 
        otherwise.
        """
        self._graph = LinkedDirectedGraph()
        self._start_label = start_label
        edge_list = rep.split()
        for edge in edge_list:
            # Disconnected vertex
            if not '>' in edge:
                # A disconnected vertex
                if not self._graph.contains_vertex(edge):
                    self._graph.add_vertex(edge)
                else:
                    self._graph = None
                    return "Error: Duplicate vertex"
            # Two vertices and an edge
            else:
                bracket_pos = edge.find('>')
                colon_pos = edge.find(':')
                if (bracket_pos == -1 or colon_pos == -1 or
                    bracket_pos > colon_pos):
                    self._graph = None
                    return "Error: Problem with > or :"
                from_label = edge[:bracket_pos]
                to_label = edge[bracket_pos + 1 : colon_pos]
                weight = edge[colon_pos + 1 :]
                if weight.isdigit():
                    weight = int(weight)
                if not self._graph.contains_vertex(from_label):
                    self._graph.add_vertex(from_label)
                if not self._graph.contains_vertex(to_label):
                    self._graph.add_vertex(to_label)
                if self._graph.contains_edge(from_label, to_label):
                    self._graph = None
                    return "Error: Duplicate edge"
                self._graph.add_edge(from_label, to_label, weight)
        vertex = self._graph.get_vertex(start_label)
        if vertex is None:
            self._graph = None
            return "Error: Start label not in graph"
        else:
            vertex.set_mark()
            return "Graph created successfully"

    def get_graph(self):
        """Returns the string rep of the graph, 
        or None if it is unavailable.
        """
        if not self._graph:
            return None
        else:
            return str(self._graph)

    def get_start_label(self) -> str:
        """Returns the starting label."""
        return self._start_label

    def run(self, algorithm):
        """Runs the given algorithm on the graph and returns its result, 
        or None if the graph is unavailable.
        """
        if self._graph is None:
            return None
        else:
            return algorithm(self._graph, self._start_label)