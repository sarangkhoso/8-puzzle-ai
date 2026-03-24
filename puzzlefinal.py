import streamlit as st
import time, tracemalloc, heapq, random, pandas as pd
from collections import deque

st.set_page_config(page_title="8 Puzzle AI Lab", layout="centered")

GOAL = (1,2,3,4,5,6,7,8,0)
MAX_TREE = 300
MOVES = {
    0:[1,3],1:[0,2,4],2:[1,5],
    3:[0,4,6],4:[1,3,5,7],5:[2,4,8],
    6:[3,7],7:[4,6,8],8:[5,7]
}

def manhattan(s):
    return sum(abs(i//3-(v-1)//3)+abs(i%3-(v-1)%3) for i,v in enumerate(s) if v!=0)

def misplaced(s):
    return sum(1 for i,v in enumerate(s) if v!=0 and v!=GOAL[i])

def neighbors(s):
    z=s.index(0)
    res=[]
    for m in MOVES[z]:
        l=list(s)
        l[z],l[m]=l[m],l[z]
        res.append(tuple(l))
    return res

def bfs(start):
    tracemalloc.start(); t0=time.time()
    q=deque([(start,[])])
    vis=set(); nodes=0
    while q:
        s,p=q.popleft(); nodes+=1
        if s==GOAL:
            _,mem=tracemalloc.get_traced_memory()
            return p,nodes,time.time()-t0,mem,True
        vis.add(s)
        for n in neighbors(s):
            if n not in vis:
                q.append((n,p+[n]))
    _,mem=tracemalloc.get_traced_memory()
    return None,nodes,time.time()-t0,mem,False

def dfs(start,limit=40):
    tracemalloc.start(); t0=time.time()
    stck=[(start,[])]
    vis=set(); nodes=0
    while stck:
        s,p=stck.pop(); nodes+=1
        if s==GOAL:
            _,mem=tracemalloc.get_traced_memory()
            return p,nodes,time.time()-t0,mem,False
        if len(p)>limit: continue
        vis.add(s)
        for n in neighbors(s):
            if n not in vis:
                stck.append((n,p+[n]))
    _,mem=tracemalloc.get_traced_memory()
    return None,nodes,time.time()-t0,mem,False

def ucs(start):
    tracemalloc.start(); t0=time.time()
    heap=[(0,start,[])]
    vis=set(); nodes=0
    while heap:
        c,s,p=heapq.heappop(heap); nodes+=1
        if s==GOAL:
            _,mem=tracemalloc.get_traced_memory()
            return p,nodes,time.time()-t0,mem,True
        if s in vis: continue
        vis.add(s)
        for n in neighbors(s):
            heapq.heappush(heap,(c+1,n,p+[n]))
    _,mem=tracemalloc.get_traced_memory()
    return None,nodes,time.time()-t0,mem,False

def greedy(start):
    tracemalloc.start(); t0=time.time()
    heap=[(manhattan(start),start,[])]
    vis=set(); nodes=0
    while heap:
        _,s,p=heapq.heappop(heap); nodes+=1
        if s==GOAL:
            _,mem=tracemalloc.get_traced_memory()
            return p,nodes,time.time()-t0,mem,False
        vis.add(s)
        for n in neighbors(s):
            if n not in vis:
                heapq.heappush(heap,(manhattan(n),n,p+[n]))
    _,mem=tracemalloc.get_traced_memory()
    return None,nodes,time.time()-t0,mem,False

def astar(start,heuristic):
    tracemalloc.start(); t0=time.time()
    heap=[(heuristic(start),0,start,[])]
    vis=set(); nodes=0
    while heap:
        f,g,s,p=heapq.heappop(heap); nodes+=1
        if s==GOAL:
            _,mem=tracemalloc.get_traced_memory()
            return p,nodes,time.time()-t0,mem,True
        vis.add(s)
        for n in neighbors(s):
            if n not in vis:
                heapq.heappush(heap,(g+1+heuristic(n),g+1,n,p+[n]))
    _,mem=tracemalloc.get_traced_memory()
    return None,nodes,time.time()-t0,mem,False

def ida_star(start):
    tracemalloc.start(); t0=time.time()
    bound=manhattan(start)
    path=[start]; nodes=0
    def search(g,b):
        nonlocal nodes
        node=path[-1]
        f=g+manhattan(node)
        if f>b: return f
        if node==GOAL: return "FOUND"
        m=float("inf")
        for n in neighbors(node):
            if n not in path:
                path.append(n); nodes+=1
                t=search(g+1,b)
                if t=="FOUND": return "FOUND"
                if t<m: m=t
                path.pop()
        return m
    while True:
        t=search(0,bound)
        if t=="FOUND":
            _,mem=tracemalloc.get_traced_memory()
            return path[1:],nodes,time.time()-t0,mem,True
        if t == float("inf"):
            _,mem=tracemalloc.get_traced_memory()
            return None,nodes,time.time()-t0,mem,False
        bound=t

def solvable(s):
    arr=[x for x in s if x!=0]
    inv=sum(arr[i]>arr[j] for i in range(len(arr)) for j in range(i+1,len(arr)))
    return inv%2==0

def random_puzzle():
    while True:
        s=list(GOAL)
        random.shuffle(s)
        if solvable(s) and tuple(s)!=GOAL:
            return tuple(s)

if "state" not in st.session_state:
    st.session_state.state=list(GOAL)
if "last_path" not in st.session_state:
    st.session_state.last_path=[]

st.title("🧩 8 Puzzle AI Lab (Styled Tiles)")

def show_puzzle_tiles(state):
    st.write("Current Puzzle:")
    for r in range(3):
        cols = st.columns(3)
        for c in range(3):
            val = state[r*3 + c]
            if val != 0:
                style = (
                    "width:70px; height:70px; background-color:white; "
                    "color:black; border-radius:15px; font-weight:bold; "
                    "font-size:32px; display:flex; justify-content:center; align-items:center; "
                    "border: 2px solid black; user-select:none;"
                )
                cols[c].markdown(f"<div style='{style}'>{val}</div>", unsafe_allow_html=True)
            else:
                style = (
                    "width:70px; height:70px; background-color:#B0B0B0; "
                    "border-radius:15px; border: 2px solid black;"
                )
                cols[c].markdown(f"<div style='{style}'></div>", unsafe_allow_html=True)

show_puzzle_tiles(st.session_state.state)

algo = st.selectbox("Algorithm", ["BFS","DFS","UCS","Greedy","A*_Manhattan","A*_Misplaced","IDA*"])

col1, col2, col3 = st.columns(3)
if col1.button("🎲 Random"):
    st.session_state.state = list(random_puzzle())
if col2.button("Reset"):
    st.session_state.state = list(GOAL)

if col3.button("Solve"):
    start = tuple(st.session_state.state)
    if not solvable(start):
        st.error("Not solvable")
    else:
        if algo == "BFS":
            res = bfs(start)
        elif algo == "DFS":
            res = dfs(start)
        elif algo == "UCS":
            res = ucs(start)
        elif algo == "Greedy":
            res = greedy(start)
        elif algo == "A*_Manhattan":
            res = astar(start, manhattan)
        elif algo == "A*_Misplaced":
            res = astar(start, misplaced)
        else:
            res = ida_star(start)

        if res is None or res[0] is None:
            st.error("No solution found by this algorithm.")
        else:
            path, nodes, t, mem, opt = res
            st.session_state.last_path = path
            st.success(f"Steps: {len(path)} | Time: {t:.4f}s | Nodes expanded: {nodes}")

            for step, state in enumerate(path):
                st.write(f"Step {step+1}:")
                show_puzzle_tiles(state)
                time.sleep(0.4)

if st.button("📊 Compare All"):
    start = tuple(st.session_state.state)
    data = []
    algos = {
        "BFS": bfs,
        "DFS": dfs,
        "UCS": ucs,
        "Greedy": greedy,
        "A*_Manhattan": lambda s: astar(s, manhattan),
        "A*_Misplaced": lambda s: astar(s, misplaced),
        "IDA*": ida_star
    }
    for name, fn in algos.items():
        res = fn(start)
        if res is None or res[0] is None:
            data.append([name, None, None])
        else:
            path, nodes, t, mem, opt = res
            data.append([name, t, nodes])
    df = pd.DataFrame(data, columns=["Algorithm", "Time (s)", "Nodes Expanded"])
    st.dataframe(df)
    st.bar_chart(df.set_index("Algorithm"))