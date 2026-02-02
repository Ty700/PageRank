cmake_minimum_required(VERSION 3.28)
project(PageRankingApp VERSION 1.0.0)
include(ProcessorCount)

ProcessorCount(N)
if(NOT N EQUAL 0)
	set(CMAKE_BUILD_PARALLEL_LEVEL ${N})
	message(STATUS "Building with ${N} Jobs")
endif()

set(EXE_NAME PageRankingApp)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_executable(${EXE_NAME} src/pagerank.cpp)
add_subdirectory(src)
add_subdirectory(lib)
add_subdirectory(bindings)

target_compile_options(${EXE_NAME} PRIVATE -Wall -Wextra) 

target_compile_options(${EXE_NAME} PRIVATE
  $<$<CONFIG:Debug>:-DDEBUG>
)

set_target_properties(${EXE_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY_DEBUG "${CMAKE_BINARY_DIR}/../bin/debug"
    RUNTIME_OUTPUT_DIRECTORY_RELEASE "${CMAKE_BINARY_DIR}/../bin/release"
)
