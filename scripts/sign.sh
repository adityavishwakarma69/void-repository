#!/bin/sh
set -eu

[ $# -eq 3 ] || {
    echo "Usage: $0 <target-dir> <private-key> <signed-by>" >&2
    exit 1
}

TARGET="$1"
KEY="$2"
SIGNER="$3"


for repo in "$TARGET"/*; do
    [ -d "$repo" ] || continue

    arch="$(basename "$repo")"

    env XBPS_ARCH="$arch" \
        xbps-rindex --privkey "$KEY" -S "$repo"/*.xbps

    env XBPS_ARCH="$arch" \
        xbps-rindex \
            --privkey "$KEY" \
            --signedby "$SIGNER" \
            -s "$repo"
done
