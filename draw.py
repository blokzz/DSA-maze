
import random
CELL_SIZE = 40
ROWS = 10
COLS = 10
OFFSET = 2

start = (ROWS // 2, COLS // 2)
end = (0, COLS - 1)
def random_edge_cell(rows, cols):
    edge = random.choice(["top", "bottom", "left", "right"])

    if edge == "top":
        return (0, random.randint(0, cols - 1))
    if edge == "bottom":
        return (rows - 1, random.randint(0, cols - 1))
    if edge == "left":
        return (random.randint(0, rows - 1), 0)
    if edge == "right":
        return (random.randint(0, rows - 1), cols - 1)


def pick_start_and_exits(rows, cols, num_exits=1):

    edges = []
    for c in range(cols):
        edges.append((0, c))
        edges.append((rows - 1, c))
    for r in range(1, rows - 1):
        edges.append((r, 0))
        edges.append((r, cols - 1))
        
    selected = random.sample(edges, 1 + num_exits)
    
    start = selected[0]
    exits = selected[1:]
    
    return start, exits

def open_walls_for_points(grid, points, rows, cols):
    for (r, c) in points:
        if r == 0: grid[r][c].walls["top"] = False
        elif r == rows - 1: grid[r][c].walls["bottom"] = False
        elif c == 0: grid[r][c].walls["left"] = False
        elif c == cols - 1: grid[r][c].walls["right"] = False
def draw_cell_walls(canvas, cell):
    x1, y1 = cell.col * CELL_SIZE + OFFSET, cell.row * CELL_SIZE + OFFSET
    x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
    if cell.walls["top"]: canvas.create_line(x1, y1, x2, y1, width=2)
    if cell.walls["right"]: canvas.create_line(x2, y1, x2, y2, width=2)
    if cell.walls["bottom"]: canvas.create_line(x1, y2, x2, y2, width=2)
    if cell.walls["left"]: canvas.create_line(x1, y1, x1, y2, width=2)

def draw_maze(canvas, grid):
    canvas.delete("all")
    for r in range(ROWS):
        for c in range(COLS):
            draw_cell_walls(canvas, grid[r][c])


def draw_point(canvas, r, c, color):
    x, y = c*CELL_SIZE+CELL_SIZE//2+OFFSET, r*CELL_SIZE+CELL_SIZE//2+OFFSET
    R = CELL_SIZE//4
    canvas.create_oval(x-R, y-R, x+R, y+R, fill=color, outline="")

def draw_path_cell(canvas, r, c, color):
    pad = 8
    x1, y1 = c*CELL_SIZE+pad+OFFSET, r*CELL_SIZE+pad+OFFSET
    x2, y2 = x1+CELL_SIZE-2*pad, y1+CELL_SIZE-2*pad
    canvas.create_rectangle(x1,y1,x2,y2, fill=color, outline="")

def draw_kanji(canvas, kanji_map):
    for (r, c), sym in kanji_map.items():
        x, y = c*CELL_SIZE+CELL_SIZE//2+OFFSET, r*CELL_SIZE+CELL_SIZE//2+OFFSET
        canvas.create_text(x, y, text=sym, font=("Arial", 14, "bold"), fill="blue")

def place_kanji(grid, start, end, rows, cols, symbols):
    free = [
        (r, c)
        for r in range(rows)
        for c in range(cols)
        if (r, c) not in (start, end)
    ]
    random.shuffle(free)

    return {
        free[i]: symbols[i]
        for i in range(len(symbols))
    }
