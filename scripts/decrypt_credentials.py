import os
import json

# Jenkins passes: ENCRYPTED_CLIENTS_RAHUL
jenkins_value = os.environ.get("ENCRYPTED_CLIENTS_RAHUL")

print("Raw Jenkins Value Rahul:", jenkins_value)
with open("secret_val_rahul_new.txt", "w") as f:
        f.write(jenkins_value)

if not jenkins_value:
    print("Error: ENCRYPTED_CLIENTS_RAHUL not found")
    exit(1)

try:
    # If the Jenkins secret contains JSON
    parsed = json.loads(jenkins_value)
    print("Parsed JSON:", parsed)
    

except json.JSONDecodeError:
    # If it's just a string, not JSON
    print("Value is not JSON, treated as raw string.")
    parsed = jenkins_value

# TODO: Add your decryption logic here if needed
# decrypted = decrypt(parsed)

print("Final Secret Value:", parsed)
