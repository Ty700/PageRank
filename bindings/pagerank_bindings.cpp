#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "graph.h"

namespace py = pybind11;

PYBIND11_MODULE(pagerank_cpp, m){
    m.doc() = "C++ implementation of PageRank algorithm";
    
    py::class_<Graph>(m, "Graph")
        .def(py::init<>())
        .def("add_node", &Graph::add_node, "Add a node to the graph",
             py::arg("label"))
        .def("add_edge", &Graph::add_edge, "Add an edge to the graph",
             py::arg("src"), py::arg("dest"))
        .def("num_nodes", &Graph::get_num_nodes, "Get the number of nodes in the graph")
        .def("compute_pagerank", &Graph::compute_pagerank, "Compute PageRank scores");
}
