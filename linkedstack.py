"""
File: linkedstack.py

This module defines a LinkedStack class.
"""

from node import Node
from abstractstack import AbstractStack
from typing import Iterable


class LinkedStack(AbstractStack):
    """A link-based stack implementation using a singly linked
    sequence of nodes.
    """

    def __init__(self, source_collection=None):
        """Sets the initial state of self, which includes the contents 
        of source_collection, if it's present.
        """
        self._items = None
        AbstractStack.__init__(self, source_collection)

    def peek(self):
        """Returns the item at the top of the stack, 
        otherwise raises KeyError if the stack is empty.
        """
        if self.is_empty():
            raise KeyError("The stack is empty")
        return self._items.data

    def __iter__(self) -> Iterable[list]:
        """Supports iteration over a view of self."""
        
        def visit_nodes(node: Node):
            """Adds items to temp_list from tail to head."""
            if node is not None:
                visit_nodes(node.next)
                temp_list.append(node.data)
                
        temp_list = list()                
        visit_nodes(self._items)
        return iter(temp_list)

    def clear(self):
        """Clears the stack."""
        self._size = 0
        self._items = None

    def push(self, item):
        """Adds item to the top of the stack."""
        self._items = Node(item, self._items)
        self._size += 1

    def pop(self):
        """Removes and returns the item at the top of the stack,
        otherwise raises KeyErorr if the stack is empty.
        """
        if self.is_empty():
            raise KeyError("The stack is empty")
        data = self._items.data
        self._items = self._items.next
        self._size -= 1
        return data