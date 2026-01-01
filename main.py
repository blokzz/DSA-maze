from tkinter import *
from maze_generators import *
from draw import *
from algorithms import *
from pathfinder import *
import random

def pick_4(kanji_arr):
    random_four = ()
    while len(random_four) !=4:
        r = random.choice(kanji_arr)
        random_four +=(r ,)
        kanji_arr.remove(r)
    return random_four
kanji_symbols = ["鬱","森","戯","暖","魚","遡","結","灰"]
kanji_to_collect = pick_4(kanji_symbols)

GLOBAL_MAZE = None
GLOBAL_START = None
GLOBAL_EXITS = []
GLOBAL_KANJI = {}
ANIMATION_RUNNING = False


def pick_kanji_randomly(grid, exclude_points, amount=4):
    all_cells = [(r, c) for r in range(ROWS) for c in range(COLS) if (r, c) not in exclude_points]
    random.shuffle(all_cells)
    
    symbols = ["鬱","森","戯","暖","魚","遡","結","灰"]
    chosen_pos = all_cells[:amount]
    
    return {pos: symbols[i] for i, pos in enumerate(chosen_pos)}
MULTI_EXIT_VAR = None 

def run_adventure(algo_type):
    global ANIMATION_RUNNING
    if ANIMATION_RUNNING: return
    
    draw_maze(canvas, GLOBAL_MAZE)
    draw_kanji(canvas, GLOBAL_KANJI)
    draw_point(canvas, GLOBAL_START[0], GLOBAL_START[1], "green")
    for (er, ec) in GLOBAL_EXITS:
        draw_point(canvas, er, ec, "red")
    
    targets = list(GLOBAL_KANJI.keys())
    current_pos = GLOBAL_START
    full_path = []
    
    finder = get_path_bfs if algo_type == "BFS" else get_path_dfs
    color = "yellow" if algo_type == "BFS" else "orange"
    
    while targets:
        closest = min(targets, key=lambda t: abs(t[0]-current_pos[0]) + abs(t[1]-current_pos[1]))
        segment = finder(GLOBAL_MAZE, current_pos, closest, ROWS, COLS)
        if full_path: full_path.extend(segment[1:])
        else: full_path.extend(segment)
        current_pos = closest
        targets.remove(closest)
        
    if GLOBAL_EXITS:
        best_exit = min(GLOBAL_EXITS, key=lambda e: abs(e[0]-current_pos[0]) + abs(e[1]-current_pos[1]))
        segment_exit = finder(GLOBAL_MAZE, current_pos, best_exit, ROWS, COLS)
        full_path.extend(segment_exit[1:])
    
    ANIMATION_RUNNING = True
    idx = 0
    def animate():
        nonlocal idx
        global ANIMATION_RUNNING
        if idx >= len(full_path):
            ANIMATION_RUNNING = False
            return
        
        r, c = full_path[idx]
        draw_path_cell(canvas, r, c, color)
        if (r, c) == GLOBAL_START: draw_point(canvas, r, c, "green")
        elif (r, c) in GLOBAL_EXITS: draw_point(canvas, r, c, "red")
        elif (r, c) in GLOBAL_KANJI: draw_point(canvas, r, c, "lime")
        
        idx += 1
        canvas.after(30, animate)
    animate()

def generate_new_level(algorithm):
    global GLOBAL_MAZE, GLOBAL_START, GLOBAL_EXITS, GLOBAL_KANJI
    
    if algorithm == "KRUSKAL":
        GLOBAL_MAZE = generate_maze_kruskal(ROWS, COLS)
    elif algorithm == "PRIM":
        GLOBAL_MAZE = generate_maze_prim(ROWS, COLS)
    else:
        GLOBAL_MAZE = generate_maze_dfs(ROWS, COLS)
    
    is_multi = MULTI_EXIT_VAR.get()
    num_exits = 3 if is_multi else 1
    

    GLOBAL_START, GLOBAL_EXITS = pick_start_and_exits(ROWS, COLS, num_exits)
    
    points_to_open = [GLOBAL_START] + GLOBAL_EXITS
    open_walls_for_points(GLOBAL_MAZE, points_to_open, ROWS, COLS)
    
    GLOBAL_KANJI = pick_kanji_randomly(GLOBAL_MAZE, points_to_open)
    
    # 4. Rysowanie
    draw_maze(canvas, GLOBAL_MAZE)
    draw_kanji(canvas, GLOBAL_KANJI)
    draw_point(canvas, GLOBAL_START[0], GLOBAL_START[1], "green")
    for (er, ec) in GLOBAL_EXITS:
        draw_point(canvas, er, ec, "red")

root = Tk()
root.title("Projekt asd 2")

canvas = Canvas(root, width=COLS*CELL_SIZE+OFFSET*2, height=ROWS*CELL_SIZE+OFFSET*2, bg="white")
canvas.pack()

ctrl = Frame(root, bg="#eee", pady=5)
ctrl.pack(fill="x")

Label(ctrl, text="GENERUJ:", bg="#eee", font=("Arial", 8, "bold")).pack(side="left")

MULTI_EXIT_VAR = BooleanVar()
chk_multi = Checkbutton(ctrl, text="Wiele Wyjść", variable=MULTI_EXIT_VAR, bg="#eee")
chk_multi.pack(side="left", padx=5)

Button(ctrl, text="DFS", bg="lightblue", command=lambda: generate_new_level("DFS")).pack(side="left", padx=2)
Button(ctrl, text="Kruskal", bg="#add8e6", command=lambda: generate_new_level("KRUSKAL")).pack(side="left", padx=2)
Button(ctrl, text="Prim", bg="#87cefa", command=lambda: generate_new_level("PRIM")).pack(side="left", padx=2)

Frame(ctrl, width=2, bg="gray").pack(side="left", padx=10, fill="y")


Label(ctrl, text="SZUKAJ:", bg="#eee", font=("Arial", 8, "bold")).pack(side="left")
Button(ctrl, text="BFS", bg="lightyellow", command=lambda: run_adventure("BFS")).pack(side="left", padx=2)
Button(ctrl, text="DFS", bg="peachpuff", command=lambda: run_adventure("DFS")).pack(side="left", padx=2)

generate_new_level("DFS")
root.mainloop()