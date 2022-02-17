"""
File: abstractcollection.py

This module defines an AbstractCollection class containing common data 
and method implementations for collections. Assumes that each collection 
type supports an iterator and an add method.
"""

class AbstractCollection():
    """Represents an abstract collection for all collection types."""

    def __init__(self, source_collection):
        """Will copy items to self from source_collection, 
        if it is present.
        """
        self._size = 0
        if source_collection:
            for item in source_collection:
                self.add(item)
    
    def __len__(self) -> int:
        """Returns the number of items in self."""
        return self._size

    def is_empty(self) -> bool:
        """Returns True if self is empty, or False otherwise."""
        return len(self) == 0

    def __str__(self) -> str:
        """Returns the string representation of the collection, 
        using the format [<item-1>, <item-2>, . . ., <item-n>].
        """
        return f"[{', '.join(map(str, self))}]"

    def __add__(self, other):
        """Returns a new collection consisting of the items in self and 
        other.
        """
        result = type(self)(self)
        for item in other:
            result.add(item)
        return result

    def __eq__(self, other):
        """Returns True if self equals other, or False otherwise."""
        if self is other: return True
        if type(self) != type(other): return False
        if len(self) != len(other): return False
        other_items = iter(other)
        for item in self:
            if item != next(other_items):
                return False
        return True