#!/bin/bash
set -euo pipefail
echo "Initializing APISIX GitOps project structure..."

mkdir -p manifests/base
cat > manifests/base/deployment.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: apisix
  labels:
    app: apisix
spec:
  replicas: 1
  selector:
    matchLabels:
      app: apisix
  template:
    metadata:
      labels:
        app: apisix
    spec:
      containers:
      - name: apisix
        image: apache/apisix:2.14.0-alpine
        ports:
        - containerPort: 9080
EOF

cat > manifests/base/service.yaml <<'EOF'
apiVersion: v1
kind: Service
metadata:
  name: apisix
spec:
  selector:
    app: apisix
  ports:
    - port: 80
      targetPort: 9080
EOF

cat > manifests/kustomization.yaml <<'EOF'
resources:
- base/deployment.yaml
- base/service.yaml
EOF

echo "Init complete. Manifests created under manifests/base/"
