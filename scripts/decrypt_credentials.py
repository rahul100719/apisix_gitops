import json

with open("secret.txt", "r") as f:
    secret = f.read().strip()

print("Python received secret:", secret)  # THIS WILL PRINT REAL SECRET

try:
    decoded = json.loads(secret)
    print("Parsed JSON:", decoded)
except:
    print("Not JSON:", secret)
