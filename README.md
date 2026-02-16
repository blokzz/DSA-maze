# Maze Intelligence: Generation, Pathfinding & Analysis 

<p align="center">
  <img src="assets/demo.gif" alt="maze animation" width="400">
</p>

This project was developed as a **Mini-Project for the Data Structures and Algorithms (DSA) course** at University. It provides a comprehensive suite for visualizing, analyzing, and comparing graph-based algorithms in a 2D grid environment.

The application allows users to procedurally generate mazes and solve them using various pathfinding techniques, with a specific focus on state-dependent logic (collecting items before exiting).

---

##  Academic Context

* **Course:** Data Structures and Algorithms (DSA)
* **Objective:** Practical implementation of graph traversal, Minimum Spanning Trees (MST), and heuristic search.
* **Key Focus:** Comparative analysis of algorithm efficiency .

##  Key Features

### 1. Maze Generation (MST & Backtracking)
The tool generates "perfect" mazes (every cell is reachable with no loops) using:
* **Randomized DFS (Recursive Backtracker):** Creates long, winding corridors.
* **Kruskal’s Algorithm:** Uses a **Disjoint Set Union (DSU)** structure to merge walls, creating a dense, complex branching factor.
* **Prim’s Algorithm:** A neighbor-based growth approach that results in a unique radial topological structure.

### 2. Intelligent Pathfinding & State Logic
The solver isn't just looking for an exit; it must handle a **multi-objective scenario**:
* **Objective Collection:** The algorithm is strictly required to pick up **4 specific targets** (items) before the exit(s) become accessible.
* **Multi-Exit Support:** Once targets are acquired, the system identifies the most efficient path to the nearest available exit.
* **Real-time Visualization:** Built with **Tkinter**, showing the path in real time.

### 3. Algorithm Comparison
| Algorithm | Category | Heuristic | Search Strategy |
| :--- | :--- | :--- | :--- |
| **DFS** | Uninformed | None | LIFO (Stack) - Explores deep, often non-optimal. |
| **BFS** | Uninformed | None | FIFO (Queue) - Guarantees the shortest path. |
| **A\*** | Informed | **Manhattan** | Priority Queue - Optimizes based on $f(n) = g(n) + h(n)$. |

##  Performance Analytics & Statistics
To fulfill the analytical requirements of the DSA course, the application tracks:
* **Nodes Visited:** Measures the "exploration overhead" (efficiency of the search).
* **Path Length:** Final distance from Start $\rightarrow$ 4 Targets $\rightarrow$ Exit.
* **Visual Step-through:** Demonstrates how heuristics (like Manhattan) significantly prune the search space compared to BFS.

##  Technical Stack
* **Language:** Python 3.x
* **GUI Library:** Tkinter
* **Core Concepts:**
    * Graph Representation (Adjacency logic)
    * Priority Queues & Heuristics
    * Disjoint Set Union (DSU) for Kruskal's
    * State-machine logic for item collection

##  How to Run
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/blokzz/DSA-maze.git
    ```
2.  **Navigate to the directory:**
    ```bash
    cd DSA-maze
    ```
3.  **Run the application:**
    ```bash
    python main.py
    ```

---
*Developed as part of the University DSA Curriculum.*
