import os
import yaml
from cryptography.fernet import Fernet

key = open("../apisix_secret.key", "rb").read()
fernet = Fernet(key)

# Check if Jenkins passed encrypted credentials
jenkins_clients = os.environ.get("ENCRYPTED_CLIENTS_Rahul")
if jenkins_clients:
    import json
    clients = json.loads(jenkins_clients)
    print("Decrypted Client ID:", clients)
else:
    with open("../configs/encrypted_credentials.yaml", "r") as f:
        data = yaml.safe_load(f)
    clients = data.get("clients", [])

for c in clients:
    client_id = fernet.decrypt(c['id'].encode()).decode()
    client_secret = fernet.decrypt(c['secret'].encode()).decode()
    print("Decrypted Client ID:", client_id)
    print("Decrypted Client Secret:", client_secret)
