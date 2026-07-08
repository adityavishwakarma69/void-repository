#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from .merge import merge
from .index import index
from .sign import sign


def parse_args():
    parser = ArgumentParser(
        prog="repository",
        description="merge index and sign void repositories"
    )
    parser.add_argument(
        "--packages",
        type=Path,
        required=True,
        help="Packages directory for merging with repository"
    )
    parser.add_argument(
        "--repository",
        type=Path,
        required=True,
        help="Repository directory to be merger with the packages"
    )
    parser.add_argument(
        "--key",
        type=Path,
        required=True,
        help="Private RSA key file to sign the repository and packages"
    )
    parser.add_argument(
        "--signedby",
        type=str,
        required=True,
        help="Name of the person who signed the repository"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    packages_dir = args.packages
    repository_dir = args.repository
    key_file = args.key
    signer = args.signedby

    merge(packages_dir, repository_dir)
    index(repository_dir)
    sign(repository_dir, key_file, signer)


if __name__ == "__main__":
    main()
