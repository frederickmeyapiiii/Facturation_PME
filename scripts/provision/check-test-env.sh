#!/bin/bash
set -euo pipefail

host="${1:-localhost}"
port="${2:-8001}"
url="http://${host}:${port}/admin/"

response=$(curl -s -o /dev/null -w "%{http_code}" "$url")

if [[ "$response" =~ ^([23])[0-9]{2}$ ]]; then
  echo "OK: test environment responded with $response"
  exit 0
fi

echo "FAIL: expected 2xx or 3xx, got $response"
exit 1
