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
        self.elements = []
    
    def is_empty(self):
        return not self.elements
    
    def enqueue(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def dequeue(self):
        return heapq.heappop(self.elements)[1]


# class heap:
# [1,2,3,4,5,6,7,8]