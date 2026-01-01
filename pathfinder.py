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

def get_path_bfs(grid, start_pos, target_pos, rows, cols):
    q = Queue()
    q.enqueue(start_pos)
    visited = {start_pos}
    parent = {}
    found = False

    while not q.is_empty():
        curr = q.dequeue()
        if curr == target_pos:
            found = True
            break
        r, c = curr
        directions = [("top", -1, 0), ("right", 0, 1), ("bottom", 1, 0), ("left", 0, -1)]
        for wall, dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if not grid[r][c].walls[wall] and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = curr
                    q.enqueue((nr, nc))
    return reconstruct_path(parent, start_pos, target_pos) if found else []

def get_path_dfs(grid, start_pos, target_pos, rows, cols):
    stack = Stack()
    stack.push(start_pos)
    
    visited = {start_pos}
    parent = {}
    found = False

    while not stack.is_empty():
        curr = stack.pop()
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
                    
    return reconstruct_path(parent, start_pos, target_pos) if found else []