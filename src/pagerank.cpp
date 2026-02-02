#include "graph.h"

int main()
{
    /* 
     * C++ is purely the backend for this project. 
     * All the main logic and interaction is handled in Python.
     * This file is just for testing and debugging purposes.
     * To compile this file with debugging information, use the -d flag.
     */
    #ifdef DEBUG 
        Graph g;
        g.add_node("A");
        g.add_node("B");
        g.add_node("C");
        g.add_node("D");
        g.add_node("E");
        
        g.add_edge("A", "B");
        g.add_edge("A", "C");
        g.add_edge("A", "D");

        g.add_edge("B", "C");
        g.add_edge("B", "E");

        g.add_edge("C", "D");
        auto page_rank = g.compute_pagerank(); 
    #endif

    return 0;
}
