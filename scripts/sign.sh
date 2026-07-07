#!/bin/sh
set -eu

[ $# -eq 3 ] || {
    echo "Usage: $0 <target-dir> <private-key> <signed-by>" >&2
    exit 1
}

TARGET="$1"
KEY="$2"
SIGNER="$3"


for repo in "$TARGET"/*
do
  echo "signing $repo packages"
  xbps-rindex --privkey "$KEY" -S "$repo"/*.xbps
  echo "signing $repo"
  xbps-rindex --privkey "$KEY" -s "$repo" --signedby "$SIGNER"
done
