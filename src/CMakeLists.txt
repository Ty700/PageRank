set(PAGERANK_SRC
    graph.cpp
    pagerank.cpp
)

target_sources(${EXE_NAME} PRIVATE ${PAGERANK_SRC})
