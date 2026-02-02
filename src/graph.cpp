#include "graph.h"
#ifdef DEBUG 
    #include <iomanip>
    #include <iostream>
#endif

void Graph::add_node(const std::string& lbl)
{
    /* Check if node already exists in the adj matrix */
    if (this->node_to_index.find(lbl) != this->node_to_index.end()) {
        /* Node already exists */
        #if DEBUG 
            std::cout << "Node " << lbl << " already exists in the graph." << std::endl;
        #endif 
        return;
    }
    
    /* Maps the node label to the next available index */ 
    /* Example: If the graph is empty and we add node "A", then node_to_index["A"] = 0 */
    node_to_index[lbl] = this->num_nodes;
    this->num_nodes += 1;

    adj.resize(this->num_nodes);
    for(int i = 0; i < this->num_nodes; i++)
        adj[i].resize(this->num_nodes, 0);
}

void Graph::add_edge(const std::string& src, const std::string& dest)
{
    /* Ensure both nodes exist in the graph */
    if(this->node_to_index.find(src) == this->node_to_index.end() ||
       this->node_to_index.find(dest) == this->node_to_index.end())
    {
        /* One or both nodes do not exist */
        /* TODO: DEBUG LOG */
        #if DEBUG 
            std::cout << "One or both nodes do not exist in the graph: " << src << ", " << dest << std::endl;
        #endif

        return;
    }

    int src_index   = this->node_to_index[src];
    int dest_index  = this->node_to_index[dest];

    /* Add the edge to the adjacency matrix */
    this->adj[src_index][dest_index] = 1;

    return;
}

void Graph::compute_out_degrees(std::vector<int>& out_degrees)
{
    for(int i = 0; i < this->num_nodes; i++)
    {
        int out_degree = 0;
        for(int j = 0; j < this->num_nodes; j++)
        {
            out_degree += this->adj[i][j];
        }
        out_degrees[i] = out_degree;
    }
}

std::vector<std::vector<double>> Graph::build_transition_matrix()
{
    /* Compute out-degrees */
    std::vector<int> out_degrees (num_nodes, 0);
    compute_out_degrees(out_degrees);
    
    /* Init transition matrix */
    std::vector<std::vector<double>> transition_matrix ;
    
    transition_matrix.resize(this->num_nodes);
    for(int i = 0; i < this->num_nodes; i++)
        transition_matrix[i].resize(this->num_nodes);

    /* Build translation matrix */
    for(int row = 0; row < this->num_nodes; row++)
    {
        for(int col = 0; col < this->num_nodes; col++)
        {
            if(out_degrees[row] == 0)
            {
                transition_matrix[col][row] = static_cast<double>(1.0/this->num_nodes);
            }
            else 
            {
                transition_matrix[col][row] = static_cast<double>(this->adj[row][col]) / static_cast<double>(out_degrees[row]);
            }
        }
    }

    #ifdef DEBUG
        // Create index-to-label mapping for printing
        std::vector<std::string> labels(num_nodes);
        for(const auto& pair : node_to_index)
        {
            labels[pair.second] = pair.first;
        }

        // Pretty print with labels
        std::cout << "\n\t=== Transition Matrix (Column-Stochastic) ===" << std::endl;
        std::cout << std::fixed << std::setprecision(4);
        
        // Print column headers
        std::cout << " ";  // Space for row labels
        for(int j = 0; j < this->num_nodes; j++)
        {
            std::cout << std::setw(10) << labels[j];
        }
        std::cout << std::endl;
        
        // Print matrix with row labels
        for(int i = 0; i < this->num_nodes; i++)
        {
            std::cout << std::setw(2) << labels[i] << " [ ";
            for(int j = 0; j < this->num_nodes; j++)
            {
                std::cout << std::setw(8) << transition_matrix[i][j];
                if(j < num_nodes - 1) std::cout << ", ";
            }
            std::cout << " ]" << std::endl;
        }
        std::cout << std::endl;
    #endif
    return transition_matrix;
}

std::vector<std::vector<double>> Graph::build_teleportation_matrix()
{
    std::vector<std::vector<double>> teleportation_matrix;
    teleportation_matrix.resize(this->num_nodes);

    for(int i = 0; i < this->num_nodes; i++)
        teleportation_matrix[i].resize(this->num_nodes, static_cast<double>(1.0/this->num_nodes));

    #ifdef DEBUG
        // Create index-to-label mapping for printing
        std::vector<std::string> labels(num_nodes);
        for(const auto& pair : node_to_index)
        {
            labels[pair.second] = pair.first;
        }

        // Pretty print with labels
        std::cout << "\n\t=== Teleportation Matrix (Column-Stochastic) ===" << std::endl;
        std::cout << std::fixed << std::setprecision(4);
        
        // Print column headers
        std::cout << " ";  // Space for row labels
        for(int j = 0; j < this->num_nodes; j++)
        {
            std::cout << std::setw(10) << labels[j];
        }
        std::cout << std::endl;
        
        // Print matrix with row labels
        for(int i = 0; i < this->num_nodes; i++)
        {
            std::cout << std::setw(2) << labels[i] << " [ ";
            for(int j = 0; j < this->num_nodes; j++)
            {
                std::cout << std::setw(8) << teleportation_matrix[i][j];
                if(j < num_nodes - 1) std::cout << ", ";
            }
            std::cout << " ]" << std::endl;
        }
        std::cout << std::endl;
    #endif
    return teleportation_matrix;
}

std::vector<std::vector<double>> Graph::compute_pagerank()
{
    auto transition_matrix    = build_transition_matrix();
    auto teleportation_matrix  = build_teleportation_matrix();
    
    std::vector<std::vector<double>> pagerank_matrix;

    return pagerank_matrix;
}

























