"""
Autonomous Assessment Solver & Technical Round Prep Kit for Vansh Sharma
Engineered for HackerEarth, HackerRank, Codility, CoderPad, and LeetCode style assessments.
Provides:
1. DSA & Python Optimal Solutions (with time/space complexity analysis)
2. Core Technical Cheatsheets (Python internals, PyTorch, LangGraph, RAG, SQL)
3. Architecture & System Design briefs tailored to Vansh's real projects (ResearchMind, LexAI)
Strictly 0 em-dashes and clean formatting.
"""
import sys
import os
import re
import json

BASE_DIR = r"D:\opencode stuff\job-agents"

# Common patterns in entry-level & fresher AI/ML coding tests
DSA_TOPICS = {
    "sliding_window": {
        "title": "Sliding Window / Two Pointers",
        "example": "Longest substring without repeating characters / Maximum subarray sum of size K",
        "pattern": "Use two pointers (left, right) with a hash map / set to maintain window invariants in O(N) time."
    },
    "dynamic_programming": {
        "title": "Dynamic Programming & Memoization",
        "example": "0/1 Knapsack, Coin Change, Longest Common Subsequence",
        "pattern": "Identify state variables, write recurrence relation, memoize with @functools.lru_cache or 1D/2D array."
    },
    "graphs_bfs_dfs": {
        "title": "Graph Traversal (BFS / DFS)",
        "example": "Shortest path in unweighted grid, Topological sort, Cycle detection",
        "pattern": "Use collections.deque for BFS (shortest path), recursion/stack with visited set for DFS."
    },
    "trees": {
        "title": "Binary Trees & BSTs",
        "example": "Lowest Common Ancestor, Tree diameter, Level order traversal",
        "pattern": "Post-order traversal for bottom-up computation; BFS for level order."
    },
    "fast_io": {
        "title": "Python Fast I/O & Competitive Programming Boilerplate",
        "example": "HackerEarth / HackerRank standard input handling",
        "pattern": "import sys; input = sys.stdin.read; data = input().split()"
    }
}

TECHNICAL_CHEATSHEET = {
    "python": [
        "GIL (Global Interpreter Lock): Restricts multi-threaded Python bytecode execution to a single core. Use multiprocessing or asyncio for parallel IO-bound workloads.",
        "Generators vs Iterators: Generators yield values on the fly with lazy evaluation, keeping memory complexity at O(1).",
        "Memory Management: Python uses reference counting combined with a cyclic garbage collector (gc module)."
    ],
    "rag_ai": [
        "Hybrid Retrieval: Combining BM25 keyword search with dense vector embeddings (FAISS/ChromaDB) to capture exact acronyms and semantic relevance.",
        "Reranking: Using cross-encoders (e.g. BGE-Reranker) on top-k candidates to boost precision before LLM generation.",
        "Chunking Strategies: Recursive character splitting with 10-15% token overlap to preserve sentence boundaries."
    ],
    "fastapi_backend": [
        "Async vs Sync: Define endpoints with async def when using non-blocking IO (asyncpg, httpx); use def for blocking CPU-bound tasks to let FastAPI threadpool handle them.",
        "Pydantic Validation: Validates incoming request payloads and serializes responses with strict type safety."
    ]
}

def generate_dsa_solution(problem_text, language="python"):
    prob_lower = problem_text.lower()
    
    # Identify problem archetype
    archetype = "General Algorithm"
    if any(k in prob_lower for k in ["subarray", "substring", "window", "two sum"]):
        archetype = "Sliding Window / Two Pointers"
        complexity = "O(N) Time, O(min(N, M)) Space"
        code = '''def solve(arr, k=None):
    # Two pointer / Sliding window approach
    n = len(arr)
    left = 0
    curr_sum = 0
    max_ans = 0
    
    for right in range(n):
        curr_sum += arr[right]
        # Invariant maintenance
        while k is not None and curr_sum > k and left <= right:
            curr_sum -= arr[left]
            left += 1
        max_ans = max(max_ans, curr_sum)
        
    return max_ans
'''
    elif any(k in prob_lower for k in ["path", "graph", "grid", "island", "connected", "bfs", "dfs"]):
        archetype = "Graph BFS / DFS"
        complexity = "O(V + E) Time, O(V) Space"
        code = '''from collections import deque

def solve_grid(grid):
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    visited = set()
    queue = deque([(0, 0, 0)]) # (r, c, dist)
    visited.add((0, 0))
    
    while queue:
        r, c, d = queue.popleft()
        if r == rows - 1 and c == cols - 1:
            return d
            
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                if grid[nr][nc] == 0: # Traversable
                    visited.add((nr, nc))
                    queue.append((nr, nc, d + 1))
    return -1
'''
    elif any(k in prob_lower for k in ["dp", "knapsack", "coins", "ways", "subsequence", "maximum profit"]):
        archetype = "Dynamic Programming (Memoization)"
        complexity = "O(N * Target) Time, O(Target) Space"
        code = '''from functools import lru_cache

def solve_dp(values, weights, capacity):
    n = len(values)
    
    @lru_cache(maxsize=None)
    def dp(index, rem_cap):
        if index >= n or rem_cap <= 0:
            return 0
        # Choice 1: Skip
        not_take = dp(index + 1, rem_cap)
        # Choice 2: Take (if within capacity)
        take = 0
        if weights[index] <= rem_cap:
            take = values[index] + dp(index + 1, rem_cap - weights[index])
        return max(take, not_take)
        
    return dp(0, capacity)
'''
    else:
        archetype = "Hash Map / Frequency Counter Optimization"
        complexity = "O(N) Time, O(N) Space"
        code = '''from collections import defaultdict, Counter

def solve_optimal(items):
    counts = Counter(items)
    # Fast retrieval and sorting by frequency
    sorted_items = sorted(counts.items(), key=lambda x: -x[1])
    return sorted_items
'''

    return {
        "archetype": archetype,
        "complexity": complexity,
        "code": code.strip()
    }

def generate_prep_kit(company_name, role_title, test_provider="HackerEarth"):
    clean_comp = company_name.replace("\u2014", " - ").replace("\u2013", " - ").strip()
    clean_role = role_title.replace("\u2014", " - ").replace("\u2013", " - ").strip()

    kit = {
        "company": clean_comp,
        "role": clean_role,
        "provider": test_provider,
        "test_structure": [
            {"section": "Section 1: Data Structures & Algorithms", "duration": "45-60 mins", "details": "2 coding questions (Array/String Two Pointers, Dynamic Programming, or Tree/Graph traversal). Focus on O(N) time complexity."},
            {"section": "Section 2: Python Internals & Core CS", "duration": "20-30 mins", "details": "10-15 MCQs on Python memory model, decorators, GIL, generator behavior, and SQL indexing."},
            {"section": "Section 3: AI/ML Engineering & System Design", "duration": "20 mins", "details": "Questions on RAG architecture, vector distance metrics (Cosine vs L2), handling latency in LLMs, and model evaluation metrics."}
        ],
        "key_talking_points_for_interviews": [
            "ResearchMind: LangGraph multi-agent coordination reducing hallucination rates with hybrid BM25 + FAISS retrieval.",
            "LexAI: Legal intelligence pipeline with sub-200ms latency and exact line-level source attribution.",
            "Production Hygiene: Docker containerization, asynchronous FastAPI endpoints, and automated tests."
        ],
        "top_dsa_patterns": list(DSA_TOPICS.values())[:3],
        "cheatsheet": TECHNICAL_CHEATSHEET
    }
    return kit

if __name__ == "__main__":
    kit = generate_prep_kit("NextAstra", "AI Engineer", "HackerEarth")
    print("Sample Prep Kit Generated:")
    print(f"Company: {kit['company']} | Provider: {kit['provider']}")
    print("DSA Patterns:", len(kit["top_dsa_patterns"]))
