#include "graph.h"

int main()
{
    Graph g;
    g.add_node("A");
    g.add_node("B");
    g.add_node("C");
    
    /* Example:
     * +------+
     * |  A   |<---+
     * +------+    |
     * |           | 
     * |           | 
     * v           v
     * +----+    +----+
     * | B  |    | C  |
     * +----+    +----+
     */
    g.add_edge("A", "B");
    g.add_edge("A", "C");
    g.add_edge("C", "A");

    auto transition_matrix = g.build_transition_matrix();
    return 0;
}
