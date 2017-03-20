#! /usr/bin/env python3.6
# -*- coding: utf-8 -*-

from unittest import TestCase, main
from src.linked import DoublyLinkedList, Node
from src.exceptions import *


class TestDLL(TestCase):
    _length = 10

    def setUp(self) -> None:
        self.values = list(range(self._length))

    def test_empty_dll(self) -> None:
        dll = DoublyLinkedList()
        self.assertEqual(dll.size(), 0)
        self.assertEqual(dll.to_list(), [])

    def test_insertions(self) -> None:
        dll = DoublyLinkedList(1)

        def test_insert_before() -> None:
            self.assertEqual(dll.size(), 1)
            dll.insertBefore(Node(0), dll.head)
            self.assertEqual(dll.to_list(), [0, 1])

        def test_insert_after() -> None:
            dll.insertAfter(Node(2), dll.last)
            self.assertEqual(dll.to_list(), [0, 1, 2])

        test_insert_before()
        test_insert_after()

    def test_from_and_to_list(self) -> None:
        dll = DoublyLinkedList().fromlist(self.values)
        self.assertEqual(dll.size(), self._length)
        self.assertEqual(DoublyLinkedList.fromlist(self.values).to_list(), self.values)

    def test_node_exceptions(self) -> None:
        dll = DoublyLinkedList(Node(0))

        with self.assertRaises(NoPreviousNodeError):
            dll.head.prv()

        with self.assertRaises(NoNextNodeError):
            dll.head.nxt()

        self.assertFalse(dll.head.has_prev())
        self.assertFalse(dll.head.has_next())

    def test_clearing_dll(self) -> None:
        dll = DoublyLinkedList.fromlist(self.values)
        dll.clear()
        self.assertEqual(dll.size(), 0)
        self.assertIsNone(dll.head)
        self.assertIsNone(dll.last)

    def test_searching_dll(self) -> None:
        dll = DoublyLinkedList.fromlist(self.values)
        self.assertIs(type(dll.search(4)), Node)
        self.assertEqual(dll.search(5).value, 5)


if __name__ == '__main__':
    main()