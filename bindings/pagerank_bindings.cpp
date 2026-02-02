#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "graph.h"

namespace py = pybind11;

PYBIND11_MODULE(pagerank_cpp, m){
    m.doc() = "C++ implementation of PageRank algorithm";
    
    /* Expose the Result struct */
    py::class_<PageRankResult>(m, "Result")
        .def_readonly("pagerank_scores", &PageRankResult::pagerank_vector, "Computed PageRank scores for each node")
        .def_readonly("convergence_history", &PageRankResult::convergence_history, "History of convergence differences per iteration")
        .def_readonly("num_iterations", &PageRankResult::iterations, "Number of iterations taken to converge");

    /* Bind the Graph class */
    py::class_<Graph>(m, "Graph")
        .def(py::init<>())
        .def("add_node", &Graph::add_node, "Add a node to the graph",
             py::arg("label"))
        .def("add_edge", &Graph::add_edge, "Add an edge to the graph",
             py::arg("src"), py::arg("dest"))
        .def("num_nodes", &Graph::get_num_nodes, "Get the number of nodes in the graph")
        .def("compute_pagerank", &Graph::compute_pagerank, "Compute PageRank scores");
}
