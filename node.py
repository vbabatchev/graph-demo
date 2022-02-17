"""
File: node.py

This module defines a Node class.
"""

class Node():
    """Represents a singly linked node."""

    def __init__(self, data, next: 'Node' = None):
        self.data = data
        self.next = next