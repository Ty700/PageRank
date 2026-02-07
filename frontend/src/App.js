import React, { useState } from 'react';
import * as api from './api/pagerank';

function App() {
    const [nodes, setNodes] = useState([]);
    const [edges, setEdges] = useState([]);
    const [nodeInput, setNodeInput] = useState('');
    const [edgeFrom, setEdgeFrom] = useState('');
    const [edgeTo, setEdgeTo] = useState(''); 
    
    // New state for PageRank results
    const [pageRankScores, setPageRankScores] = useState(null);
    const [iterations, setIterations] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [visualizationUrl, setVisualizationUrl] = useState(null);

    const addNode = () => {
        if (nodeInput && !nodes.includes(nodeInput)) {
            setNodes([...nodes, nodeInput]);
            setNodeInput('');
        }
    };

    const addEdge = () => {
        if (edgeFrom && edgeTo && nodes.includes(edgeFrom) && nodes.includes(edgeTo)) {
            setEdges([...edges, [edgeFrom, edgeTo]]);
            setEdgeFrom('');
            setEdgeTo('');
        }
    };

    const handleComputePageRank = async () => {
        if (nodes.length === 0) {
            setError('Please add at least one node');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            // Step 1: Create graph on backend
            await api.createGraph(nodes, edges);
            
            // Step 2: Compute PageRank
            const result = await api.computePageRank();
            setPageRankScores(result.scores);
            setIterations(result.iterations);
            
            // Step 3: Get visualization
            const imageBlob = await api.getVisualization();
            const imageUrl = URL.createObjectURL(imageBlob);
            setVisualizationUrl(imageUrl);
            
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleClearGraph = async () => {
        setNodes([]);
        setEdges([]);
        setPageRankScores(null);
        setIterations(null);
        setVisualizationUrl(null);
        setError(null);
        
        // Clear on backend too
        try {
            await api.clearGraph();
        } catch (err) {
            console.error('Failed to clear backend:', err);
        }
    };

    return (
        <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
            <h1>PageRank Calculator</h1>

            {/* Error Display */}
            {error && (
                <div style={{ 
                    padding: '10px', 
                    backgroundColor: '#ffebee', 
                    color: '#c62828',
                    marginBottom: '20px',
                    borderRadius: '4px'
                }}>
                    Error: {error}
                </div>
            )}

            {/* Add Nodes Section */}
            <div style={{ marginBottom: '20px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
                <h2>Add Nodes</h2>
                <input
                    type="text"
                    value={nodeInput}
                    onChange={(e) => setNodeInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && addNode()}
                    placeholder="Node name (e.g., A)"
                    style={{ padding: '8px', marginRight: '10px' }}
                />
                <button onClick={addNode} style={{ padding: '8px 16px' }}>
                    Add Node
                </button>
                
                <div style={{ marginTop: '10px' }}>
                    <strong>Nodes:</strong> {nodes.join(', ') || 'None'}
                </div>
            </div>

            {/* Add Edges Section */}
            <div style={{ marginBottom: '20px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
                <h2>Add Edges</h2>
                <input
                    type="text"
                    value={edgeFrom}
                    onChange={(e) => setEdgeFrom(e.target.value)}
                    placeholder="From node"
                    style={{ padding: '8px', marginRight: '10px' }}
                />
                <span>→</span>
                <input
                    type="text"
                    value={edgeTo}
                    onChange={(e) => setEdgeTo(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && addEdge()}
                    placeholder="To node"
                    style={{ padding: '8px', margin: '0 10px' }}
                />
                <button onClick={addEdge} style={{ padding: '8px 16px' }}>
                    Add Edge
                </button>
                
                <div style={{ marginTop: '10px' }}>
                    <strong>Edges:</strong> 
                    {edges.length > 0 
                        ? edges.map((e, i) => <span key={i}> {e[0]}→{e[1]}</span>)
                        : ' None'}
                </div>
            </div>

            {/* Action Buttons */}
            <div style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
                <button 
                    onClick={handleComputePageRank}
                    disabled={loading || nodes.length === 0}
                    style={{ 
                        padding: '12px 24px',
                        backgroundColor: loading ? '#ccc' : '#4CAF50',
                        color: '#fff',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: loading ? 'not-allowed' : 'pointer',
                        fontSize: '16px',
                        fontWeight: 'bold'
                    }}
                >
                    {loading ? 'Computing...' : 'Compute PageRank'}
                </button>

                <button 
                    onClick={handleClearGraph}
                    style={{ 
                        padding: '12px 24px',
                        backgroundColor: '#f44336',
                        color: '#fff',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontSize: '16px'
                    }}
                >
                    Clear Graph
                </button>
            </div>

            {/* Results Section */}
            {pageRankScores && (
                <div style={{ marginTop: '30px' }}>
                    <h2>PageRank Results</h2>
                    
                    {/* Scores Table */}
                    <div style={{ 
                        padding: '20px', 
                        border: '1px solid #ccc', 
                        borderRadius: '8px',
                        marginBottom: '20px'
                    }}>
                        <h3>Scores (Converged in {iterations} iterations)</h3>
                        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                            <thead>
                                <tr style={{ backgroundColor: '#f5f5f5' }}>
                                    <th style={{ padding: '10px', textAlign: 'left', borderBottom: '2px solid #ddd' }}>Node</th>
                                    <th style={{ padding: '10px', textAlign: 'right', borderBottom: '2px solid #ddd' }}>PageRank Score</th>
                                </tr>
                            </thead>
                            <tbody>
                                {Object.entries(pageRankScores)
                                    .sort((a, b) => b[1] - a[1]) // Sort by score descending
                                    .map(([node, score]) => (
                                        <tr key={node}>
                                            <td style={{ padding: '10px', borderBottom: '1px solid #eee' }}>{node}</td>
                                            <td style={{ padding: '10px', textAlign: 'right', borderBottom: '1px solid #eee' }}>
                                                {score.toFixed(6)}
                                            </td>
                                        </tr>
                                    ))
                                }
                            </tbody>
                        </table>
                    </div>

                    {/* Visualization */}
                    {visualizationUrl && (
                        <div style={{ 
                            padding: '20px', 
                            border: '1px solid #ccc', 
                            borderRadius: '8px'
                        }}>
                            <h3>Graph Visualization</h3>
                            <img 
                                src={visualizationUrl} 
                                alt="PageRank Visualization" 
                                style={{ maxWidth: '100%', height: 'auto' }}
                            />
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default App;
