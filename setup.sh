#!/bin/bash

# Author: Aditya Bhatt
# Date: 10:08 AM 30-08-2024
# NOTE: This script sets up a Python virtual environment, activates it, and installs required packages.

# Step 1: Create a virtual environment
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "Virtual environment 'venv' created."
else
    echo "Virtual environment 'venv' already exists."
fi

# Step 2: Activate the virtual environment
# For Unix-based systems (Linux, macOS)
source venv/Scripts/activate

# Step 3: Install required packages
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Installed packages from requirements.txt."
else
    pip install Flask
    echo "requirements.txt not found. Installed Flask by default."
fi

echo "Virtual environment setup and package installation complete."
