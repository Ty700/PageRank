import React,{ useState } from 'react';
import './PageRank.css';
import { createGraph, computePageRank, getVisualization, clearGraph } from './api/pagerank';

function App() {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [nodeInput, setNodeInput] = useState('');
  const [fromNode, setFromNode] = useState('');
  const [toNode, setToNode] = useState('');
  const [pageRankScores, setPageRankScores] = useState(null);
  const [visualizationUrl, setVisualizationUrl] = useState(null);
  const [iterations, setIterations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Add multiple nodes at once
  const addNode = () => {
    const trimmed = nodeInput.trim();
    if (!trimmed) return;

    // Split by comma, space, or newline
    const newNodes = trimmed
      .split(/[,\s\n]+/)
      .map(n => n.trim())
      .filter(n => n && !nodes.includes(n));

    if (newNodes.length === 0) {
      setError('Node(s) already exist or invalid input');
      setTimeout(() => setError(null), 3000);
      return;
    }

    setNodes([...nodes, ...newNodes]);
    setNodeInput('');
    setError(null);
  };

  // Remove a node
  const removeNode = (nodeToRemove) => {
    setNodes(nodes.filter(n => n !== nodeToRemove));
    // Also remove edges connected to this node
    setEdges(edges.filter(([from, to]) => from !== nodeToRemove && to !== nodeToRemove));
  };

  // Add edge
  const addEdge = () => {
    if (!fromNode || !toNode) {
      setError('Please select both nodes');
      setTimeout(() => setError(null), 3000);
      return;
    }

    const edgeExists = edges.some(([f, t]) => f === fromNode && t === toNode);
    if (edgeExists) {
      setError('Edge already exists');
      setTimeout(() => setError(null), 3000);
      return;
    }

    setEdges([...edges, [fromNode, toNode]]);
    setFromNode('');
    setToNode('');
    setError(null);
  };

  // Remove edge
  const removeEdge = (edgeToRemove) => {
    setEdges(edges.filter(e => e !== edgeToRemove));
  };

  // Load template graphs
  const loadTemplate = (template) => {
    switch(template) {
      case 'star':
        setNodes(['A', 'B', 'C', 'D', 'E']);
        setEdges([['A', 'B'], ['A', 'C'], ['A', 'D'], ['A', 'E']]);
        break;
      case 'cycle':
        setNodes(['A', 'B', 'C', 'D']);
        setEdges([['A', 'B'], ['B', 'C'], ['C', 'D'], ['D', 'A']]);
        break;
      case 'linear':
        setNodes(['A', 'B', 'C', 'D', 'E']);
        setEdges([['A', 'B'], ['B', 'C'], ['C', 'D'], ['D', 'E']]);
        break;
      case 'complete':
        const completeNodes = ['A', 'B', 'C', 'D'];
        const completeEdges = [];
        for (let i = 0; i < completeNodes.length; i++) {
          for (let j = 0; j < completeNodes.length; j++) {
            if (i !== j) {
              completeEdges.push([completeNodes[i], completeNodes[j]]);
            }
          }
        }
        setNodes(completeNodes);
        setEdges(completeEdges);
        break;
      default:
        break;
    }
    setError(null);
    setPageRankScores(null);
    setVisualizationUrl(null);
  };

  // Compute PageRank
  const handleComputePageRank = async () => {
    if (nodes.length === 0) {
      setError('Please add at least one node');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Create graph
      await createGraph(nodes, edges);

      // Compute PageRank
      const result = await computePageRank();
      setPageRankScores(result.scores);
      setIterations(result.iterations);

      // Get visualization
      const vizBlob = await getVisualization();
      const url = URL.createObjectURL(vizBlob);
      setVisualizationUrl(url);
    } catch (err) {
      setError(err.message || 'Failed to compute PageRank');
    } finally {
      setLoading(false);
    }
  };

  // Clear everything
  const handleClear = async () => {
    try {
      await clearGraph();
      setNodes([]);
      setEdges([]);
      setNodeInput('');
      setFromNode('');
      setToNode('');
      setPageRankScores(null);
      setVisualizationUrl(null);
      setIterations(null);
      setError(null);
    } catch (err) {
      setError('Failed to clear graph');
    }
  };

  // Handle Enter key
  const handleKeyPress = (e, action) => {
    if (e.key === 'Enter') {
      action();
    }
  };

  return (
    <div className="App">
      <h1>PageRank Calculator</h1>

      {error && <div className="error">{error}</div>}

      {/* Templates */}
      <div className="section">
        <h3>Quick Start Templates</h3>
        <div className="templates">
          <button onClick={() => loadTemplate('cycle')} className="btn-template">Cycle Graph</button>
          <button onClick={() => loadTemplate('star')} className="btn-template">Star Graph</button>
          <button onClick={() => loadTemplate('linear')} className="btn-template">Linear Chain</button>
          <button onClick={() => loadTemplate('complete')} className="btn-template">Complete Graph</button>
        </div>
      </div>

      {/* Add Nodes */}
      <div className="section">
        <h3>Add Nodes</h3>
        <p className="hint">Enter node names separated by commas or spaces (e.g., "A, B, C" or "A B C")</p>
        <div className="input-group">
          <input
            type="text"
            value={nodeInput}
            onChange={(e) => setNodeInput(e.target.value)}
            onKeyPress={(e) => handleKeyPress(e, addNode)}
            placeholder="A, B, C, D..."
          />
          <button onClick={addNode} className="btn-primary">Add Nodes</button>
        </div>

        {nodes.length > 0 && (
          <div className="chips">
            {nodes.map(node => (
              <span key={node} className="chip">
                {node}
                <button onClick={() => removeNode(node)} className="chip-remove">×</button>
              </span>
            ))}
          </div>
        )}
        {nodes.length === 0 && <p className="empty-state">No nodes yet. Add some above!</p>}
      </div>

      {/* Add Edges */}
      <div className="section">
        <h3>Add Edges</h3>
        <div className="input-group">
          <select 
            value={fromNode} 
            onChange={(e) => setFromNode(e.target.value)}
            disabled={nodes.length === 0}
          >
            <option value="">From node</option>
            {nodes.map(node => (
              <option key={node} value={node}>{node}</option>
            ))}
          </select>

          <span className="arrow">→</span>

          <select 
            value={toNode} 
            onChange={(e) => setToNode(e.target.value)}
            disabled={nodes.length === 0}
          >
            <option value="">To node</option>
            {nodes.map(node => (
              <option key={node} value={node}>{node}</option>
            ))}
          </select>

          <button 
            onClick={addEdge} 
            className="btn-primary"
            disabled={nodes.length === 0}
          >
            Add Edge
          </button>
        </div>

        {edges.length > 0 && (
          <div className="chips">
            {edges.map((edge, idx) => (
              <span key={idx} className="chip edge-chip">
                {edge[0]} → {edge[1]}
                <button onClick={() => removeEdge(edge)} className="chip-remove">×</button>
              </span>
            ))}
          </div>
        )}
        {edges.length === 0 && <p className="empty-state">No edges yet. Add connections above!</p>}
      </div>

      {/* Actions */}
      <div className="actions">
        <button 
          onClick={handleComputePageRank} 
          className="btn-primary"
          disabled={loading || nodes.length === 0}
        >
          {loading ? 'Computing...' : 'Compute PageRank'}
        </button>
        <button 
          onClick={handleClear} 
          className="btn-danger"
          disabled={loading}
        >
          Clear Graph
        </button>
      </div>

      {/* Results */}
      {pageRankScores && (
        <div className="section results">
          <h2>PageRank Results</h2>
          {iterations && (
            <p className="convergence-info">Converged in {iterations} iterations</p>
          )}

          <table>
            <thead>
              <tr>
                <th>Node</th>
                <th>PageRank Score</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(pageRankScores)
                .sort(([, a], [, b]) => b - a)
                .map(([node, score]) => (
                  <tr key={node}>
                    <td><strong>{node}</strong></td>
                    <td>{score.toFixed(6)}</td>
                  </tr>
                ))}
            </tbody>
          </table>

          {visualizationUrl && (
            <div className="visualization">
              <h3>Graph Visualization</h3>
              <img src={visualizationUrl} alt="PageRank Graph" />
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App; 
