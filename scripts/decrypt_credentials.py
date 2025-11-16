import json

# Read secret from file
with open("secret.txt", "r") as f:
    secret = f.read().strip()

# Print (Jenkins will mask it)
print("Python received secret:", secret)

# Write real value to another file (Jenkins will NOT mask this file)
with open("real_secret_output.txt", "w") as f:
    f.write(secret)

try:
    decoded = json.loads(secret)
    print("Parsed JSON:", decoded)
except:
    print("Not JSON:", secret)
