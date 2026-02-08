cmake_minimum_required(VERSION 3.15)
project(PageRank)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Find Python and pybind11
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 REQUIRED)

# Include directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/lib)

# Create Python module
pybind11_add_module(pagerank_cpp 
    bindings/pagerank_bindings.cpp
    src/graph.cpp
)

# Set output directory
set_target_properties(pagerank_cpp PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/python/pagerank"
)
