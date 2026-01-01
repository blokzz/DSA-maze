import random
from algorithms import Stack, Union_find
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.walls = {
            "top": True,
            "right": True,
            "bottom": True,
            "left": True
        }

def generate_maze_dfs(rows, cols):
    grid = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
    

    stack = Stack()
    
    current = grid[0][0]
    current.visited = True
    stack.push(current)
    
    while not stack.is_empty():
        current = stack.peek()
        neighbors = []
        directions = [("top", -1, 0, "bottom"), ("right", 0, 1, "left"), 
                      ("bottom", 1, 0, "top"), ("left", 0, -1, "right")]
        
        for wall, dr, dc, opp_wall in directions:
            nr, nc = current.row + dr, current.col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor = grid[nr][nc]
                if not neighbor.visited:
                    neighbors.append((wall, neighbor, opp_wall))
        
        if neighbors:
            wall, next_cell, opp_wall = random.choice(neighbors)
            current.walls[wall] = False
            next_cell.walls[opp_wall] = False
            next_cell.visited = True
            stack.push(next_cell)
        else:
            stack.pop()
            
    return grid

def generate_maze_kruskal(rows, cols):
    grid = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
    edges = []
    for r in range(rows):
        for c in range(cols):
            if r < rows - 1: edges.append(((r, c), (r + 1, c), "bottom"))
            if c < cols - 1: edges.append(((r, c), (r, c + 1), "right"))
    
    random.shuffle(edges)
    dsu = Union_find([(r, c) for r in range(rows) for c in range(cols)])
    
    for (r1, c1), (r2, c2), wall_type in edges:
        if dsu.union((r1, c1), (r2, c2)):
            cell1 = grid[r1][c1]
            cell2 = grid[r2][c2]
            if wall_type == "bottom":
                cell1.walls["bottom"] = False
                cell2.walls["top"] = False
            elif wall_type == "right":
                cell1.walls["right"] = False
                cell2.walls["left"] = False
    return grid

def generate_maze_prim(rows, cols):
    grid = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
    start_cell = grid[0][0]
    start_cell.visited = True
    frontier = []
    
    def add_neighbors(cell):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = cell.row + dr, cell.col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor = grid[nr][nc]
                if not neighbor.visited and (nr, nc) not in frontier:
                    frontier.append((nr, nc))

    add_neighbors(start_cell)
    
    while frontier:
        cr, cc = random.choice(frontier)
        frontier.remove((cr, cc))
        current_cell = grid[cr][cc]
        current_cell.visited = True
        
        potential = []
        dirs = [("top", -1, 0, "bottom"), ("bottom", 1, 0, "top"), 
                ("left", 0, -1, "right"), ("right", 0, 1, "left")]
        
        for wall, dr, dc, opp_wall in dirs:
            nr, nc = cr + dr, cc + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc].visited:
                    potential.append((wall, grid[nr][nc], opp_wall))
        
        if potential:
            wall, neighbor, opp_wall = random.choice(potential)
            current_cell.walls[wall] = False
            neighbor.walls[opp_wall] = False
            
        add_neighbors(current_cell)
        
    return grid