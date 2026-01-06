import heapq
class Stack:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop() if not self.is_empty() else None
    def peek(self):
        return self.items[-1] if not self.is_empty() else None
    def is_empty(self):
        return len(self.items) == 0

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None
    def is_empty(self):
        return len(self.items) == 0

class Union_find:
    def __init__(self , elements):
        self.parent = {e:e for e in elements}
    def find(self,item):
        if self.parent[item]!=item:
            self.parent[item]= self.find(self.parent[item])
        return self.parent[item]
    def union(self, item1 , item2):
        root1 = self.find(item1)
        root2 = self.find(item2)
        if root1 != root2:
            self.parent[root1] = root2
            return True
        return False
class PriorityQueue:
    def __init__(self):
        self.heap = MinHeap()
    
    def is_empty(self):
        return self.heap.is_empty()
    
    def enqueue(self, item, priority):
        self.heap.push((priority, item))
    
    def dequeue(self):
        return self.heap.pop()[1]
class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, item):
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return root

    def is_empty(self):
        return len(self.heap) == 0

    def _sift_up(self, idx):
        parent_idx = (idx - 1) // 2
        if idx > 0 and self.heap[idx] < self.heap[parent_idx]:
            self.heap[idx], self.heap[parent_idx] = self.heap[parent_idx], self.heap[idx]
            self._sift_up(parent_idx)

    def _sift_down(self, idx):
        smallest = idx
        left_child = 2 * idx + 1
        right_child = 2 * idx + 2
        size = len(self.heap)
        if left_child < size and self.heap[left_child] < self.heap[smallest]:
            smallest = left_child
        if right_child < size and self.heap[right_child] < self.heap[smallest]:
            smallest = right_child
        if smallest != idx:
            self.heap[idx], self.heap[smallest] = self.heap[smallest], self.heap[idx]
            self._sift_down(smallest)