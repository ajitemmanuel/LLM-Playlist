#!/usr/bin/env bash
set -euo pipefail

S=http://127.0.0.1:8000/mcp
ACCEPT='application/json, text/event-stream'
CT='application/json'

echo "Initializing session..."

# 1) initialize
SID=$(curl -sSL -D - -o /dev/null \
  -H "Accept: $ACCEPT" -H "Content-Type: $CT" \
  -X POST $S \
  -d '{
    "jsonrpc":"2.0","id":1,"method":"initialize","params":{
      "protocolVersion":"2025-03-26",
      "capabilities":{},
      "clientInfo":{"name":"bash","version":"1.0"}
    }
  }' | sed -nE 's/^Mcp-Session-Id:[[:space:]]*//Ip' | tr -d '\r')

echo "SID=$SID"

# 2) notifications/initialized
curl -sSL \
  -H "Accept: $ACCEPT" \
  -H "Content-Type: $CT" \
  -H "Mcp-Session-Id: $SID" \
  -X POST $S \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}'

# 3) tools/call
echo "Calling add(2, 3)..."
RESPONSE=$(curl -sSL \
  -H "Accept: $ACCEPT" \
  -H "Content-Type: $CT" \
  -H "Mcp-Session-Id: $SID" \
  -X POST $S \
  -d '{
    "jsonrpc":"2.0",
    "id":2,
    "method":"tools/call",
    "params":{"name":"add","arguments":{"a":2,"b":3}}
  }')

echo "Response from server:"
echo "$RESPONSE"

# Extract and print result if jq is available
if command -v jq > /dev/null; then
  echo "Result value:"
  echo "$RESPONSE" | sed -n 's/^data: //p' | jq '.result.structuredContent.result'
fi
