# Find pybind11
find_package(pybind11 REQUIRED)

# Find Python
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

# Create Python module
pybind11_add_module(pagerank_cpp 
    pagerank_bindings.cpp 
    ${CMAKE_SOURCE_DIR}/src/graph.cpp
)

target_include_directories(pagerank_cpp PRIVATE 
    ${CMAKE_SOURCE_DIR}/lib
)

set_target_properties(pagerank_cpp PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/python/pagerank"
)
