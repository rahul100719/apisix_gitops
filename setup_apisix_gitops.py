import os
import sys
import yaml
import zipfile
from cryptography.fernet import Fernet

# ---------- Helper Functions ----------
def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)
    print(f"Created file: {path}")

# ---------- Config Input ----------
# YAML file containing multiple clients and routes
# Example: apisix_config.yaml
"""
clients:
  - id: client1
    secret: secret1
  - id: client2
    secret: secret2
routes:
  - name: route1
    path: /route1
    service: service1
    port: 80
  - name: route2
    path: /route2
    service: service2
    port: 8080
"""

config_file = "apisix_config.yaml"
if not os.path.exists(config_file):
    sys.exit(f"{config_file} not found. Please create the YAML file with clients and routes.")

with open(config_file, "r") as f:
    config = yaml.safe_load(f)

# ---------- Project Structure ----------
project_name = "apisix_gitops"
create_dir(project_name)
os.chdir(project_name)

dirs = ["routes", "plugins", "scripts", "configs"]
for d in dirs:
    create_dir(d)

# ---------- Secret Key ----------
secret_file = "apisix_secret.key"
if not os.path.exists(secret_file):
    key = Fernet.generate_key()
    write_file(secret_file, key.decode())
else:
    with open(secret_file, "rb") as f:
        key = f.read()

fernet = Fernet(key)

# ---------- Encrypt Client Credentials ----------
encrypted_creds = []
for client in config.get("clients", []):
    enc_id = fernet.encrypt(client["id"].encode()).decode()
    enc_secret = fernet.encrypt(client["secret"].encode()).decode()
    encrypted_creds.append({"id": enc_id, "secret": enc_secret})

# Write encrypted credentials to configs/encrypted_credentials.yaml
enc_file_content = yaml.dump({"clients": encrypted_creds})
write_file("configs/encrypted_credentials.yaml", enc_file_content)

# ---------- Generate Route Files ----------
for route in config.get("routes", []):
    route_content = f"""
apiVersion: apisix.apache.org/v2
kind: ApisixRoute
metadata:
  name: {route['name']}
spec:
  http:
    - name: {route['name']}
      match:
        paths:
          - {route['path']}
      backend:
        serviceName: {route['service']}
        servicePort: {route['port']}
"""
    write_file(f"routes/{route['name']}.yaml", route_content)

# ---------- Example Plugin ----------
plugin_file = """-- Example plugin
local plugin = require("apisix.plugin")
local core = require("apisix.core")

local _M = {version=0.1, priority=1000}

function _M.access(conf, ctx)
    core.log.info("Example plugin running")
end

return _M
"""
write_file("plugins/example_plugin.lua", plugin_file)

# ---------- Scripts ----------
# decrypt_credentials.py (reads from file or Jenkins ENV)
decrypt_script = f"""import os
import yaml
from cryptography.fernet import Fernet

key = open("../{secret_file}", "rb").read()
fernet = Fernet(key)

# Check if Jenkins passed encrypted credentials
jenkins_clients = os.environ.get("ENCRYPTED_CLIENTS")
if jenkins_clients:
    import json
    clients = json.loads(jenkins_clients)
else:
    with open("../configs/encrypted_credentials.yaml", "r") as f:
        data = yaml.safe_load(f)
    clients = data.get("clients", [])

for c in clients:
    client_id = fernet.decrypt(c['id'].encode()).decode()
    client_secret = fernet.decrypt(c['secret'].encode()).decode()
    print("Decrypted Client ID:", client_id)
    print("Decrypted Client Secret:", client_secret)
"""
write_file("scripts/decrypt_credentials.py", decrypt_script)

# ---------- Makefile ----------
makefile_content = f"""
SHELL := /bin/bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: init decrypt package

init:
\t@echo "Project initialized"

decrypt:
\t@python3 scripts/decrypt_credentials.py

package:
\tzip -r ../apisix_gitops_package.zip .
"""
write_file("Makefile", makefile_content)

# ---------- Create ZIP ----------
zip_name = "../apisix_gitops_package.zip"
with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk("."):
        for file in files:
            zipf.write(os.path.join(root, file))
print(f"\n✅ Project zipped successfully as {zip_name}")
