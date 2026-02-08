FROM python:3.11-slim

# Install system dependencies for C++ compilation
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies including pybind11
RUN pip install --no-cache-dir \
    flask==3.0.0 \
    flask-cors==4.0.0 \
    matplotlib==3.8.2 \
    networkx==3.2.1 \
    numpy==1.26.2 \
    pybind11[global]

# Copy C++ source and build system
COPY lib/ ./lib/
COPY src/ ./src/
COPY bindings/ ./bindings/
COPY CMakeLists.txt ./

# Create python/pagerank directory for the compiled module
RUN mkdir -p python/pagerank

# Build C++ module with pybind11
RUN mkdir -p build && \
    cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release \
          -DPYTHON_EXECUTABLE=$(which python3) \
          -Dpybind11_DIR=$(python3 -m pybind11 --cmakedir) \
          .. && \
    cmake --build . && \
    cd ..

# Copy the compiled module to python/pagerank
RUN cp python/pagerank/*.so python/pagerank/ 2>/dev/null || \
    find build -name "pagerank_cpp*.so" -exec cp {} python/pagerank/ \;

# Verify the module exists
RUN ls -la python/pagerank/ && \
    python3 -c "import sys; sys.path.insert(0, 'python/pagerank'); import pagerank_cpp; print('Module loaded successfully!')"

# Copy Flask application
COPY app.py ./

# Create output directory
RUN mkdir -p /app/output

# Expose port
EXPOSE 5000

# Run Flask
CMD ["python3", "app.py"]
