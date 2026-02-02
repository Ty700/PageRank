#pragma once 

#include <vector>
#include <string>
#include <map>

class Graph {
    private:
        /* Member Variables */
        std::vector<std::vector<int>> adj;          /* Adjacency Matrix */
        std::map<std::string, int> node_to_index;   /* Maps Node to Index in Adjacency Matrix */
        std::vector<std::string> index_to_node;     /* Maps Index in Adjacency Matrix to Node */
        int num_nodes = 0; 
    
        /* PageRank Parameters */
        const double ALPHA = 0.75;      /* Damping Factor for Transition Matrix */
        const double BETA = 1 - ALPHA;  /* Teleportation Factor */

        /* Convergence Parameters */
        const int MAX_ITER = 100;       /* Maximum Iterations for Convergence */
        const double EPSILON = 1e-6;    /* Convergence Threshold */
        
        /* Helper Functions */
        void compute_out_degrees(std::vector<int>& out_degrees);
        std::vector<std::vector<double>> build_transition_matrix();
        std::vector<std::vector<double>> build_teleportation_matrix();

    public:
        Graph() {};
        void add_node(const std::string& lbl);
        void add_edge(const std::string& from, const std::string& to);

        std::vector<std::vector<double>> compute_pagerank(); 
        int get_num_nodes() const { return this->num_nodes; }
};
