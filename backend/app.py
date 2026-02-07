from datetime import datetime
from flask import Flask, jsonify, request, send_file
import sys 
import secrets
from pathlib import Path 
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import shutil

sys.path.insert(0, str(Path(__file__).parent / 'python' / 'pagerank'))
import pagerank_cpp

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# In-memory storage for graphs, keyed by session ID to allow multiple users to have their own graphs
# TODO: Transfer to database for persistence and scalability
graphs = {}
@app.route('/api/graph', methods=['POST'])
def create_graph():
    # Get or create session ID
    session_id = request.cookies.get('session_id')
    if not session_id:
        session_id = secrets.token_hex(16)
    
    data = request.get_json()
    if not data or 'edges' not in data or 'nodes' not in data:
        return jsonify({'error': 'Invalid input data'}), 400

    # Init graph 
    graph = pagerank_cpp.Graph()

    # Add Nodes 
    for node in data['nodes']:
        graph.add_node(str(node))

    # Add Edges 
    for edge in data['edges']:
        if len(edge) != 2:
            return jsonify({'error': 'Each edge must have exactly two nodes'}), 400
        graph.add_edge(str(edge[0]), str(edge[1]))
    
    # Store the graph
    graphs[session_id] = {
        'graph': graph,
        'nodes': data['nodes'],
        'edges': data['edges']
    }

    # Create response and set cookie
    response = jsonify({
        'message': 'Graph created successfully',
        'num_nodes': graph.num_nodes(),
        'num_edges': len(graph.get_edges())
    })
    response.set_cookie('session_id', session_id, httponly=True, samesite='Lax')
    return response, 201

@app.route('/api/pagerank', methods=['GET'])
def compute_pagerank():
    # Grab the session ID to retrieve the user's graphs
    session_id = request.cookies.get('session_id')
    if not session_id or session_id not in graphs:
        return jsonify({'error': 'No graph found for this session'}), 404
    
    graph_data = graphs[session_id]
    graph = graph_data['graph']
    nodes = graph_data['nodes']

    # Sends a request to the C++ backend to compute PageRank and returns the results as JSON
    result = graph.compute_pagerank()

    graphs[session_id]['pagerank'] = result 

    return jsonify({
        'scores': {node: score for node, score in zip(nodes, result.pagerank_scores)},
        'iterations': result.num_iterations,
        'convergence_history': result.convergence_history
    }), 200

@app.route('/api/visualize', methods=['GET'])
def visualize_graph():
    # Grab the session ID to retrieve the user's graphs
    session_id = request.cookies.get('session_id')
    if not session_id or session_id not in graphs:
        return jsonify({'error': 'No graph found for this session'}), 404
    
    nodes = graphs[session_id]['nodes']
    edges = graphs[session_id]['edges']
    scores = graphs[session_id]['pagerank'].pagerank_scores

    pixel_budget = 50000
    min_size = 500

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
    pos = nx.circular_layout(G, scale=2)

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

    
    # Create output directory if it doesn't exist
    output_path = Path(__file__).parent / 'output' / session_id 
    output_path.mkdir(parents=True, exist_ok=True)

    # Create file name with timestamp to avoid overwriting previous visualizations
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    output_file = output_path / f"{timestamp}_visual.png"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_file, dpi=600, bbox_inches='tight', facecolor='white')
    
    return send_file(str(output_file), mimetype='image/png')

@app.route('/api/clear', methods=['POST'])
def clear_graph():
    """Clear the current session's graph and delete output files."""
    session_id = request.cookies.get('session_id') 
    
    if session_id and session_id in graphs:
        # Delete graph from memory
        del graphs[session_id]
        
        # Delete output directory for this session
        output_dir = Path(__file__).parent / 'output' / session_id
        if output_dir.exists():
            shutil.rmtree(output_dir)
            return jsonify({
                'message': 'Graph and output files cleared successfully'
            }), 200
        else:
            return jsonify({
                'message': 'Graph cleared (no output files found)'
            }), 200
    else:
        return jsonify({'error': 'No graph found for this session'}), 404

def cleanup_old_sessions(max_age_hours=24):
    """Remove sessions older than max_age_hours."""
    current_time = time.time()
    output_base = Path(__file__).parent / 'output'
    
    if not output_base.exists():
        return
    
    for session_dir in output_base.iterdir():
        if session_dir.is_dir():
            # Check directory age
            dir_age_hours = (current_time - session_dir.stat().st_mtime) / 3600
            
            if dir_age_hours > max_age_hours:
                # Remove from memory if exists
                session_id = session_dir.name
                if session_id in graphs:
                    del graphs[session_id]
                
                # Remove directory
                shutil.rmtree(session_dir)
                print(f"Cleaned up old session: {session_id}")

if __name__ == '__main__':
    cleanup_old_sessions()  # Clean up old sessions on start
    app.run(debug=True, host='0.0.0.0', port=5000)
