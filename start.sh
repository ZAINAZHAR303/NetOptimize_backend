#!/bin/bash
# Install system dependencies
apt-get update && apt-get install -y libssl-dev gcc

# Install Python dependencies
pip install -r requirements.txt

# Run the application
uvicorn main2:app --host 0.0.0.0 --port $PORT