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
│  - Color-coded importance gradient       │
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
- ✅ NetworkX-based graph visualization
- ✅ Node sizing proportional to PageRank ("pixel pie" approach)
- ✅ Color gradient mapping (Blues colormap)
- ✅ Directed edges with arrows
- ✅ Legend showing exact PageRank values
- ✅ High-resolution PNG export (300 DPI)

## 📦 Building the Project

### Prerequisites
```bash
# C++ compiler with C++17 support
sudo apt install build-essential cmake

# Python 3.8+ with development headers
sudo apt install python3 python3-pip python3-dev

# pybind11 for C++/Python bindings
pip install pybind11

# Visualization libraries
pip install matplotlib networkx
# Or: sudo apt install python3-matplotlib python3-networkx
```

### Build Instructions
```bash
# Clone repository
git clone git@github.com:Ty700/PageRank.git
cd PageRank

# Debug build (with verbose C++ output)
python3 build.py -d

# Production build (optimized)
python3 build.py

# Clean build artifacts
python3 build.py -c
```

### Project Structure
```
pagerank-project/
├── lib/
│   ├── graph.h          # Graph class interface
│   └── CMakeLists.txt
├── src/
│   ├── graph.cpp        # Graph implementation
│   ├── pagerank.cpp     # C++ test executable
│   └── CMakeLists.txt
├── bindings/
│   ├── pagerank_bindings.cpp  # pybind11 module definition
│   └── CMakeLists.txt
├── python/
│   ├── pagerank/        # Compiled .so module location
│   ├── examples/        # Python scripts
│   │   ├── test_binding.py    # Visualization script
│   └── output/          # Generated PNG files
├── bin/
│   ├── debug/           # Debug binaries
│   └── release/         # Release binaries
├── build.py             # Build automation script
├── CMakeLists.txt       # Root CMake config
└── README.md
```

## 💻 Usage Examples

### C++ Usage
```cpp
#include "graph.h"

int main() {
    Graph g;
    
    // Build graph
    g.add_node("A");
    g.add_node("B");
    g.add_node("C");
    
    g.add_edge("A", "B");  // A → B
    g.add_edge("A", "C");  // A → C
    g.add_edge("C", "A");  // C → A (creates cycle)
    
    // Compute PageRank
    auto result = g.compute_pagerank();
    
    // Access results
    std::vector<double> ranks = result.pagerank_vector;
    std::vector<double> history = result.convergence_history;
    size_t iterations = result.iterations;
    
    return 0;
}
```

### Python Usage
```python
import sys
sys.path.insert(0, 'python/pagerank')
import pagerank_cpp

# Build graph
g = pagerank_cpp.Graph()
g.add_node("A")
g.add_node("B")
g.add_node("C")
g.add_edge("A", "B")
g.add_edge("A", "C")
g.add_edge("C", "A")

# Compute PageRank
result = g.compute_pagerank()

# Access results
print(f"PageRank scores: {result.pagerank_scores}")
print(f"Converged in {result.num_iterations} iterations")
print(f"Convergence history: {result.convergence_history}")

# Get graph structure
nodes = g.get_nodes()
edges = g.get_edges()
```

### Visualization
```bash
cd python/examples
python3 test_binding.py
# Outputs: ../output/pagerank_network.png
```

**Visualization Features:**
- Node sizes proportional to PageRank (total pixel budget approach)
- Color gradient from light to dark blue (importance)
- Directed arrows showing edge direction
- Legend with exact PageRank values
- Spring layout algorithm for automatic positioning

**Debug Output:**
```
=== Transition Matrix (Column-Stochastic) ===
         A         B         C
 A [  0.0000,  0.0000,  1.0000 ]
 B [  0.5000,  0.0000,  0.0000 ]
 C [  0.5000,  0.0000,  0.0000 ]

=== Google Matrix (Column-Stochastic) ===
         A         B         C
 A [  0.0833,  0.0833,  0.8333 ]
 B [  0.4583,  0.0833,  0.0833 ]
 C [  0.4583,  0.0833,  0.0833 ]

Converged after 23 iterations.

=== Final PageRank Vector ===
A [ 0.387097 ]
B [ 0.306452 ]
C [ 0.306452 ]
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
- **Data Visualization**: NetworkX, matplotlib, gradient mapping, proportional scaling
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
