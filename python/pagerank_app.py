#!/usr/bin/env python3

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'pagerank'))

import pagerank_cpp


def load_graph_config(config_path):
    """Load graph configuration from JSON file."""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Error: Config file '{config_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config file: {e}")
        sys.exit(1)


def build_graph_from_config(config):
    """Build C++ graph from config dict."""
    g = pagerank_cpp.Graph()
    
    # Add nodes
    nodes = config.get('nodes', [])
    if not nodes:
        print("Error: No nodes defined in config.")
        sys.exit(1)
    
    for node in nodes:
        g.add_node(str(node))
    
    # Add edges
    edges = config.get('edges', [])
    if not edges:
        print("Warning: No edges defined in config.")
    
    for edge in edges:
        if len(edge) != 2:
            print(f"Warning: Invalid edge format {edge}, skipping.")
            continue
        src, dest = edge
        g.add_edge(str(src), str(dest))
    
    return g


def compute_pagerank(graph):
    """Compute PageRank and return result."""
    result = graph.compute_pagerank()
    return result


def print_results(graph, result):
    """Print PageRank results to console."""
    nodes = graph.get_nodes()
    scores = result.pagerank_scores
    
    print("\n" + "=" * 50)
    print("PageRank Results:")
    print("=" * 50)
    for node, score in zip(nodes, scores):
        print(f"  {node}: {score:.6f}")
    print("=" * 50)
    print(f"Converged in {result.num_iterations} iterations")
    print("=" * 50 + "\n")

def visualize_graph(graph, result, config):
    """Generate visualization using NetworkX and matplotlib."""
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
        import matplotlib.cm as cm
        from matplotlib.patches import FancyArrowPatch, Arc
        import numpy as np
    except ImportError:
        print("Error: NetworkX and matplotlib required for visualization.")
        print("Install with: pip install networkx matplotlib")
        return
    
    # Get graph data
    nodes = graph.get_nodes()
    edges = graph.get_edges()
    scores = result.pagerank_scores
    
    # Get visualization parameters
    params = config.get('parameters', {})
    pixel_budget = params.get('pixel_budget', 50000)
    min_size = params.get('min_node_size', 500)
    output_path = params.get('output_path', 'output/pagerank_network.png')
    
    # Build NetworkX graph
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    
    # Separate self-loops from regular edges
    self_loops = []
    regular_edges = []
    for src, dest in edges:
        if src == dest:
            self_loops.append((src, dest))
        else:
            regular_edges.append((src, dest))
    
    # Add only regular edges to NetworkX graph
    G.add_edges_from(regular_edges)
    
    # Calculate node sizes
    node_sizes = [max(min_size, rank * pixel_budget) for rank in scores]
    node_size_dict = {node: size for node, size in zip(nodes, node_sizes)}
    
    # Assign distinct colors to each node
    n_nodes = len(nodes)
    colormap = cm.get_cmap('tab10')
    if n_nodes > 10:
        colormap = cm.get_cmap('tab20')
    
    node_color_map = {}
    node_colors = []
    for i, node in enumerate(nodes):
        color = colormap(i / max(n_nodes - 1, 1))
        node_color_map[node] = color
        node_colors.append(color)
    
    # Calculate layout
    layout_type = params.get('layout', 'spring')
    
    if layout_type == 'circular':
        pos = nx.circular_layout(G, scale=2)
    elif layout_type == 'kamada_kawai':
        try:
            pos = nx.kamada_kawai_layout(G, scale=2)
        except:
            pos = nx.spring_layout(G, seed=42, k=3, iterations=50, scale=2)
    else:  # spring (default)
        pos = nx.spring_layout(G, seed=42, k=3, iterations=50, scale=2)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(18, 14))
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos,
                          node_size=node_sizes,
                          node_color=node_colors,
                          alpha=0.9,
                          edgecolors='black',
                          linewidths=3,
                          ax=ax)
    
    # Draw regular edges one by one with source node color
    for src, dest in regular_edges:
        edge_color = node_color_map[src]
        temp_node_sizes = [node_size_dict[n] for n in G.nodes()]
        nx.draw_networkx_edges(G, pos,
                              edgelist=[(src, dest)],
                              edge_color=[edge_color],
                              arrows=True,
                              arrowstyle='->',
                              arrowsize=25,
                              width=3,
                              alpha=0.85,
                              node_size=temp_node_sizes,
                              min_target_margin=20,
                              connectionstyle='arc3,rad=0.15',
                              ax=ax)
    
    # Draw self-loops manually as small circles above nodes
    for src, dest in self_loops:
        x, y = pos[src]
        edge_color = node_color_map[src]

        # Estimate node radius from node size
        # node_size is in points^2, convert to approximate data units
        node_radius = 0.15  # Approximate radius in data coordinates
        
        # Loop positioned above the node, starting from edge
        loop_offset_y = 0.35  # Height above node center
        loop_center_y = y + node_radius + loop_offset_y  # Start from top edge
        loop_radius = 0.18
        
        # Draw semi-circle arc
        loop = Arc(
            xy=(x, loop_center_y),
            width=loop_radius * 2,
            height=loop_radius * 2,
            angle=0,
            theta1=20,
            theta2=340,
            color=edge_color,
            linewidth=4,
            alpha=0.85,
            capstyle='round'
        )
        ax.add_patch(loop)
        
        # Add arrowhead at end of arc
        arrow_angle = np.radians(340)
        arrow_x = x + loop_radius * np.cos(arrow_angle)
        arrow_y = loop_center_y + loop_radius * np.sin(arrow_angle)
        
        # Arrow should point back toward the node edge
        dx = 0.04
        dy = -0.05
        
        ax.annotate('',
                   xy=(arrow_x - dx, arrow_y - dy),  # Point toward node
                   xytext=(arrow_x, arrow_y),
                   arrowprops=dict(
                       arrowstyle='->',
                       color=edge_color,
                       lw=4,
                       alpha=0.85,
                       shrinkA=0,
                       shrinkB=0
                   ))    # Draw labels

        nx.draw_networkx_labels(G, pos,
                               font_size=18,
                               font_weight='bold',
                               font_family='sans-serif',
                               font_color='black',
                               ax=ax)
        
        # Add legend
        legend_text = "PageRank Scores:\n" + "\n".join(
            [f"{node}: {score:.4f}" for node, score in zip(nodes, scores)]
        )
        ax.text(0.02, 0.98, legend_text,
                transform=ax.transAxes,
                verticalalignment='top',
                fontsize=13,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9, pad=0.8),
                family='monospace')
        
        ax.set_title("PageRank Visualization", fontsize=20, fontweight='bold', pad=25)
        ax.axis('off')
        ax.set_aspect('equal')
        
        # Set axis limits with padding
        all_x = [pos[node][0] for node in nodes]
        all_y = [pos[node][1] for node in nodes]
        margin = 0.5
        ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
        ax.set_ylim(min(all_y) - margin, max(all_y) + margin + 0.3)  # Extra for loops
        
        plt.tight_layout()
        
        # Ensure output directory exists
        output_file = Path(__file__).parent / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Save
        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Visualization saved to: {output_file}")
        
        # Show if requested
        if params.get('show_plot', False):
            plt.show()
        
        plt.close()

def main():
    parser = argparse.ArgumentParser(
        description='PageRank computation and visualization tool'
    )
    parser.add_argument('--config', '-c',
                       default='graph_config.json',
                       help='Path to graph configuration JSON file (default: graph_config.json)')
    parser.add_argument('--visualize', '-v',
                       action='store_true',
                       help='Generate visualization (requires NetworkX and matplotlib)')
    parser.add_argument('--no-print',
                       action='store_true',
                       help='Suppress console output of results')
    
    args = parser.parse_args()
    
    # Resolve config path relative to script location
    config_path = Path(__file__).parent / args.config
    
    # Load config
    print(f"Loading configuration from: {config_path}")
    config = load_graph_config(config_path)
    
    # Build graph
    print("Building graph...")
    graph = build_graph_from_config(config)
    print(f"  Nodes: {graph.num_nodes()}")
    print(f"  Edges: {len(graph.get_edges())}")
    
    # Compute PageRank
    print("Computing PageRank...")
    result = compute_pagerank(graph)
    
    # Print results
    if not args.no_print:
        print_results(graph, result)
    
    # Visualize if requested
    if args.visualize or config.get('parameters', {}).get('visualize', False):
        print("Generating visualization...")
        visualize_graph(graph, result, config)
    
    print("Done!")


if __name__ == "__main__":
    main()

