#!/bin/bash
set -euo pipefail
echo "Deploying APISIX manifests to Kubernetes..."
if [ -z "${KUBECONFIG:-}" ]; then
  echo "KUBECONFIG not set. Use KUBECONFIG env or provide kubeconfig file."
  exit 1
fi

kubectl apply -k manifests/
