#!/usr/bin/env bash
# Run from the extracted repository root on Ubuntu. Requires Mininet/OS-Ken.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "Person 2 files:"
python3 -m py_compile person2/smart_content_controller_osken.py \
  person2/smart_content_topology.py person2/smart_content_gateway.py \
  person2/gateway_client.py

echo "Python syntax checks passed."
echo "Start controller in terminal 1:"
echo "  cd '$ROOT/person2' && osken-manager --ofp-tcp-listen-port 6653 smart_content_controller_osken.py"
echo "Start Mininet in terminal 2:"
echo "  sudo python3 '$ROOT/person2/smart_content_topology.py'"
echo "Then follow person2/README.txt for in-Mininet commands."
