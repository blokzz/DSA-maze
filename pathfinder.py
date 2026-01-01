from algorithms import *
import random

def reconstruct_path(parent, start, end):
    path = []
    curr = end
    while curr != start:
        path.append(curr)
        curr = parent.get(curr)
        if curr is None: break 
    path.append(start)
    path.reverse()
    return path

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)
    
def get_path_bfs(grid, start_pos, target_pos, rows, cols):
    q = Queue()
    q.enqueue(start_pos)
    visited = {start_pos}
    parent = {}
    found = False
    
    nodes_count = 0

    while not q.is_empty():
        curr = q.dequeue()
        nodes_count += 1
        
        if curr == target_pos: found = True; break
        r, c = curr
        for wall, dr, dc in [("top",-1,0),("right",0,1),("bottom",1,0),("left",0,-1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if not grid[r][c].walls[wall] and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = curr
                    q.enqueue((nr, nc))
    
    path = reconstruct_path(parent, start_pos, target_pos) if found else []
    return path, nodes_count

def get_path_dfs(grid, start_pos, target_pos, rows, cols):
    stack = Stack()
    stack.push(start_pos)
    visited = {start_pos}
    parent = {}
    found = False
    
    nodes_count = 0

    while not stack.is_empty():
        curr = stack.pop()
        nodes_count += 1
        
        if curr == target_pos: found = True; break
        r, c = curr
        dirs = [("top",-1,0),("right",0,1),("bottom",1,0),("left",0,-1)]
        random.shuffle(dirs)
        for wall, dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if not grid[r][c].walls[wall] and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = curr
                    stack.push((nr, nc))
                    
    path = reconstruct_path(parent, start_pos, target_pos) if found else []
    return path, nodes_count

def get_path_astar(grid, start_pos, target_pos, rows, cols):
    pq = PriorityQueue()
    pq.enqueue(start_pos, 0)
    
    parent = {start_pos: None}
    cost_so_far = {start_pos: 0}
    found = False
    
    nodes_count = 0
    
    while not pq.is_empty():
        current = pq.dequeue()
        nodes_count += 1
        
        if current == target_pos:
            found = True
            break
        
        r, c = current
        dirs = [("top",-1,0),("right",0,1),("bottom",1,0),("left",0,-1)]
        
        for wall, dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if not grid[r][c].walls[wall]:
                    new_cost = cost_so_far[current] + 1
                    if (nr, nc) not in cost_so_far or new_cost < cost_so_far[(nr, nc)]:
                        cost_so_far[(nr, nc)] = new_cost
                        priority = new_cost + heuristic((nr, nc), target_pos)
                        pq.enqueue((nr, nc), priority)
                        parent[(nr, nc)] = current
                        
    path = reconstruct_path(parent, start_pos, target_pos) if found else []
    return path, nodes_count