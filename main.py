from tkinter import *
from maze_generators import *
from draw import *
import itertools
from algorithms import *
from pathfinder import *
import random

GLOBAL_MAZE = None
GLOBAL_START = None
GLOBAL_EXITS = []
GLOBAL_KANJI = {}
ANIMATION_RUNNING = False
STATS_LABEL = None
NODES_VISITED = 0
MULTI_EXIT_VAR = None 

def pick_kanji_randomly(grid, exclude_points, rows, cols, amount=4):
    all_cells = [(r, c) for r in range(rows) for c in range(cols) if (r, c) not in exclude_points]
    random.shuffle(all_cells)
    symbols = ["鬱","森","戯","暖","魚","遡","結","灰","手","示","紙"]
    random.shuffle(symbols)
    random_four = symbols[:amount]
    if len(all_cells) < amount: amount = len(all_cells)
    chosen = all_cells[:amount]

    return {pos: random_four[i] for i, pos in enumerate(chosen)}

def run_adventure(algo_type):
    global ANIMATION_RUNNING, NODES_VISITED
    if ANIMATION_RUNNING: return
    
    draw_maze(canvas, GLOBAL_MAZE)
    draw_kanji(canvas, GLOBAL_KANJI)
    draw_point(canvas, GLOBAL_START[0], GLOBAL_START[1], "green")
    for (er, ec) in GLOBAL_EXITS:
        draw_point(canvas, er, ec, "red")
    
    if algo_type == "BFS":
        finder = get_path_bfs
        dist_estimator = get_path_bfs
        color = "yellow"
        algo_name = "BFS (Szerokość)"
    elif algo_type == "A*":
        finder = get_path_astar
        dist_estimator = get_path_astar
        color = "#add8e6"
        algo_name = "A* (A-Star)"
    else:
        finder = get_path_dfs
        dist_estimator = get_path_bfs
        color = "orange"
        algo_name = "DFS (Głębokość)"
        
    targets = list(GLOBAL_KANJI.keys())
    
    best_total_order = []
    min_total_length = float('inf')
    
    possible_orders = list(itertools.permutations(targets))
    
    exits = GLOBAL_EXITS if GLOBAL_EXITS else []
    
    for order in possible_orders:
        current_sim_pos = GLOBAL_START
        current_path_len = 0
        valid_order = True
        
        for target in order:
            path, _ = dist_estimator(GLOBAL_MAZE, current_sim_pos, target, ROWS, COLS)
            if not path:
                valid_order = False
                break
            current_path_len += len(path)
            current_sim_pos = target
            
        if not valid_order: continue
            
        if exits:
            best_exit_len = float('inf')
            for ex in exits:
                path, _ = dist_estimator(GLOBAL_MAZE, current_sim_pos, ex, ROWS, COLS)
                if path and len(path) < best_exit_len:
                    best_exit_len = len(path)
            
            if best_exit_len != float('inf'):
                current_path_len += best_exit_len
            else:
                continue

        if current_path_len < min_total_length:
            min_total_length = current_path_len
            best_total_order = list(order)


    print(f"Najlepsza trasa ma długość: {min_total_length}")

    full_path = []
    total_nodes_visited = 0
    current_pos = GLOBAL_START
    
    for target in best_total_order:
        segment, cost = finder(GLOBAL_MAZE, current_pos, target, ROWS, COLS)
        
        total_nodes_visited += cost
        if full_path: full_path.extend(segment[1:])
        else: full_path.extend(segment)
        current_pos = target
        
    if exits:
        best_exit = None
        min_len = float('inf')
        best_segment = []
        best_cost = 0
        
        for ex in exits:
            path, cost = dist_estimator(GLOBAL_MAZE, current_pos, ex, ROWS, COLS)
            if path and len(path) < min_len:
                min_len = len(path)
                best_exit = ex
                real_path, real_cost = finder(GLOBAL_MAZE, current_pos, ex, ROWS, COLS)
                best_segment = real_path
                best_cost = real_cost
        
        if best_segment:
            full_path.extend(best_segment[1:])
            total_nodes_visited += best_cost

    stats_text = f"Algorytm: {algo_name}\nDługość trasy: {len(full_path)}\nOdwiedzone pola: {total_nodes_visited}"
    STATS_LABEL.config(text=stats_text, fg="blue" if algo_type != "DFS" else "red")

    ANIMATION_RUNNING = True
    idx = 0
    head_obj = None
    def animate():
        nonlocal idx, head_obj
        global ANIMATION_RUNNING
        if idx >= len(full_path):
            ANIMATION_RUNNING = False
            if best_exit:
                draw_point(canvas, best_exit[0], best_exit[1], "purple") 
            return
        if head_obj: canvas.delete(head_obj)
        r, c = full_path[idx]
        draw_path_cell(canvas, r, c, color)
        x, y = c*CELL_SIZE+CELL_SIZE//2+OFFSET, r*CELL_SIZE+CELL_SIZE//2+OFFSET
        R = CELL_SIZE//6
        head_obj = canvas.create_oval(x-R, y-R, x+R, y+R, fill="blue")
        if (r, c) == GLOBAL_START: 
            draw_point(canvas, r, c, "green")
            
        elif (r, c) in GLOBAL_EXITS: 
            draw_point(canvas, r, c, "red")
            
        elif (r, c) in GLOBAL_KANJI: 
            draw_point(canvas, r, c, "lime")
        
        idx += 1
        canvas.after(30, animate)
    animate()

def generate_new_level(algorithm):
    global GLOBAL_MAZE, GLOBAL_START, GLOBAL_EXITS, GLOBAL_KANJI
    global ROWS, COLS
    try:
        val = int(spin_size.get())
    except:
        val = 15
    ROWS = val
    COLS = val
    
    new_w = COLS * CELL_SIZE + OFFSET * 2
    new_h = ROWS * CELL_SIZE + OFFSET * 2
    canvas.config(width=new_w, height=new_h)
    
    if algorithm == "KRUSKAL": GLOBAL_MAZE = generate_maze_kruskal(ROWS, COLS)
    elif algorithm == "PRIM": GLOBAL_MAZE = generate_maze_prim(ROWS, COLS)
    else: GLOBAL_MAZE = generate_maze_dfs(ROWS, COLS)
    
    is_multi = MULTI_EXIT_VAR.get()
    num_exits = 3 if is_multi else 1
    GLOBAL_START, GLOBAL_EXITS = pick_start_and_exits(ROWS, COLS, num_exits)
    
    points_to_open = [GLOBAL_START] + GLOBAL_EXITS
    open_walls_for_points(GLOBAL_MAZE, points_to_open, ROWS, COLS)
    GLOBAL_KANJI = pick_kanji_randomly(GLOBAL_MAZE, points_to_open, ROWS, COLS)
    
    draw_maze(canvas, GLOBAL_MAZE)
    draw_kanji(canvas, GLOBAL_KANJI)
    draw_point(canvas, GLOBAL_START[0], GLOBAL_START[1], "green")
    for (er, ec) in GLOBAL_EXITS: draw_point(canvas, er, ec, "red")
    
    STATS_LABEL.config(text=f"Labirynt {ROWS}x{COLS}. Wybierz algorytm.", fg="black")


root = Tk()
root.title("Projekt asd 2")

stats_frame = Frame(root, bg="white", pady=5)
stats_frame.pack(fill="x")
STATS_LABEL = Label(stats_frame, text="", font=("Consolas", 10), bg="white")
STATS_LABEL.pack()

canvas = Canvas(root, width=COLS*CELL_SIZE+OFFSET*2, height=ROWS*CELL_SIZE+OFFSET*2, bg="white")
canvas.pack()

ctrl = Frame(root, bg="#eee", pady=5)
ctrl.pack(fill="x")

Label(ctrl, text="SIZE:", bg="#eee", font=("Arial", 8)).pack(side="left")
SIZE_VAR = IntVar(value=10)
spin_size = Spinbox(ctrl, from_=5, to=20, width=3, textvariable=SIZE_VAR)
spin_size.pack(side="left", padx=5)

Frame(ctrl, width=5, bg="#eee").pack(side="left")

Label(ctrl, text="GEN:", bg="#eee", font=("Arial", 8, "bold")).pack(side="left")
MULTI_EXIT_VAR = BooleanVar()
Checkbutton(ctrl, text="Multi-Exit", variable=MULTI_EXIT_VAR, bg="#eee").pack(side="left")

Button(ctrl, text="DFS", bg="lightblue", command=lambda: generate_new_level("DFS")).pack(side="left")
Button(ctrl, text="Kruskal", bg="#add8e6", command=lambda: generate_new_level("KRUSKAL")).pack(side="left")
Button(ctrl, text="Prim", bg="#87cefa", command=lambda: generate_new_level("PRIM")).pack(side="left")

Frame(ctrl, width=10, bg="#eee").pack(side="left")

Label(ctrl, text="RUN:", bg="#eee", font=("Arial", 8, "bold")).pack(side="left")
Button(ctrl, text="DFS", bg="peachpuff", command=lambda: run_adventure("DFS")).pack(side="left")
Button(ctrl, text="BFS", bg="lightyellow", command=lambda: run_adventure("BFS")).pack(side="left")
Button(ctrl, text="A*", bg="#90ee90", font=("Arial", 9, "bold"), command=lambda: run_adventure("A*")).pack(side="left", padx=5)

generate_new_level("DFS")
root.mainloop()