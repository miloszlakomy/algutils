from collections import OrderedDict

class OrderedSet(OrderedDict):
    def __init__(self, iterable=None):
        super().__init__()
        if iterable is not None:
            self.update(iterable)

    def add(self, item):
        """Add an item to the set. If the item is already present, do nothing."""
        self[item] = None  # Using the item as a key, value is irrelevant

    def remove(self, item):
        """Remove an item from the set. Raises KeyError if the item is not present."""
        del self[item]

    def discard(self, item):
        """Remove an item from the set if it is present. Does nothing if the item is not present."""
        super().pop(item, None)

    def update(self, iterable):
        """Add multiple items to the set from an iterable."""
        for item in iterable:
            self.add(item)

    def pop(self, index=-1):
        """Remove and return an item at the specified index. Raises IndexError if the index is out of range."""
        if not self:
            raise IndexError("pop from an empty OrderedSet")

        it = iter(self) if index >= 0 else reversed(self)
        for _ in range(index + 1 if index >= 0 else -index):
            key = next(it)

        del self[key]  # Remove the item from the OrderedSet
        return key  # Return the removed item

    def __and__(self, other) -> "OrderedSet":
        return OrderedSet(super().keys() & other)

    def __contains__(self, item):
        """Check if an item is in the set."""
        return super().__contains__(item)

    def __iter__(self):
        """Return an iterator over the set."""
        return super().__iter__()

    def __len__(self):
        """Return the number of unique items in the set."""
        return super().__len__()

    def __repr__(self):
        """Return a string representation of the OrderedSet."""
        return f"{OrderedSet.__name__}({list(self.keys())})"
