#!/usr/bind/env python3

import sys 
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm

sys.path.insert(0, '../pagerank') 

import pagerank_cpp

def test_pagerank():
    g = pagerank_cpp.Graph()
    
    # This will be passed in via JSON from the webserver eventually
    g.add_node("A")
    g.add_node("B")
    g.add_node("C")
    g.add_node("D")
    g.add_node("E")
    g.add_node("F")

    g.add_edge("B", "C")
    g.add_edge("B", "E")

    g.add_edge("C", "D")

    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("A", "D")

    g.add_edge("F", "A")

    result = g.compute_pagerank()
    scores = result.pagerank_scores
    nodes = g.get_nodes()
    edges = g.get_edges()
    edges.sort()
    
    # G => Visual graph
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    
    # Cal pixel sizes of each node (based on the rank)
    TOTAL_PIXEL_COUNT = 50_000
    min_size = 500
    node_sizes = [max(min_size, rank * TOTAL_PIXEL_COUNT) for rank in scores]
    
    # Gradient node colors
    node_colors = [cm.Blues(rank * 2.5) for rank in scores]  
    
    # Calculate node placement
    pos = nx.spring_layout(G, seed=42, k=1.5)  
    
    # Create figure
    plt.figure(figsize=(14, 10))
     
    nx.draw_networkx_nodes(G, pos, 
                          node_size=node_sizes, 
                          node_color=node_colors,
                          alpha=0.9,
                          edgecolors='black',
                          linewidths=2)
    
    nx.draw_networkx_edges(G, pos, 
                          arrows=True,
                          arrowstyle='->',
                          arrowsize=25,
                          edge_color='gray',
                          width=2.5,
                          connectionstyle='arc3,rad=0.1',
                           node_size=node_sizes,        
                      min_target_margin=15)         
    
    nx.draw_networkx_labels(G, pos, 
                           font_size=14, 
                           font_weight='bold',
                           font_family='sans-serif')
    
    legend_text = "PageRank Scores:\n" + "\n".join(
        [f"{node}: {score:.4f}" for node, score in zip(nodes, scores)]
    )

    plt.text(0.02, 0.98, legend_text, 
            transform=plt.gca().transAxes,
            verticalalignment='top',
            fontsize=12,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.title("PageRank Visualization", fontsize=16, fontweight='bold')
    plt.axis('off')

    # Save and/or show
    plt.tight_layout()
    plt.savefig('./outputs/pagerank_network.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    test_pagerank()
