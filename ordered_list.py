class Node:
    '''Node for use with doubly-linked list'''
    def __init__(self, item):
        self.item = item
        self.next = None
        self.prev = None

class OrderedList:
    '''A doubly-linked ordered list of items, from lowest (head of list) to highest (tail of list)'''

    def __init__(self):
        '''Use ONE dummy node as described in class
           ***No other attributes***
           DO NOT have an attribute to keep track of size'''
        self.head = Node(None)

    def is_empty(self):
        '''Returns True if OrderedList is empty
            MUST have O(1) performance'''
        return self.head.next is None or self.head.next is self.head

    def add(self, item):
        '''Adds an item to OrderedList, in the proper location based on ordering of items
           from lowest (at head of list) to highest (at tail of list) and returns True.
           If the item is already in the list, do not add it again and return False.
           MUST have O(n) average-case performance'''
        if not self.search(item):
            current = self.head
            new = Node(item)
            if self.is_empty():
                self.head.next = new
                new.next = self.head
                new.prev = self.head
                self.head.prev = new
                return True
            else:
                while current.next is not self.head:
                    current = current.next
                    if current.item > item:
                        new.next = current
                        new.prev = current.prev
                        current.prev = new
                        new.prev.next = new
                        return True
                    elif item > current.item and current.next == self.head:
                        new.next = self.head
                        new.prev = current
                        current.next = new
                        self.head.prev = new
                        return True
        return False

    def remove(self, item):
        '''Removes the first occurrence of an item from OrderedList. If item is removed (was in the list)
          returns True.  If item was not removed (was not in the list) returns False
           MUST have O(n) average-case performance'''
        if not self.search(item):
            return False
        else:
            current = self.head
            while current.next is not None:
                current = current.next
                if current.item == item:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                    return True

    def index(self, item):
        '''Returns index of the first occurrence of an item in OrderedList (assuming head of list is index 0).
           If item is not in list, return None
           MUST have O(n) average-case performance'''
        current = self.head
        index = -1
        if self.is_empty():
            return None
        i = 0
        while i < self.size():
            current = current.next
            index += 1
            if current.item == item:
                return index
            i += 1
        return None
        # index = 0
        # if not self.search(item):
        #     return None
        # current = self.head
        # while current.next is not None:
        #     current = current.next
        #     if current.item == item:
        #         return index
        #     index += 1

    def pop(self, index):
        '''Removes and returns item at index (assuming head of list is index 0).
           If index is negative or >= size of list, raises IndexError
           MUST have O(n) average-case performance'''
        position = 0
        if index < 0 or index >= self.size():
            raise IndexError
        current = self.head.next
        while position != index:
            current = current.next
            position += 1
        popped = current.item
        current.next.prev = current.prev
        current.prev.next = current.next
        return popped

    def search(self, item):  # recursive
        '''Searches OrderedList for item, returns True if item is in list, False otherwise"
           To practice recursion, this method must call a RECURSIVE method that
           will search the list
           MUST have O(n) average-case performance'''
        current = self.head
        return self.help_search(item, current)

    def help_search(self, item, node):
        """Recursive function to help search list"""
        if node.item == item:
            return True
        if self.is_empty() or node.next is self.head:
            return False
        return self.help_search(item, node.next)

    def python_list(self):
        '''Return a Python list representation of OrderedList, from head to tail
           For example, list with integers 1, 2, and 3 would return [1, 2, 3]
           MUST have O(n) performance'''
        current = self.head
        values = []
        i = 0
        while i < self.size():
            current = current.next
            values.append(current.item)
            i += 1
        return values

    def python_list_reversed(self):  # recursive
        '''Return a Python list representation of OrderedList, from tail to head, using recursion
           For example, list with integers 1, 2, and 3 would return [3, 2, 1]
           To practice recursion, this method must call a RECURSIVE method that
           will return a reversed list
           MUST have O(n) performance'''
        values = []
        if self.is_empty():
            return values
        current = self.head.prev
        return self.reverse_help(values, current)

    def reverse_help(self, values, current):
        if current.prev == self.head:
            values.append(current.item)
            return values
        while current.prev != self.head:
            values.append(current.item)
            return self.reverse_help(values, current.prev)

    def size(self):  # recursive
        '''Returns number of items in the OrderedList
           To practice recursion, this method must call a RECURSIVE method that
           will count and return the number of items in the list
           MUST have O(n) performance'''
        if self.is_empty():
            return 0
        current = self.head
        return self.size_helper(current.next)

    def size_helper(self, current):
        """Recursive method for size"""
        if current is self.head:
            return 0
        return 1 + self.size_helper(current.next)
