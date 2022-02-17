"""
File: abstractstack.py

This module defines an AbstractStack class containing common data and
method implementations for stacks.
"""

from abstractcollection import AbstractCollection


class AbstractStack(AbstractCollection):
    """An abstract stack implementation."""

    def __init__(self, source_collection=None):
        """Sets the initial state of self, which includes the contents 
        of source_collection, if it's present.
        """
        AbstractCollection.__init__(self, source_collection)
    
    def add(self, item):
        """Adds item to self."""
        self.push(item)