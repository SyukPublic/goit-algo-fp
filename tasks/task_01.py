# -*- coding: utf-8 -*-

"""
HomeWork Task 2
"""

import copy
import random
from typing import Any, Optional, Iterator

class Node:
    def __init__(self, data: Any = None) -> None:
        self.data: Any = data
        self.next: Optional[Node] = None

    def __repr__(self) -> str:
        return f"Node({self.data!r})"


class LinkedList:
    def __init__(self, head: Optional[Node] = None) -> None:
        self.head: Optional[Node] = head

    def __iter__(self) -> Iterator[Node]:
        current_node = self.head
        while current_node is not None:
            yield current_node
            current_node = current_node.next

    def __str__(self) -> str:
        return " -> ".join(repr(x) for x in self)

    def _search(self, data: Any) -> tuple[Optional[Node], Optional[Node]]:
        """
        Returns the first and the previous node with the specified value
        """
        current_node = self.head
        prev_node: Optional[Node] = None
        while current_node is not None:
            if current_node.data == data:
                return current_node, prev_node
            prev_node, current_node = current_node, current_node.next
        return None, prev_node

    def append(self, data: Any) -> None:
        """
        Add an element to the end of the list
        """
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        current_node = self.head
        while current_node.next is not None:
            current_node = current_node.next
        current_node.next = new_node

    def prepend(self, data: Any) -> None:
        """
        Add an element to the beginning of the list
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, data: Any) -> bool:
        """
        Delete the first node with the value data.
        Returns True if deleted, and False if the node was not found.
        """
        current_node, prev_node = self._search(data)
        if current_node is not None:
            if prev_node:
                prev_node.next = current_node.next
            else:
                self.head = current_node.next
            return True
        return False

    def insert_before(self, next_node: Node, data: Any) -> None:
        """
        Insert a new node before the specified one
        """
        if next_node is None:
            return
        if self.head == next_node:
            self.prepend(data)
            return
        new_node = Node(data)
        new_node.next = next_node
        current_node = self.head
        while current_node is not None and current_node.next != next_node:
            current_node = current_node.next
        if current_node is not None:
            current_node.next = new_node

    def insert_after(self, prev_node: Node, data: Any) -> None:
        """
        Insert a new node after the specified one
        """
        if prev_node is None:
            return
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def find(self, data: Any) -> Optional[Node]:
        """
        Returns the first node with the specified value
        """
        current_node, _ = self._search(data)
        return current_node

    def reverse_iterative(self) -> None:
        """
        Reverse a singly linked list in-place (modifies the next references)
        """
        prev_node = None
        current_node = self.head
        while current_node is not None:
            # save the reference to the next one
            next_node = current_node.next
            # change the direction
            current_node.next = prev_node
            # shift the prev_node forward
            prev_node = current_node
            # move on
            current_node = next_node
        # new head of the list
        self.head = prev_node

    def reverse_recursive(self) -> None:
        """
        Reverse a singly linked list in-place recursively (modifies the next references)
        """

        def _reverse_(node: Optional[Node], prev_node: Optional[Node] = None) -> Optional[Node]:
            if node is None:
                return prev_node
            next_node = node.next
            node.next = prev_node
            return _reverse_(next_node, node)

        self.head = _reverse_(self.head)

    # =================================================== Merge Sort ===================================================

    def sort_iterative(self) -> None:
        """
        Sort a list with merge sort (bottom-up, non-recursive).
        Works on very large lists and doesn’t overflow the recursion stack.
        """
        if self.head is None or self.head.next is None:
            return

        def _split_(head: Node, size: int) -> Optional[Node]:
            """
            Detach a sublist of length size and return its head.
            """
            current_node = head
            for _ in range(size - 1):
                if current_node is None or current_node.next is None:
                    break
                current_node = current_node.next
            if current_node is None:
                return None
            next_node = current_node.next
            current_node.next = None
            return next_node

        def _merge_(ll1: Optional[Node], ll2: Optional[Node]) -> tuple[Node, Node]:
            """
            Merge two sorted sublists. Return (head, tail).
            """
            dummy_head = Node(0)
            tail_node = dummy_head
            while ll1 is not None and ll2 is not None:
                if ll1.data <= ll2.data:
                    tail_node.next, ll1 = ll1, ll1.next
                else:
                    tail_node.next, ll2 = ll2, ll2.next
                tail_node = tail_node.next
            tail_node.next = ll1 if ll1 is not None else ll2
            while tail_node.next is not None:
                tail_node = tail_node.next
            return dummy_head.next, tail_node

        # Length calculation
        _length = 0
        _current_node = self.head
        while _current_node is not None:
            _length += 1
            _current_node = _current_node.next

        _dummy_head = Node(0)
        _dummy_head.next = self.head
        _size = 1

        while _size < _length:
            _prev_node, _current_node = _dummy_head, _dummy_head.next
            while _current_node is not None:
                _left_node = _current_node
                _right_node = _split_(_left_node, _size)
                _current_node = _split_(_right_node, _size)
                _merged_head, _merged_tail = _merge_(_left_node, _right_node)
                _prev_node.next = _merged_head
                _prev_node = _merged_tail
            _size *= 2

        self.head = _dummy_head.next

    def sort_recursive(self) -> None:
        """
        Recursive merge sort of a list.
        Causes a RecursionError on very large lists.
        """
        def _get_middle_(head: Node) -> Node:
            """
            Find the middle of the list (fast (2 nodes shift)/slow (1 node shift) pointers)
            """
            slow, fast = head, head
            while fast.next is not None and fast.next.next is not None:
                slow = slow.next
                fast = fast.next.next
            return slow

        def _sorted_merge_(left_node: Optional[Node], right_node: Optional[Node]) -> Optional[Node]:
            """
            Merge two sorted lists
            """
            if left_node is None:
                return right_node
            if right_node is None:
                return left_node

            if left_node.data <= right_node.data:
                result = left_node
                result.next = _sorted_merge_(left_node.next, right_node)
            else:
                result = right_node
                result.next = _sorted_merge_(left_node, right_node.next)
            return result

        def _merge_sort_(head: Optional[Node]) -> Optional[Node]:
            """
            Recursive merge sort
            """
            if head is None or head.next is None:
                return head

            middle_node = _get_middle_(head)
            next_to_middle = middle_node.next
            middle_node.next = None  # розділяємо список

            left = _merge_sort_(head)
            right = _merge_sort_(next_to_middle)

            return _sorted_merge_(left, right)

        self.head = _merge_sort_(self.head)

    # =================================================== Merge Sort ===================================================


def merge_sorted_lists(ll1: LinkedList, ll2: LinkedList) -> LinkedList:
    """
    Merge two sorted singly linked lists into one sorted list.

    :param ll1: First linked list (LinkedList, mandatory)
    :param ll2: Second linked list (LinkedList, mandatory)
    :return: Merged linked list (LinkedList)
    """

    # Dummy "head" to simplify the logic
    dummy_head = Node(0)
    tail = dummy_head

    ll1_node = ll1.head
    ll2_node = ll2.head

    while ll1_node is not None and ll2_node is not None:
        if ll1_node.data <= ll2_node.data:
            tail.next, ll1_node = ll1_node, ll1_node.next
        else:
            tail.next, ll2_node = ll2_node, ll2_node.next
        tail = tail.next

    # Add the remaining elements
    tail.next = ll1_node if ll1_node is not None else ll2_node

    return LinkedList(head=dummy_head.next)


def test_linked_list_operations() -> None:

    ll = LinkedList()
    for number in [random.randint(1, 100) for _ in range(10)]:
        ll.append(number)

    print("Зв'язний список:")
    print(ll)

    print()
    print("Ітераційна реалізація реверсу (O(n) часу та O(1) пам’яті)")
    ll_copy = copy.deepcopy(ll)
    print("Зв'язний список до реверсу:")
    print(ll)
    ll_copy.reverse_iterative()
    print("Зв'язний список після реверсу:")
    print(ll_copy)

    print()
    print("Рекурсивна реалізація реверсу (O(n) часу та O(n) пам’яті)")
    ll_copy = copy.deepcopy(ll)
    print("Зв'язний список до реверсу:")
    print(ll)
    ll_copy.reverse_recursive()
    print("Зв'язний список після реверсу:")
    print(ll_copy)

    print()
    print("Ітераційна реалізація merge sort O(n log n) часу та O(1) пам’яті)")
    ll_copy = copy.deepcopy(ll)
    print("Зв'язний список до сортування:")
    print(ll)
    ll_copy.sort_iterative()
    print("Зв'язний список після сортування:")
    print(ll_copy)

    print()
    print("Рекурсивна реалізація merge sort (O(n log n) часу та O(log n) пам’яті)")
    ll_copy = copy.deepcopy(ll)
    print("Зв'язний список до сортування:")
    print(ll)
    ll_copy.sort_recursive()
    print("Зв'язний список після сортування:")
    print(ll_copy)

    ll1 = LinkedList()
    for number in [random.randint(1, 100) for _ in range(10)]:
        ll1.append(number)
    ll1.sort_iterative()

    ll2 = LinkedList()
    for number in [random.randint(1, 100) for _ in range(10)]:
        ll2.append(number)
    ll2.sort_iterative()

    print()
    print("Перший зв'язний відсортований список:")
    print(ll1)
    print("Другий зв'язний відсортований список:")
    print(ll2)
    ll_merged = merge_sorted_lists(ll1, ll2)
    print("Об'єднаний зв'язний список:")
    print(ll_merged)
