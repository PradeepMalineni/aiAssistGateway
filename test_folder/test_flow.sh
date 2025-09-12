#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8765}"
OAS_PATH="${OAS_PATH:-apis/payments/openapi.yaml}"
OUT_DIR="${OUT_DIR:-.out}"

jq_bin="$(command -v jq || true)"
if [[ -z "$jq_bin" ]]; then
  echo "jq is required. Install jq and re-run." >&2
  exit 1
fi

echo "== DevX Gateway Assistant: test flow =="
echo "BASE_URL=$BASE_URL"
echo "OAS_PATH=$OAS_PATH"
echo "OUT_DIR=$OUT_DIR"
echo

echo "-- 1) MCP manifest --"
curl -s "${BASE_URL}/.well-known/mcp.json" | jq '.name,.version,.tools | length'

echo "-- 2) Discover OAS --"
# Prefer JSON body; fallback to query param if server expects it
discover_json=$(curl -s -X POST "${BASE_URL}/tools/discover_oas"   -H "Content-Type: application/json"   -d "{"workspaceRoot":"."}" || true)
if [[ -z "$discover_json" || "$discover_json" == *"422"* ]]; then
  discover_json=$(curl -s -X POST "${BASE_URL}/tools/discover_oas?workspaceRoot=." )
fi
echo "$discover_json" | jq

echo "-- 3) Analyze OAS --"
traits=$(curl -s -X POST "${BASE_URL}/tools/analyze_oas"   -H "Content-Type: application/json"   -d "{"oasPath":"${OAS_PATH}","useAI":true}")
echo "$traits" | jq

echo "-- 4) Decide gateway --"
decision=$(curl -s -X POST "${BASE_URL}/tools/decide_gateway"   -H "Content-Type: application/json"   -d "{"traits":${traits},"useAI":true}")
echo "$decision" | jq

echo "-- 5) Synthesize guardrails --"
plan=$(curl -s -X POST "${BASE_URL}/tools/synthesize_guardrails"   -H "Content-Type: application/json"   -d "{"traits":${traits},"useAI":true}")
echo "$plan" | jq

echo "-- 6) Generate bundle --"
build=$(curl -s -X POST "${BASE_URL}/tools/generate_bundle"   -H "Content-Type: application/json"   -d "{"oasPath":"${OAS_PATH}","decision":${decision},"plan":${plan},"outDir":"${OUT_DIR}"}")
echo "$build" | jq

echo "-- 7) Gate (policy check) --"
applied=$(echo "$build" | jq '.applied_controls')
gate=$(curl -s -X POST "${BASE_URL}/tools/opa_gate"   -H "Content-Type: application/json"   -d "{"plan":${plan},"appliedControls":${applied}}")
echo "$gate" | jq

echo "-- 8) One-shot end-to-end (sanity) --"
oneshot=$(curl -s -X POST "${BASE_URL}/tools/run_gateway_assistant"   -H "Content-Type: application/json"   -d "{"oasPath":"${OAS_PATH}","outDir":"${OUT_DIR}","useAI":true}")
echo "$oneshot" | jq

echo
echo "Artifacts (if any) should be under: ${OUT_DIR}/"
