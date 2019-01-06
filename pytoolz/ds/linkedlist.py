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
      >>> ll.add(Node(3))
      >>> ll.add(Node(4))
      >>> ll.add(Node(5))
      >>> ll.add(Node(6))
      >>> print(ll)
      LinkedList(head=Node(value=6, next=Node(value=5, next=Node(value=4, next=Node(value=3, next=None)))))
    """
    head = None

    def __init__(self):
        pass

    def add(self, node: Node):
        if self.head:
            node.next = self.head
        self.head = node

    def __repr__(self):
        return f"LinkedList(head={self.head})"

    # TODO
    # @classmethod -> from_list
    # __iter__ -> iterate


if __name__ == "__main__":
    ll = LinkedList()
    ll.add(Node(3))
    ll.add(Node(4))
    ll.add(Node(5))
    ll.add(Node(6))
    print(ll)
