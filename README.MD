# PageRank Algorithm Implementation

A complete implementation of Google's PageRank algorithm in C++ with Python visualization capabilities and web-based graph analysis interface.

## 🎯 Project Goals

### Educational Objectives
- **Understand Markov Chains**: Implement the mathematical foundation behind PageRank using transition matrices and random walks
- **Master Algorithm Design**: Compare iterative (power iteration) vs. direct (linear algebra) approaches
- **Learn Full-Stack Development**: Build a complete pipeline from C++ core to web interface
- **Explore Computer Vision**: Parse hand-drawn graphs from images using CV techniques

### Technical Objectives
- High-performance C++ implementation for PageRank computation
- Python bindings (pybind11) for flexibility and visualization
- Computer vision pipeline for parsing graph images (PNG/MS Paint)
- Self-hosted web application for interactive graph analysis
- Performance benchmarking between different algorithmic approaches

## 🏗️ Architecture
```
┌─────────────────────────────────────────┐
│  C++ Core (Phase 1) ✓ COMPLETE          │
│  - Graph representation (adjacency)      │
│  - Transition matrix builder            │
│  - Power iteration algorithm            │
│  - Convergence detection                 │
└──────────────┬──────────────────────────┘
               │ pybind11
               ▼
┌─────────────────────────────────────────┐
│  Python Layer (Phase 2) 🚧 IN PROGRESS  │
│  - C++ bindings                          │
│  - Matplotlib visualizations             │
│  - Convergence plotting                  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Computer Vision (Phase 3) 📋 PLANNED   │
│  - PNG/image parsing (OpenCV)            │
│  - Node detection (HoughCircles)         │
│  - Edge detection (HoughLines)           │
│  - Arrow direction detection             │
│  - OCR for node labels (Tesseract)       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Web Application (Phase 4) 📋 PLANNED   │
│  - Flask backend API                     │
│  - React frontend                        │
│  - Graph visualization (D3.js)           │
│  - Self-hosted on homelab                │
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

## 🚀 Current Features (Phase 1)

- ✅ Graph construction with string-labeled nodes
- ✅ Adjacency matrix representation
- ✅ Automatic dangling node handling
- ✅ Column-stochastic transition matrix
- ✅ Google matrix computation (with teleportation)
- ✅ Power iteration with configurable parameters
- ✅ Convergence detection and reporting
- ✅ Pretty-printed debug output for all matrices
- ✅ Configurable damping factor (α) and convergence threshold (ε)

## 📦 Building the Project

### Prerequisites
```bash
# C++ compiler with C++17 support
sudo apt install build-essential cmake

# Python 3.8+ (for future phases)
sudo apt install python3 python3-pip
```

### Build Instructions
```bash
# Clone repository
git clone git@github.com:Ty700/PageRank.git
cd PageRank

# Debug build (with verbose output)
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
│   ├── pagerank.cpp     # Main entry point
│   └── CMakeLists.txt
├── bin/
│   ├── debug/           # Debug binaries
│   └── release/         # Release binaries
├── build.py             # Build automation script
├── CMakeLists.txt       # Root CMake config
└── README.md
```

## 💻 Usage Example
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
    auto ranks = g.compute_pagerank();
    
    // ranks[0] = PageRank of node A
    // ranks[1] = PageRank of node B
    // ranks[2] = PageRank of node C
    
    return 0;
}
```

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

Iteration 1: diff = 0.666667
Iteration 2: diff = 0.416667
...
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
| `EPSILON` | 1e-6 | Convergence threshold for ||R_{k+1} - R_k|| |

**Modify in `lib/graph.h`:**
```cpp
const double ALPHA = 0.75;      // Try 0.85 for Google's original value
const double EPSILON = 1e-6;    // Tighten to 1e-8 for more precision
```

## 🔮 Planned Features

### Phase 2: Python Integration (In Progress)
- [ ] pybind11 bindings for C++ Graph class
- [ ] Python API for graph construction and PageRank computation
- [ ] Matplotlib visualization of convergence history
- [ ] Network graph visualization with node sizes based on PageRank

### Phase 3: Computer Vision Pipeline
- [ ] PNG/image upload support
- [ ] Circle detection for nodes (OpenCV HoughCircles)
- [ ] Line detection for edges (Hough line transform)
- [ ] Arrow direction detection
- [ ] OCR for node label extraction (Tesseract)
- [ ] Automatic adjacency matrix generation from images

### Phase 4: Linear Algebra Solver
- [ ] Direct solution via Gaussian elimination
- [ ] Eigenvalue decomposition approach
- [ ] Performance benchmarking vs. power iteration
- [ ] Trade-off analysis (time complexity, accuracy, memory)

### Phase 5: Web Application
- [ ] Flask REST API backend
- [ ] React frontend with drag-and-drop PNG upload
- [ ] Real-time graph visualization (D3.js/vis.js)
- [ ] Interactive PageRank parameter tuning
- [ ] Convergence animation
- [ ] Export results (JSON, CSV, PDF reports)
- [ ] Docker containerization
- [ ] Self-hosted deployment on homelab (192.168.86.241)

## 🎓 Learning Outcomes

This project demonstrates:
- **Algorithms & Data Structures**: Graph representations, matrix operations, iterative methods
- **Linear Algebra**: Markov chains, stochastic matrices, eigenvectors, stationary distributions
- **Systems Programming**: C++ performance optimization, memory management
- **Software Engineering**: Clean architecture, separation of concerns, build systems
- **Full-Stack Development**: C++/Python integration, web APIs, frontend frameworks
- **Computer Vision**: Image processing, feature detection, OCR
- **DevOps**: Docker, self-hosting, CI/CD (future)

## 📚 References

- [The PageRank Citation Ranking: Bringing Order to the Web](http://ilpubs.stanford.edu:8090/422/) - Original PageRank paper by Larry Page et al.
- [Stanford CS246: Mining Massive Datasets](http://web.stanford.edu/class/cs246/) - Course materials on graph algorithms
- [Wikipedia: PageRank](https://en.wikipedia.org/wiki/PageRank) - Comprehensive overview
- [SNAP: Stanford Network Analysis Platform](https://snap.stanford.edu/) - Graph datasets for testing

## 🏠 Self-Hosting Details

**Target Infrastructure:**
- **Hardware**: Proxmox homelab @ 192.168.86.241
- **Container**: LXC container 100 (existing Docker services)
- **Domain**: pagerank.ty700.tech
- **External Access**: Cloudflare Tunnel + Nginx Proxy Manager
- **Stack**: Docker Compose (backend + frontend + nginx)

## 📝 License

MIT License - feel free to use for educational purposes

## 👤 Author

**Tyler** - Verification Engineer @ AMD | MS Computer Science Student @ Texas A&M University

*Built as a portfolio project demonstrating algorithms, systems programming, and full-stack development skills.*

---

**Current Status:** Phase 1 Complete ✓ | Phase 2 In Progress 🚧

**Next Milestone:** pybind11 bindings + Python visualization

**Estimated Completion:** Phase 2 (1 weekend) | Full Project (4-5 weekends)
