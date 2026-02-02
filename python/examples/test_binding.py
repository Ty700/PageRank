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

    for i, val in enumerate(result):
        print(f"  rank[{i}] = {val}")

if __name__ == "__main__":
    test_pagerank()
