# PageRank Algorithm Implementation

A complete implementation of Google's PageRank algorithm in C++ with Python visualization capabilities and web-based graph analysis interface.

## 🎯 Project Goals

### Educational Objectives
- **Understand Markov Chains**: Implement the mathematical foundation behind PageRank using transition matrices and random walks
- **Master Algorithm Design**: Compare iterative (power iteration) vs. direct (linear algebra) approaches
- **Learn Full-Stack Development**: Build a complete pipeline from C++ core to web interface
- **Explore Computer Vision**: Parse hand-drawn graphs from images using CV techniques (future enhancement)

### Technical Objectives
- High-performance C++ implementation for PageRank computation
- Python bindings (pybind11) for flexibility and visualization
- Self-hosted web application for interactive graph analysis
- Network visualization with node importance representation
- Performance benchmarking between different algorithmic approaches

## 🏗️ Architecture
```
┌─────────────────────────────────────────┐
│  C++ Core (Phase 1) ✓ COMPLETE          │
│  - Graph representation (adjacency)      │
│  - Transition matrix builder            │
│  - Power iteration algorithm            │
│  - Convergence detection & tracking      │
└──────────────┬──────────────────────────┘
               │ pybind11
               ▼
┌─────────────────────────────────────────┐
│  Python Layer (Phase 2) ✓ COMPLETE      │
│  - C++ bindings (pybind11)               │
│  - NetworkX graph visualization          │
│  - Matplotlib rendering                  │
│  - Node sizing by PageRank               │
│  - Distributed arrow endpoints           │
│  - Self-loop visualization               │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Web Application (Phase 3) 📋 PLANNED   │
│  - Flask backend API                     │
│  - React frontend                        │
│  - Interactive graph builder             │
│  - Real-time PageRank computation        │
│  - Graph visualization (D3.js)           │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Homelab Deployment (Phase 4) 📋 PLANNED│
│  - Docker containerization               │
│  - Self-hosted on Proxmox                │
│  - Domain: pagerank.ty700.tech           │
│  - Cloudflare Tunnel + Nginx Proxy       │
└─────────────────────────────────────────┘
```

## 🧮 Algorithm Overview

### The PageRank Formula

**Power Iteration Method:**
```
R_{k+1} = M × R_k

where M = α·P + (1-α)·E
```

**Components:**
- **P**: Transition matrix (column-stochastic, derived from graph structure)
- **E**: Teleportation matrix (all entries = 1/n for n nodes)
- **α**: Damping factor (0.75 - probability of following links)
- **(1-α)**: Teleportation probability (0.25 - probability of random jump)
- **R**: PageRank vector (importance scores for each node)

**Convergence:**
- Iterate until `||R_{k+1} - R_k|| < ε` (typically ε = 1e-6)
- Usually converges in 20-100 iterations
- Convergence history tracked for visualization

### Key Concepts

**Markov Chain Random Walk:**
PageRank models a "random surfer" who:
1. Starts at a random webpage
2. With probability α (0.75): clicks a random outgoing link
3. With probability (1-α) (0.25): jumps to any random page (teleportation)
4. Repeats indefinitely

The stationary distribution of this Markov chain gives the PageRank values.

**Dangling Nodes:**
Nodes with no outgoing edges are handled by treating them as linking to all nodes equally (uniform teleportation).

## 🚀 Current Features

### Phase 1: C++ Core ✓ COMPLETE
- ✅ Graph construction with string-labeled nodes
- ✅ Adjacency matrix representation
- ✅ Automatic dangling node handling
- ✅ Column-stochastic transition matrix
- ✅ Google matrix computation (with teleportation)
- ✅ Power iteration with configurable parameters
- ✅ Convergence detection and tracking
- ✅ Pretty-printed debug output for all matrices
- ✅ Configurable damping factor (α) and convergence threshold (ε)

### Phase 2: Python Integration & Visualization ✓ COMPLETE
- ✅ pybind11 bindings for C++ Graph class
- ✅ Python API for graph construction and PageRank computation
- ✅ PageRankResult struct with scores, convergence history, and iteration count
- ✅ JSON-based graph configuration
- ✅ NetworkX-based graph visualization
- ✅ Node sizing proportional to PageRank ("pixel pie" approach)
- ✅ Distinct colors per node (tab10/tab20 colormap)
- ✅ Arrows colored by source node
- ✅ Distributed arrow endpoints (handles many edges gracefully)
- ✅ Self-loop visualization
- ✅ Legend showing exact PageRank values
- ✅ High-resolution PNG export (300 DPI)
- ✅ Multiple layout algorithms (spring, kamada_kawai, circular)

## 📦 Installation & Setup

### Prerequisites

**System Dependencies:**
```bash
# Ubuntu/Debian
sudo apt install build-essential cmake python3 python3-pip python3-dev

# macOS
brew install cmake python3
```

**Python Dependencies:**
```bash
# Required for C++/Python bindings
pip install pybind11

# Required for visualization
pip install matplotlib networkx numpy
```

### Building the Project

**Step 1: Clone the repository**
```bash
git clone git@github.com:Ty700/PageRank.git
cd PageRank
```

**Step 2: Compile C++ core and Python bindings**
```bash
# Production build (optimized)
python3 build.py

# Debug build (with verbose C++ output)
python3 build.py -d

# Clean all build artifacts
python3 build.py -c
```

The build script compiles:
- C++ PageRank library
- Python extension module (pybind11)
- Standalone C++ test executable (optional)

**Step 3: Verify installation**
```bash
# Check that Python module was built
ls python/pagerank/*.so

# Should see: pagerank_cpp.cpython-3XX-x86_64-linux-gnu.so
```

### Project Structure
```
PageRank/
├── lib/
│   ├── graph.h              # Graph class interface
│   └── CMakeLists.txt
├── src/
│   ├── graph.cpp            # Graph implementation
│   ├── pagerank.cpp         # C++ test executable
│   └── CMakeLists.txt
├── bindings/
│   ├── pagerank_bindings.cpp  # pybind11 module
│   └── CMakeLists.txt
├── python/
│   ├── graph_config.json    # User graph configuration
│   ├── pagerank_app.py      # Main application script
│   ├── pagerank/            # Compiled module (.so)
│   └── output/              # Generated visualizations
├── bin/
│   ├── debug/               # Debug binaries
│   └── release/             # Release binaries
├── build.py                 # C++ build automation
├── CMakeLists.txt           # Root CMake config
└── README.md
```

## 💻 Usage

### Quick Start

**1. Configure your graph** in `python/graph_config.json`:
```json
{
  "nodes": ["A", "B", "C", "D"],
  "edges": [
    ["A", "B"],
    ["A", "C"],
    ["B", "C"],
    ["C", "D"],
    ["D", "A"]
  ],
  "parameters": {
    "visualize": true,
    "output_path": "output/pagerank_network.png",
    "pixel_budget": 50000,
    "min_node_size": 500,
    "layout": "spring"
  }
}
```

**2. Run the PageRank application:**
```bash
# Compute PageRank and generate visualization
python3 python/pagerank_app.py --visualize

# Use custom config file
python3 python/pagerank_app.py --config my_graph.json --visualize

# Compute only (no visualization)
python3 python/pagerank_app.py

# Suppress console output
python3 python/pagerank_app.py --visualize --no-print
```

**3. View results:**
- Console output shows PageRank scores and iterations
- Visualization saved to `python/output/pagerank_network.png`

### Configuration Options

**Graph Definition:**
- `nodes`: Array of node labels (strings)
- `edges`: Array of `[source, destination]` pairs

**Visualization Parameters:**
- `visualize`: Enable/disable visualization (boolean)
- `output_path`: Where to save PNG (relative to python/)
- `pixel_budget`: Total pixels for node sizing (default: 50000)
- `min_node_size`: Minimum node size in pixels (default: 500)
- `layout`: Layout algorithm - `"spring"`, `"kamada_kawai"`, or `"circular"`
- `show_plot`: Display interactive plot window (boolean, default: false)

### Python API Usage
```python
import sys
sys.path.insert(0, 'python/pagerank')
import pagerank_cpp

# Create graph
g = pagerank_cpp.Graph()

# Add nodes
g.add_node("A")
g.add_node("B")
g.add_node("C")

# Add edges (directed)
g.add_edge("A", "B")  # A → B
g.add_edge("B", "C")  # B → C
g.add_edge("C", "A")  # C → A

# Compute PageRank
result = g.compute_pagerank()

# Access results
print(f"PageRank scores: {result.pagerank_scores}")
print(f"Converged in {result.num_iterations} iterations")
print(f"Convergence history: {result.convergence_history}")

# Get graph structure
nodes = g.get_nodes()        # ['A', 'B', 'C']
edges = g.get_edges()        # [('A', 'B'), ('B', 'C'), ('C', 'A')]
num_nodes = g.num_nodes()    # 3
```

### C++ Direct Usage
```cpp
#include "graph.h"

int main() {
    Graph g;
    
    // Build graph
    g.add_node("A");
    g.add_node("B");
    g.add_node("C");
    
    g.add_edge("A", "B");
    g.add_edge("B", "C");
    g.add_edge("C", "A");
    
    // Compute PageRank
    PageRankResult result = g.compute_pagerank();
    
    // Access results
    std::vector<double> ranks = result.pagerank_vector;
    std::vector<double> history = result.convergence_history;
    size_t iterations = result.iterations;
    
    return 0;
}
```

### Visualization Features

**Node Representation:**
- Size proportional to PageRank score ("pixel pie" approach)
- Distinct color per node (automatically assigned)
- Labels centered on nodes

**Edge Representation:**
- Arrows colored by source node
- Distributed endpoints (handles high-degree nodes gracefully)
- Self-loops displayed as arcs above nodes
- Slight curve to avoid overlap

**Layout Algorithms:**
- `spring`: Force-directed layout (default, good for most graphs)
- `kamada_kawai`: Energy-minimization layout (better for symmetric graphs)
- `circular`: Nodes arranged in a circle (good for visualizing connectivity)

**Example Output:**
```
Loading configuration from: python/graph_config.json
Building graph...
  Nodes: 6
  Edges: 12
Computing PageRank...

==================================================
PageRank Results:
==================================================
  A: 0.114242
  B: 0.135749
  C: 0.169634
  D: 0.199202
  E: 0.148066
  F: 0.233107
==================================================
Converged in 15 iterations
==================================================

Generating visualization...
Visualization saved to: python/output/pagerank_network.png
Done!
```

## 📊 Algorithm Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `ALPHA` | 0.75 | Damping factor (probability of following links) |
| `MAX_ITER` | 100 | Maximum iterations before forced termination |
| `EPSILON` | 1e-6 | Convergence threshold for \|\|R_{k+1} - R_k\|\| |

**Modify in `lib/graph.h`:**
```cpp
const double ALPHA = 0.75;      // Try 0.85 for Google's original value
const double EPSILON = 1e-6;    // Tighten to 1e-8 for more precision
```

After modifying, rebuild:
```bash
python3 build.py -c  # Clean
python3 build.py     # Rebuild
```

## 🔮 Roadmap

### Phase 3: Web Application (Next)
- [ ] Flask REST API backend
  - [ ] POST /api/graph - Create graph from JSON
  - [ ] GET /api/pagerank - Compute and return results
  - [ ] POST /api/visualize - Generate visualization
- [ ] React frontend
  - [ ] Interactive graph builder (drag-and-drop nodes/edges)
  - [ ] Real-time PageRank computation
  - [ ] D3.js network visualization
  - [ ] Parameter tuning interface (α, ε)
  - [ ] Convergence plot animation
- [ ] Export capabilities
  - [ ] JSON results download
  - [ ] PNG visualization export
  - [ ] CSV data export

### Phase 4: Homelab Deployment
- [ ] Docker containerization
  - [ ] Multi-stage Dockerfile (C++ build + Python runtime)
  - [ ] Docker Compose for frontend + backend
- [ ] Self-hosted deployment
  - [ ] Proxmox LXC container 100 (existing Docker services)
  - [ ] Domain: pagerank.ty700.tech
  - [ ] Cloudflare Tunnel for external access
  - [ ] Nginx Proxy Manager reverse proxy
- [ ] Production optimizations
  - [ ] Environment-based configuration
  - [ ] Logging and monitoring
  - [ ] Rate limiting

### Future Enhancements
- [ ] Computer Vision pipeline
  - [ ] PNG/image upload support
  - [ ] Circle detection for nodes (OpenCV HoughCircles)
  - [ ] Line detection for edges (Hough line transform)
  - [ ] Arrow direction detection
  - [ ] OCR for node label extraction (Tesseract)
- [ ] Alternative PageRank solvers
  - [ ] Direct solution via Gaussian elimination
  - [ ] Eigenvalue decomposition approach
  - [ ] Performance benchmarking vs. power iteration
- [ ] Graph datasets
  - [ ] SNAP dataset integration
  - [ ] Wikipedia link graph analysis
  - [ ] Social network examples

## 🎓 Learning Outcomes

This project demonstrates:
- **Algorithms & Data Structures**: Graph representations, matrix operations, iterative methods
- **Linear Algebra**: Markov chains, stochastic matrices, eigenvectors, stationary distributions
- **Systems Programming**: C++ performance optimization, memory management
- **Language Interoperability**: C++/Python integration via pybind11
- **Software Engineering**: Clean architecture, separation of concerns, build systems (CMake)
- **Data Visualization**: NetworkX, matplotlib, color mapping, distributed layouts
- **Full-Stack Development**: Backend APIs, frontend frameworks, deployment (upcoming)
- **DevOps**: Docker, self-hosting, reverse proxies (upcoming)

## 📚 References

- [The PageRank Citation Ranking: Bringing Order to the Web](http://ilpubs.stanford.edu:8090/422/) - Original PageRank paper by Larry Page et al.
- [Stanford CS246: Mining Massive Datasets](http://web.stanford.edu/class/cs246/) - Course materials on graph algorithms
- [Wikipedia: PageRank](https://en.wikipedia.org/wiki/PageRank) - Comprehensive overview
- [pybind11 Documentation](https://pybind11.readthedocs.io/) - C++/Python binding library
- [NetworkX Documentation](https://networkx.org/) - Python graph analysis library
- [SNAP: Stanford Network Analysis Platform](https://snap.stanford.edu/) - Graph datasets for testing

## 📝 License

MIT License - feel free to use for educational purposes

## 👤 Author

**Tyler** - Verification Engineer @ AMD | MS Computer Science Student @ Texas A&M University

*Built as a portfolio project demonstrating algorithms, systems programming, and full-stack development skills.*

---

**Current Status:** Phase 2 Complete ✓ | Phase 3 Starting 🚀

**Next Milestone:** Flask API + React frontend

**Project Timeline:**
- Phase 1 (C++ Core): ✓ Complete
- Phase 2 (Python + Viz): ✓ Complete  
- Phase 3 (Web App): ~2-3 weekends
- Phase 4 (Deployment): ~1 weekend

**Live Demo:** Coming soon at pagerank.ty700.tech
