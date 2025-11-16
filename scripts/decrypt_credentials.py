import os
from cryptography.fernet import Fernet

key = open("../apisix_secret.key", "rb").read()
fernet = Fernet(key)

# Check if Jenkins passed encrypted credentials
jenkins_clients = os.environ.get("ENCRYPTED_CLIENTS_Rahul")
print("Decrypted Client ID:", json.loads(jenkins_clients))
if jenkins_clients:
    import json
    clients = json.loads(jenkins_clients)
    print("Decrypted Client ID:", clients)
