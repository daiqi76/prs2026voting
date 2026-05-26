#!/bin/bash
# start.sh
# One-command launcher: activates venv, starts Flask, then starts ngrok tunnel.

set -e

VENV_DIR="$(dirname "$0")/venv"

# Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

# Install dependencies
pip install -q -r "$(dirname "$0")/requirements.txt"

# Initialize database and start Flask in background
echo "Starting Flask server on port 5000..."
cd "$(dirname "$0")"
python app.py &
FLASK_PID=$!

sleep 2

# Start ngrok (must be installed and authenticated separately)
if command -v ngrok &> /dev/null; then
  echo ""
  echo "Starting ngrok tunnel..."
  echo "Your public voting URL will appear below:"
  echo "-------------------------------------------"
  ngrok http --domain=email-dazzler-squint.ngrok-free.dev 5001
else
  echo ""
  echo "ngrok not found. Flask is running locally."
  echo "Voting URL (LAN only): http://$(ipconfig getifaddr en0):5001"
  echo "Admin URL  (LAN only): http://$(ipconfig getifaddr en0):5001/admin"
  echo ""
  echo "To enable public access, install ngrok: https://ngrok.com/download"
  wait $FLASK_PID
fi
