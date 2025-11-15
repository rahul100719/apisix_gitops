#!/bin/bash
set -euo pipefail
echo "=== APISIX GitOps: build.sh ==="

if command -v kubectl >/dev/null 2>&1; then
  echo "Validating kustomize manifests..."
  kubectl kustomize manifests >/dev/null 2>&1 || { echo "kustomize failed"; exit 1; }
  echo "Validation OK"
else
  echo "kubectl not installed - skipping validation"
fi

echo "Build complete."
