"""
File: view.py

This module defines a GraphDemoView class for viewing the application.
"""

from model import GraphDemoModel
from algorithms import shortest_paths, span_tree, topo_sort


class GraphDemoView():
    """The view class for the application includes methods for 
    displaying the menu and receiving user commands.
    """

    def __init__(self):
        self._model = GraphDemoModel()

    def run(self):
        """Menu-driven command loop for the app."""
        menu = ("\nMain Menu\n"
                "  1  Input a graph from the keyboard\n"
                "  2  Input a graph from a file\n"
                "  3  View the current graph\n"
                "  4  Single source shortest paths\n"
                "  5  Minimum spanning tree\n"
                "  6  Topological sort\n"
                "  7  Exit the program\n")

        while True:
            command = self._get_command(7, menu)
            if command == 1: self._get_from_keyboard()
            elif command == 2: self._get_from_file()
            elif command == 3: 
                print(self._model.get_graph())
            elif command == 4:
                print("Paths:")
                for row in self._model.run(shortest_paths):
                    print(row)
            elif command == 5:
                print(f"Tree: {' '.join(map(str, self._model.run(span_tree)))}")
            elif command == 6:
                print(f"Sort: {' '.join(map(str, self._model.run(topo_sort)))}")
            else: break

    def _get_command(self, high: int, menu: str) -> int:
        """Obtains and returns a command number."""
        prompt = f"Enter a number [1-{str(high)}]: "
        command_range = list(map(str, range(1, high + 1)))
        error = f"Error: Number must be 1 to {str(high)}"
        while True:
            print(menu)
            command = input(prompt)
            if command in command_range:
                return int(command)
            else:
                print(error)

    def _get_from_keyboard(self):
        """Inputs a description of the graph from the keyboard and 
        creates the graph.
        """
        rep = ""
        while True:
            edge = input("Enter an edge [src>dest:weight] or return to quit: ")
            if edge == "": break
            rep += f"{edge} "
        start_label = input("Enter the start label: ")
        print(self._model.create_graph(rep, start_label))

    def _get_from_file(self):
        """Inputs a description of the graph from a file and creates the 
        graph.
        """
        while True:
            file_name = input("Enter the file name or return to quit: ")
            if file_name == "": break
            try:
                with open(file_name) as topo:
                    rep = topo.readline()
                    start_label = topo.readline()
                    print(self._model.create_graph(rep, start_label))
                    break
            except:
                print("Incorrect file name or path")

        
# Start up the application
GraphDemoView().run()