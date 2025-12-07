#!/usr/bin/env bash
set -euo pipefail

echo "Installing system dependencies..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script as root (e.g., using sudo)." >&2
  exit 1
fi

# Update package lists
echo "Updating package lists..."
apt update

# Install Python, venv, and SQLite3
echo "Installing Python, python3-venv, and sqlite3..."
apt install -y python3 python3.8-venv sqlite3

echo "System dependencies installed successfully."