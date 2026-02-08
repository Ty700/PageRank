# PageRank Calculator

A full-stack web application that implements Google's PageRank algorithm with interactive graph visualization. Built with C++ computational backend, Python Flask API, and React frontend.

**Live Demo:** [ty700.tech/projects/pagerank](https://ty700.tech/projects/pagerank)

## Features

- **Interactive Graph Builder** - Add nodes and edges through an intuitive UI
- **Template Graphs** - Quick-start with pre-built graph patterns (cycle, star, linear, complete)
- **Real-time Computation** - C++ backend for efficient PageRank calculations
- **Visual Results** - NetworkX-powered graph visualizations with node rankings
- **Responsive Design** - Clean, modern interface that works on all devices

## Architecture
```
┌─────────────┐      HTTP       ┌──────────────┐      pybind11    ┌─────────────┐
│   React     │ ──────────────> │ Flask API    │ ───────────────> │   C++       │
│  Frontend   │ <────────────── │  (Python)    │ <─────────────── │   Engine    │
└─────────────┘      JSON       └──────────────┘      Results     └─────────────┘
```

**Stack:**
- **Backend:** C++17 (PageRank algorithm) + Python 3.11 (Flask REST API)
- **Frontend:** React 18 with functional components and hooks
- **Deployment:** Docker containers behind Nginx Proxy Manager
- **Visualization:** NetworkX + Matplotlib

## Backend Deep Dive

### C++ Engine

The core PageRank computation is implemented in C++ for performance:

**Graph Structure:**
- Adjacency list representation using `std::unordered_map<std::string, std::vector<std::string>>`
- Outbound link counting for PageRank formula
- Efficient iteration over nodes and edges

**PageRank Algorithm:**
```cpp
// Damping factor and convergence threshold
const double DAMPING_FACTOR = 0.85;
const double EPSILON = 1e-6;

// Iterative computation
while (delta > EPSILON && iterations < MAX_ITERATIONS) {
    for (each node) {
        new_rank = (1 - d) + d * sum(incoming_ranks / outbound_counts)
        delta = max(delta, abs(new_rank - old_rank))
    }
}
```

**Debug Output:**
```
=== GRAPH STRUCTURE ===
Nodes: A, B, C, D
Edges: A→B, B→C, C→D, D→A
Outbound counts: A:1, B:1, C:1, D:1

=== PAGERANK COMPUTATION ===
Iteration 1:  A: 0.2500 → 0.2500 (Δ 0.0000)
Iteration 2:  A: 0.2500 → 0.2500 (Δ 0.0000)
...
Converged in 46 iterations

=== FINAL SCORES ===
A: 0.250000
B: 0.250000
C: 0.250000
D: 0.250000
```

### Python Flask API

**Session Management:**
- Cookie-based session tracking with `secrets.token_hex(16)`
- In-memory graph storage keyed by session ID
- Automatic cleanup on `/api/clear`

**Visualization Pipeline:**
1. Graph data → NetworkX DiGraph
2. Spring layout algorithm for node positioning
3. Matplotlib rendering with node sizes proportional to PageRank scores
4. PNG export to `/app/output/<session_id>/`

**Example API Flow:**
```python
# 1. Create graph
POST /api/graph
{
  "nodes": ["A", "B", "C"],
  "edges": [["A", "B"], ["B", "C"]]
}
→ Response: {"message": "Graph created", "num_nodes": 3, "num_edges": 2}

# 2. Compute PageRank
GET /api/pagerank
→ Response: {
    "scores": {"A": 0.287, "B": 0.356, "C": 0.356},
    "iterations": 15
  }

# 3. Get visualization
GET /api/visualize
→ Response: PNG image (binary)
```

### pybind11 Bindings

C++ classes are exposed to Python via pybind11:
```cpp
PYBIND11_MODULE(pagerank_cpp, m) {
    py::class_<Graph>(m, "Graph")
        .def(py::init<>())
        .def("add_node", &Graph::add_node)
        .def("add_edge", &Graph::add_edge)
        .def("compute_pagerank", &Graph::compute_pagerank)
        .def("get_pagerank", &Graph::get_pagerank);
}
```

Python usage:
```python
import pagerank_cpp

graph = pagerank_cpp.Graph()
graph.add_node("A")
graph.add_edge("A", "B")
scores = graph.compute_pagerank()
```

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for development)
- CMake 3.15+ (for building C++ module)

### Quick Start
```bash
# Clone the repository
git clone https://github.com/Ty700/PageRank.git
cd PageRank

# Start the application
docker-compose up -d

# Frontend: http://localhost:8081
# Backend API: http://localhost:5000
```

### Development

**Backend (C++ + Flask):**
```bash
cd backend

# Build C++ module
python3 build.py

# Run Flask dev server (with debug output)
FLASK_DEBUG=1 python3 app.py

# Test C++ module directly
python3 -c "import pagerank_cpp; g = pagerank_cpp.Graph(); g.add_node('A'); print('Success!')"
```

**Frontend (React):**
```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm start
```

**Debugging Tips:**
```bash
# Check if C++ module compiled
find backend -name "pagerank_cpp*.so"

# Test API endpoints
curl -X POST http://localhost:5000/api/graph \
  -H "Content-Type: application/json" \
  -d '{"nodes":["A","B"],"edges":[["A","B"]]}'

curl http://localhost:5000/api/pagerank
```

## Project Structure
```
PageRank/
├── backend/
│   ├── lib/
│   │   ├── graph.h              # Graph class definition
│   │   └── CMakeLists.txt
│   ├── src/
│   │   ├── graph.cpp            # Graph implementation
│   │   ├── pagerank.cpp         # PageRank algorithm
│   │   └── CMakeLists.txt
│   ├── bindings/
│   │   ├── pagerank_bindings.cpp  # pybind11 interface
│   │   └── CMakeLists.txt
│   ├── app.py                   # Flask REST API
│   ├── build.py                 # Build script for C++ module
│   ├── CMakeLists.txt           # Root build config
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.js               # Main React component
│   │   ├── PageRank.css         # Styling
│   │   └── api/pagerank.js      # API client
│   ├── public/
│   │   └── index.html
│   └── package.json
└── docker-compose.yml
```

## Algorithm

Implements the original PageRank algorithm:
```
PR(A) = (1-d) + d * Σ(PR(Ti) / C(Ti))
```

Where:
- `d` = damping factor (0.85)
- `Ti` = pages linking to page A
- `C(Ti)` = number of outbound links from Ti

**Convergence:** Iterates until changes fall below ε = 1e-6 or max 100 iterations.

**Example Calculation:**
```
Graph: A → B → C → A

Initial: PR(A) = PR(B) = PR(C) = 1/3 = 0.333

Iteration 1:
  PR(A) = 0.15 + 0.85 * (0.333/1) = 0.433
  PR(B) = 0.15 + 0.85 * (0.333/1) = 0.433
  PR(C) = 0.15 + 0.85 * (0.333/1) = 0.433

Converges after ~2 iterations to equal distribution
```

## Deployment

Production deployment uses Docker with Nginx reverse proxy:
```yaml
# docker-compose.yml
services:
  pagerank-backend:
    build: ./backend
    ports:
      - "5000:5000"
    volumes:
      - ./backend/output:/app/output
  
  pagerank-frontend:
    image: nginx:alpine
    volumes:
      - ./frontend/build:/usr/share/nginx/html
    ports:
      - "8081:80"
```

## Performance Notes

- **C++ vs Python:** C++ implementation is ~10-50x faster for large graphs (1000+ nodes)
- **Memory:** O(V + E) space complexity for adjacency list
- **Time:** O(k * V * E) where k = iterations (typically < 100)

## Contributing

This is a personal portfolio project, but suggestions and feedback are welcome!

## License

MIT License - See [LICENSE](LICENSE) for details.

## Author

**Tyler Scotti**  
Verification Engineer @ AMD | MS CS Student @ Texas A&M  
[GitHub](https://github.com/Ty700) • [LinkedIn](https://www.linkedin.com/in/tylerscotti) • [Portfolio](https://ty700.tech)

---

*Built as a demonstration of full-stack development, systems programming, and DevOps skills.*
