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

# Install Python and venv
echo "Installing Python and python3-venv..."
apt install -y python3 python3.8-venv

echo "System dependencies installed successfully."