#!/bin/bash
set -euo pipefail
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <secret-file> <output-encrypted-file>"
  exit 1
fi
SECRET_FILE="$1"
OUT_FILE="$2"
openssl enc -aes-256-cbc -salt -pbkdf2 -pass pass:change_me -in "$SECRET_FILE" -out "$OUT_FILE"
echo "Encrypted $SECRET_FILE -> $OUT_FILE (password is 'change_me' - replace in production)"
