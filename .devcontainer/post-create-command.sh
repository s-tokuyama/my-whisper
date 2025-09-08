#!/bin/bash

# Install uv package manager
echo "Installing uv package manager..."
curl -LsSf https://astral.sh/uv/install.sh | sh

# Source cargo environment to make uv available
source $HOME/.cargo/env

# Create and activate virtual environment
echo "Creating virtual environment..."
uv venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install project dependencies
echo "Installing project dependencies..."
uv sync

echo "Setup completed successfully!"
