from typing import List

__all__ = ["Node", "LinkedList"]


class Node:
    """A LinkedList Node"""
    next = None

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Node(value={self.value}, next={self.next})"


class LinkedList:
    """A simple Linked list data structure.

    Basic Usage::
    >>> ll = LinkedList()
    >>> ll.add(3)
    >>> ll.add(4)
    >>> ll.add(5)
    >>> ll.add(6)
    >>> print(ll)
    LinkedList(head=Node(value=6, next=Node(value=5, next=Node(value=4, next=Node(value=3, next=None)))))

    Construct from List
    >>> ll = LinkedList.from_list([1,2,3])
    >>> print(ll)
    LinkedList(head=Node(value=3, next=Node(value=2, next=Node(value=1, next=None))))

    Iter values
    >>> print([x for x in LinkedList.from_list([1,2,3])])
    [3, 2, 1]
    """
    head = None

    def __init__(self):
        pass

    def add(self, value):
        node = Node(value)
        if self.head:
            node.next = self.head
        self.head = node

    def __repr__(self):
        return f"LinkedList(head={self.head})"

    @classmethod
    def from_list(cls, l: List):
        ll = cls()
        for el in l:
            ll.add(el)
        return ll

    def __iter__(self):
        el = self.head
        while el is not None:
            yield el.value
            el = el.next


if __name__ == "__main__":
    ll = LinkedList()
    ll.add(3)
    ll.add(4)
    ll.add(5)
    ll.add(6)
    print(ll)
