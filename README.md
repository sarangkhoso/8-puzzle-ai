# 🧩 8-Puzzle AI Lab

A **web-based interactive 8-Puzzle solver** using multiple AI search algorithms, built with **Streamlit**. This app allows users to experiment with classic AI algorithms on the 8-puzzle problem, visualize solutions step-by-step, and compare the efficiency of different algorithms.

---

## **Table of Contents**

- [Overview](#overview)  
- [Features](#features)  
- [Algorithms Implemented](#algorithms-implemented)  
- [How It Works](#how-it-works)  
- [Installation & Deployment](#installation--deployment)  
- [Usage](#usage)  
- [Technical Details](#technical-details)  
- [Screenshots](#screenshots)  
- [License](#license)

---

## **Overview**

The **8-Puzzle problem** is a sliding puzzle that consists of a 3x3 grid with 8 numbered tiles and one empty space. The goal is to move the tiles to reach a specified target configuration (the goal state):

Where `0` represents the empty space.  

This app allows users to:

- Solve any valid 8-puzzle configuration using AI algorithms.
- Visualize the puzzle state as **block-style tiles**.
- Animate the solution step-by-step.
- Compare algorithm performance based on **time taken** and **nodes expanded**.

---

## **Features**

- **Random Puzzle Generator:** Generate solvable random puzzle states for experimentation.
- **Reset to Goal:** Instantly reset the puzzle to the solved state.
- **Step-by-Step Animation:** Watch each move of the solution executed in real time.
- **Algorithm Selection:** Choose from multiple AI search strategies:
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - Uniform Cost Search (UCS)
  - Greedy Best-First Search
  - A* Search (Manhattan distance or Misplaced tiles heuristic)
  - Iterative Deepening A* (IDA*)
- **Compare Algorithms:** Display a table and chart comparing time and nodes expanded for each algorithm.
- **No Solution Handling:** Clearly indicates if a puzzle is unsolvable or a solution cannot be found.

---

## **Algorithms Implemented**

1. **Breadth-First Search (BFS)** – Explores nodes level by level, guarantees shortest path solution.
2. **Depth-First Search (DFS)** – Explores as deep as possible before backtracking, may not find shortest path.
3. **Uniform Cost Search (UCS)** – Expands nodes based on path cost, guarantees optimal solution for uniform costs.
4. **Greedy Best-First Search** – Uses heuristic only (Manhattan distance) to select nodes; fast but not always optimal.
5. **A* Search** – Combines path cost + heuristic (Manhattan or Misplaced tiles), guarantees optimal solution if heuristic is admissible.
6. **Iterative Deepening A* (IDA*)** – Space-efficient version of A*, gradually deepens search bound using heuristic.

---

## **How It Works**

1. **Puzzle Representation:**  
   - The puzzle is represented as a tuple of 9 numbers `(0-8)` where `0` is the empty space.
   - Moves are computed based on adjacency in a 3x3 grid.

2. **Solvers:**  
   - Each algorithm function returns a tuple:  
     ```
     (solution_path, nodes_expanded, time_taken, memory_used, is_optimal)
     ```
   - If a solution is not found, the path is `None`.

3. **User Interface:**  
   - Built with **Streamlit**, featuring:
     - Dropdown to select algorithm.
     - Buttons for **Random Puzzle**, **Reset**, **Solve**, and **Compare All**.
     - Styled visual tiles for puzzle representation.
     - Step-by-step solution display with animation.

4. **Performance Tracking:**  
   - Time is measured using `time.time()`.
   - Memory usage is tracked using `tracemalloc`.
   - Nodes expanded are counted during search.
   - Compare All button shows **table and chart** for all algorithms.

---

## **Installation & Deployment**

### **Local Setup**

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/8-puzzle-ai.git
   cd 8-puzzle-ai
   
   Install dependencies:
   pip install -r requirements.txt
   
   Run the Streamlit app:
   streamlit run puzzlefinal.py

   ### Deploy Online with Streamlit Cloud

1. Push your repository to **GitHub**.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/) and log in.
3. Click **New app**, select your GitHub repository, branch, and the `puzzlefinal.py` file.
4. Click **Deploy** – your app is now online and shareable.

---

## Usage

1. Select an algorithm from the dropdown.
2. Use **Random Puzzle** to generate a new puzzle.
3. Click **Solve** to execute the selected algorithm.
4. View step-by-step solution or compare all algorithms.
5. Reset puzzle to the goal state anytime.

---

## Technical Details

- **Language & Framework:** Python 3.10+, Streamlit
- **Data Structures:**
  - Puzzle state as a tuple
  - Queue for BFS
  - Stack for DFS
  - Min-heap for UCS, Greedy, A*
  - Recursive stack for IDA*
- **Heuristics:**
  - Manhattan Distance
  - Misplaced Tiles
- **Memory Management:** Uses `tracemalloc` for memory profiling
- **Performance Metrics:**
  - Time taken per algorithm
  - Number of nodes expanded
  - Optimality check

---
