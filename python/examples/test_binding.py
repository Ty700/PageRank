#!/usr/bind/env python3

import sys 
sys.path.insert(0, '../pagerank') 

import pagerank_cpp

def test_pagerank():
    g = pagerank_cpp.Graph()

    g.add_node("A")
    g.add_node("B")
    g.add_node("C")
    g.add_node("D")
    g.add_node("E")
    
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("A", "D")

    g.add_edge("B", "C")
    g.add_edge("B", "E")

    g.add_edge("C", "D")

    result = g.compute_pagerank()
    
    print("=" * 30)
    print("PageRank Results:")
    for idx, rank in enumerate(result.pagerank_scores):
        print(f"Node {idx}: {rank:.6f}")
    print("=" * 30)

    print("Convergence History:")
    for i, diff in enumerate(result.convergence_history):
        print(f"Iteration {i + 1}: Difference = {diff:.6f}")
    print("=" * 30)

    print("Iterations:", result.num_iterations)
    print("=" * 30)

if __name__ == "__main__":
    test_pagerank()
