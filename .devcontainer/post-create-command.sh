#!/bin/bash

# Install ffmpeg
echo "Installing ffmpeg..."
sudo apt-get update && sudo apt-get install -y ffmpeg

# Install uv package manager
echo "Installing uv package manager..."
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create and activate virtual environment
echo "Creating virtual environment..."
uv venv --clear

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install project dependencies
echo "Installing project dependencies..."
uv sync

echo "Setup completed successfully!"
