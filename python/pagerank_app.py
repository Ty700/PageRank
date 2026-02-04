#!/usr/bin/env python3

import sys
import json
import argparse
from pathlib import Path
from matplotlib.patches import Arc, FancyArrowPatch
import numpy as np  
sys.path.insert(0, str(Path(__file__).parent / 'pagerank'))

import pagerank_cpp


def load_graph_config(config_path):
    """Load graph configuration from JSON file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file '{config_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config file: {e}")
        sys.exit(1)


def build_graph_from_config(config):
    """Build C++ graph from config dict."""
    g = pagerank_cpp.Graph()

    nodes = config.get('nodes', [])
    if not nodes:
        print("Error: No nodes defined in config.")
        sys.exit(1)

    for node in nodes:
        g.add_node(str(node))

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
    return graph.compute_pagerank()


def print_results(graph, result):
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
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
        import matplotlib.cm as cm
        import matplotlib.colors as mcolors
    except ImportError:
        print("Error: NetworkX and matplotlib required.")
        return

    nodes = graph.get_nodes()
    edges = graph.get_edges()
    scores = result.pagerank_scores

    params = config.get('parameters', {})
    pixel_budget = params.get('pixel_budget', 50000)
    min_size = params.get('min_node_size', 500)
    output_path = params.get('output_path', 'output/pagerank_network.png')

    # Build NetworkX graph
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # Node sizes
    node_sizes = [max(min_size, s * pixel_budget) for s in scores]
    node_size_dict = dict(zip(nodes, node_sizes))

    # Colors
    colormap = cm.get_cmap('tab20' if len(nodes) > 10 else 'tab10')
    node_color_map = {
        node: colormap(i / max(len(nodes) - 1, 1))
        for i, node in enumerate(nodes)
    }

    # Layout
    layout = params.get('layout', 'spring')
    if layout == 'circular':
        pos = nx.circular_layout(G, scale=2)
    elif layout == 'kamada_kawai':
        pos = nx.kamada_kawai_layout(G, scale=2)
    else:
        pos = nx.spring_layout(G, seed=42, k=3, iterations=50, scale=2)

    fig, ax = plt.subplots(figsize=(18, 14))

    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos,
        node_size=node_sizes,
        node_color=[node_color_map[n] for n in nodes],
        edgecolors='black',
        linewidths=3,
        alpha=0.9,
        ax=ax
    )

    # Separate edges
    regular_edges = [(s, d) for s, d in edges if s != d]

    # Draw regular edges grouped by source color
    from collections import defaultdict
    edges_by_color = defaultdict(list)

    for s, d in regular_edges:
        edges_by_color[mcolors.to_hex(node_color_map[s])].append((s, d))

    for color, elist in edges_by_color.items():
        nx.draw_networkx_edges(
            G, pos,
            edgelist=elist,
            edge_color=color,
            arrows=True,
            arrowstyle='->',
            arrowsize=20,
            width=2.5,
            alpha=0.85,
            node_size=node_sizes,
            min_target_margin=15,
            connectionstyle='arc3,rad=0.15',
            ax=ax
        )

    # Labels
    nx.draw_networkx_labels(
        G, pos,
        font_size=18,
        font_weight='bold',
        font_color='black',
        ax=ax
    )

    # Legend
    legend = "PageRank Scores:\n" + "\n".join(
        f"{n}: {s:.4f}" for n, s in zip(nodes, scores)
    )
    ax.text(
        0.02, 0.98, legend,
        transform=ax.transAxes,
        va='top',
        fontsize=13,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9),
        family='monospace'
    )

    ax.set_title("PageRank Visualization", fontsize=20, fontweight='bold', pad=25)
    ax.axis('off')
    ax.set_aspect('equal')

    xs, ys = zip(*pos.values())
    margin = 0.5
    ax.set_xlim(min(xs) - margin, max(xs) + margin)
    ax.set_ylim(min(ys) - margin, max(ys) + margin)

    output_file = Path(__file__).parent / output_path
    output_file.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Visualization saved to: {output_file}")

    if params.get('show_plot', False):
        plt.show()

    plt.close()


def main():
    parser = argparse.ArgumentParser(description="PageRank tool")
    parser.add_argument('-c', '--config', default='graph_config.json')
    parser.add_argument('-v', '--visualize', action='store_true')
    parser.add_argument('--no-print', action='store_true')
    args = parser.parse_args()

    config_path = Path(__file__).parent / args.config
    print(f"Loading configuration from: {config_path}")

    config = load_graph_config(config_path)
    graph = build_graph_from_config(config)

    print(f"Nodes: {graph.num_nodes()}")
    print(f"Edges: {len(graph.get_edges())}")

    result = compute_pagerank(graph)

    if not args.no_print:
        print_results(graph, result)

    if args.visualize or config.get('parameters', {}).get('visualize', False):
        visualize_graph(graph, result, config)

    print("Done!")


if __name__ == "__main__":
    main()

