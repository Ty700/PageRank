FROM python:3.11-slim

# Install system dependencies for C++ compilation
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python requirements first (for layer caching)
RUN echo "flask==3.0.0" > requirements.txt && \
    echo "flask-cors==4.0.0" >> requirements.txt && \
    echo "matplotlib==3.8.2" >> requirements.txt && \
    echo "networkx==3.2.1" >> requirements.txt && \
    echo "numpy==1.26.2" >> requirements.txt && \
    echo "pybind11==2.11.1" >> requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy C++ source and build system
COPY lib/ ./lib/
COPY src/ ./src/
COPY bindings/ ./bindings/
COPY CMakeLists.txt ./
COPY build.py ./

# Build C++ module
RUN python3 build.py

# Copy Flask application
COPY app.py ./

# Create output directory
RUN mkdir -p /app/output

# Expose port
EXPOSE 5000

# Run Flask
CMD ["python3", "app.py"]
