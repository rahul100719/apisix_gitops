# APISIX GitOps - Example Project

This repository is a scaffold for APISIX GitOps with a Makefile and Jenkins pipeline.

Folders:
- manifests/: kustomize-able Kubernetes manifests
- scripts/: helper scripts (init, build, deploy, encrypt)
- Jenkinsfile: declarative pipeline example
- Makefile: common targets (init, build, test, zip, deploy)

Usage:
- Local: `make init && make build`
- CI: Jenkins will run `make build` and `make zip`
- Deploy: `KUBECONFIG=~/.kube/config make deploy`

Notes:
- Replace placeholder secrets and credentials before using in production.
