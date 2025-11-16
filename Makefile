# Makefile for APISIX GitOps - full CI/CD scaffold
PROJECT_NAME ?= apisix_gitops
ZIP_FILE = $(PROJECT_NAME).zip
MANIFESTS_DIR = manifests

.PHONY: all init build test lint zip deploy clean get_secret

all: init build test zip

init:
	@echo "Initializing project..."
	@mkdir -p $(MANIFESTS_DIR)
	@echo "# kustomization" > $(MANIFESTS_DIR)/kustomization.yaml || true

build:
	@echo "Running build steps (validate manifests)..."
	if command -v kubectl >/dev/null 2>&1; then \
		kubectl kustomize $(MANIFESTS_DIR) >/dev/null 2>&1 && echo "kustomize OK" || (echo "kustomize FAILED" && exit 1); \
	else \
		echo "kubectl not found; skipping kustomize check"; \
	fi

test:
	@echo "Run unit / manifest tests (placeholder)"
	@echo "No tests configured — add commands in Makefile:test"

lint:
	@echo "Linting YAMLs..."
	@which yamllint >/dev/null 2>&1 && yamllint $(MANIFESTS_DIR) || echo "yamllint not found"

zip:
	@echo "Creating ZIP package: $(ZIP_FILE)"
	@rm -f $(ZIP_FILE)
	@zip -r $(ZIP_FILE) . -x '*.git*' '*.zip' || true

deploy:
	@echo "Deploying manifests to Kubernetes (requires kubectl configured)"
	if [ -d "$(MANIFESTS_DIR)" ]; then \
		kubectl apply -k $(MANIFESTS_DIR); \
	else \
		echo "Manifests directory not found"; exit 1; \
	fi

clean:
	@echo "Cleaning artifacts..."
	@rm -f $(ZIP_FILE)

get_secret:
	@echo "Decrypting Rahul Client Secret..."
	@echo "Secret passed: $(ENCRYPTED_CLIENTS_RAHUL)"
	@python scripts/decrypt_credentials.py "$(ENCRYPTED_CLIENTS_RAHUL)"
