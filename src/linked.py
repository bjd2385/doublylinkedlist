## A quick and dirty linked list implementation

from typing import Any, List, Optional
from collections.abc import Iterable
from .exceptions import NoNextNodeError, NoPreviousNodeError


class Node:
    """ A node in our linked list """
    def __init__(self, value: Any, next: Any =None, previous: Any =None) -> None:
        if value is None:
            raise ValueError(
                f'{self.__class__.__name__} expects a value that is not {type(None)}'
            )

        self.value = value

        if next:
            self.next = Node(next) if type(next) is not Node else next
        else:
            self.next = next

        if previous:
            self.previous = Node(previous) if type(previous) is not Node \
                                else previous
        else:
            self.previous = previous

    def nxt(self) -> 'Node':
        if self.next:
            return self.next
        else:
            raise NoNextNodeError('Not linked to another node')

    def prv(self) -> 'Node':
        if self.previous:
            return self.previous
        else:
            raise NoPreviousNodeError('Not linked to previous node')

    def linkn(self, other: 'Node') -> None:
        self.next = other

    def linkp(self, other: 'Node') -> None:
        self.previous = other

    def __rshift__(self, other: 'Node') -> 'Node':
        """ Syntactic sugar for calling self.linkn, but chaining links too; allows
        the syntax N1 >> N2 >> N3 >> N4 ... for constructing linked lists
        """
        self.linkn(other)
        return self

    def __lshift__(self, other: 'Node') -> 'Node':
        """ Syntactic sugar for calling self.linkp, and allows the converse,
        N1 << N2 << N3 << N4 ..., for linking the opposite direction
        """
        self.linkp(other)
        return self

    def remove_prev_link(self) -> None:
        if self.previous:
            self.previous = None

    def remove_post_link(self) -> None:
        if self.next:
            self.next = None

    def has_prev(self) -> bool:
        return self.previous is not None

    def has_next(self) -> bool:
        return self.next is not None


class DoublyLinkedList(Iterable):
    """ Doubly linked list implementation """
    _size = 0

    def __init__(self, head_val: Any =None) -> None:
        if head_val is not None:
            self.head = Node(head_val) if type(head_val) is not Node else head_val
            self._size += 1
        else:
            self.head = None

        self.last = self.head

    def __iter__(self) -> 'DoublyLinkedList':
        return self

    def __next__(self) -> Node:
        try:
            if not hasattr(self, '_start'):
                self._start = self.head
            else:
                self._start = self._start.nxt()

        except NoNextNodeError:
            del self._start
            raise StopIteration

        else:
            return self._start

    @classmethod
    def fromlist(cls, some_list: List[Any]) -> 'DoublyLinkedList':
        """ Convert a list to a doubly linked list object """
        dll = cls()

        for item in some_list:
            dll += Node(item)

        return dll

    def to_list(self) -> List[Any]:
        return [item.value for item in self] if self.size() else []

    def addLast(self, other: Any) -> None:
        if self.head is None:
            # There's nothing at the start of the linked list
            self.head = Node(other) if type(other) is not Node else other
            self.last = self.head
        else:
            # Link the last element to `other` to make `other` the last element
            self.last.linkn(other)
            self.last = self.last.nxt()
            # Now it looks like this:
            # N1 -> N2 -> ... -> Nn -> other
        self._size += 1

    def __iadd__(self, other: Node) -> 'DoublyLinkedList':
        """ Syntactic sugar for adding a node to the linked list; must be of Node
        type, however---similar to lists and __iadd__
        """
        if type(other) is not Node:
            raise TypeError(
              f'{self.__class__.__name__} expected type Node, received {type(other)}'
            )

        self.addLast(other)
        return self

    def size(self) -> int:
        return self._size

    def insertBefore(self, other: Any, node: Node) -> None:
        """ Insert a value or node before another node---does not guarantee a doubly
        linked list.
        """
        if node.has_prev():
            node.previous >> (other if type(other) is Node else Node(other)) << node
        else:
            # `node` has no prior (it must be the head of the ll)
            node << (Node(other) if type(other) is not Node else other)
            node.prv() >> node
            self.head = node.prv()

        self._size += 1

    def insertAfter(self, other: Any, node: Node) -> None:
        """ Insert a value or node after another node """
        if node.has_next():
            node >> (other if type(other) is Node else Node(other)) << node.next
        else:
            # `node` has no next (it must be the end of the ll)
            node >> (other if type(other) is Node else Node(other))
            node.nxt() << node
        self._size += 1

    def clear(self) -> None:
        """ Clear entire linked list """
        for node in self:
            del node
        self.head = None
        self.last = self.head
        self._size = 0

    def search(self, value: Any) -> Optional[Node]:
        """ Search for a node containing some value """
        for node in self:
            if node.value == value:
                return node