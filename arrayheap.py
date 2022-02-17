"""
File: arrayheap.py

This module defines an ArrayHeap class.
"""

from abstractcollection import AbstractCollection
from typing import Iterable

class ArrayHeap(AbstractCollection):
    """Array-based min-heap implementation of a priority queue."""

    def __init__(self, source_collection=None):
        self._heap = list()
        AbstractCollection.__init__(self, source_collection)

    def peek(self):
        """Returns the topmost item in heap, 
        otherwise raises an Exception if heap is empty.
        """
        if self.is_empty():
            raise Exception("Heap is empty")
        return self._heap[0]

    def __str__(self) -> str:
        """Returns a string that shows the shape of the heap."""
        def str_helper(position, level) -> str:
            """Assists with formatting."""
            result = ""
            if position < len(self):
                result += str_helper(2*position + 2, level + 1)
                result += "|" * level
                result += f"{str(self._heap[position])}\n"
                result += str_helper(2*position + 1, level + 1)
            return result
        return str_helper(0, 0)

    def __iter__(self) -> Iterable[list]:
        """Visits the items from least to greatest."""
        temp_list = list(self._heap)
        result_list = []
        while not self.is_empty():
            result_list.append(self.pop())
        self._heap = temp_list
        self._size = len(self._heap)
        return iter(result_list)

    def add(self, item):
        """Inserts item in its proper place in heap."""
        self._size += 1
        self._heap.append(item)
        curr_pos = len(self._heap) - 1
        while curr_pos > 0:
            parent = (curr_pos - 1)//2
            parent_item = self._heap[parent]
            # Found the spot
            if parent_item <= item:
                break
            # Continue walking up
            else:
                self._heap[curr_pos] = self._heap[parent]
                self._heap[parent] = item
                curr_pos = parent

    def pop(self):
        """Removes and returns the topmost item in the heap, 
        otherwise raises an Exception if heap is empty.
        """
        if self.is_empty():
            raise Exception("Heap is empty")
        self._size -= 1
        top_item = self._heap[0]
        bottom_item = self._heap.pop(len(self._heap) - 1)
        if len(self._heap) == 0:
            return bottom_item
           
        self._heap[0] = bottom_item
        last_index = len(self._heap) - 1
        curr_pos = 0
        while True:
            left_child = 2*curr_pos + 1 
            right_child = 2*curr_pos + 2
            if left_child > last_index:
                break
            if right_child > last_index:
                max_child = left_child;
            else:
                left_item  = self._heap[left_child]
                right_item = self._heap[right_child]
                if left_item < right_item:
                    max_child = left_child
                else:
                    max_child = right_child
            max_item = self._heap[max_child]
            if bottom_item <= max_item:
                break
            else:
                self._heap[curr_pos] = self._heap[max_child]
                self._heap[max_child] = bottom_item
                curr_pos = max_child
        return top_item