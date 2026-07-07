#!/bin/sh
set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

HOST_ARCH="$(xbps-uhelper arch)"
ARCHS="$HOST_ARCH"

VOID_REPO="https://github.com/void-linux/void-packages.git"

parse_args() {
  while [ $# -gt 0 ]; do
    case "$1" in
      --arch)
        [ $# -ge 2 ] || {
          echo "Missing value for --arch" >&2
                  exit 1
        }
      ARCHS="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
    esac
  done
}

setup_build_dir() {
    BUILD_DIR="$(mktemp -d)"
    trap 'rm -rf "$BUILD_DIR"' EXIT

    VOID_DIR="$BUILD_DIR/void-packages"
    SRCPKGS="$PROJECT_DIR/srcpkgs"
}

setup_environment() {
    git clone \
        --depth=1 \
        "$VOID_REPO" \
        "$VOID_DIR"

    cd "$VOID_DIR"

    cp -r "$SRCPKGS"/* srcpkgs


    common/travis/set_mirror.sh
    common/travis/prepare.sh
}

build_package() {
    pkg="$1"
    arch="$2"

    if [ "$arch" = "$HOST_ARCH" ]; then
        ./xbps-src pkg "$pkg"
    else
        ./xbps-src -a "$arch" pkg "$pkg"
    fi
}

build_packages() {
    arch="$1"
    echo "Building for $arch"
    for pkg in "$SRCPKGS"/*; do
        build_package "$(basename "$pkg")" "$arch"
    done
}

index_packages() {
    arch="$1"
    echo "Indexing Packages for $arch"
    output_dir="$PROJECT_DIR/target/$arch"
    mkdir -p "$output_dir"

    rm -f "$output_dir"/*.xbps
    cp hostdir/binpkgs/*.xbps "$output_dir"

    env XBPS_ARCH="$arch" \
        xbps-rindex -a "$output_dir"/*.xbps

    rm -f hostdir/binpkgs/*.xbps
}

main() {
    parse_args "$@"

    setup_build_dir
    setup_environment
    for arch in $ARCHS; do
      build_packages $arch
      index_packages $arch
    done
}

main "$@"
