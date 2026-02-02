#!/usr/bin/env python3
import sys
import os

# Get absolute path
script_dir = os.path.dirname(os.path.abspath(__file__))
python_dir = os.path.dirname(script_dir)
pagerank_dir = os.path.join(python_dir, 'pagerank')

print(f"Script location: {script_dir}")
print(f"Adding to sys.path: {pagerank_dir}")
print(f"Directory exists: {os.path.exists(pagerank_dir)}")

sys.path.insert(0, pagerank_dir)

# List files in the directory
print(f"\nFiles in {pagerank_dir}:")
for f in os.listdir(pagerank_dir):
    print(f"  - {f}")

print("\nAttempting import...")
try:
    import pagerank_cpp
    print("✓ Import successful!")
    print(f"Module location: {pagerank_cpp.__file__}")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test it
g = pagerank_cpp.Graph()
g.add_node("A")
g.add_node("B")
g.add_edge("A", "B")
print(f"\n✓ Graph created with {g.get_num_nodes()} nodes")
