#!/bin/bash

# Exit on error
set -e

# Print commands as they are executed
set -x

# Function to kill existing server processes
kill_existing_server() {
    echo "Checking for existing server processes..."
    # Find processes using port 8080
    local pid=$(lsof -ti:8080)
    if [ ! -z "$pid" ]; then
        echo "Killing existing server process (PID: $pid)..."
        kill -9 $pid 2>/dev/null || true
        # Give it a moment to fully terminate
        sleep 1
    fi
}

# Function to handle cleanup on exit
cleanup() {
    echo "Shutting down MCP server..."
    kill_existing_server
}

# Set up trap for cleanup
trap cleanup EXIT

# Kill any existing server processes
kill_existing_server

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed. Please install uv first."
    exit 1
fi

# Check if uvx is available
if ! command -v uvx &> /dev/null; then
    echo "Error: uvx is not installed. Please install uvx first."
    exit 1
fi

# Clean up existing environment and lock files
echo "Cleaning up existing environment..."
rm -rf .venv
rm -f uv.lock

# Install dependencies using uv sync
echo "Installing dependencies with uv sync..."
uv sync || {
    echo "Failed to install dependencies"
    exit 1
}

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate || {
    echo "Failed to activate virtual environment"
    exit 1
}

# Start the MCP server
echo "Starting MCP server..."
exec uvx mcpo --port 8080 -- uv run --with mcp[cli] --with git+https://github.com/cluesang/pyBittle.git mcp run ./server.py

# Keep the script running until interrupted
while true; do
    sleep 1
done 