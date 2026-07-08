#!/usr/bin/env python3

from pathlib import Path
from shutil import move


def merge(packages: Path, repository: Path) -> None:
    for arch in packages.iterdir():
        if not arch.is_dir():
            continue

        repo_arch = repository / arch.name
        repo_arch.mkdir(parents=True, exist_ok=True)

        for package in arch.glob("*.xbps"):
            destination = repo_arch / package.name

            if destination.exists():
                destination.unlink()

            move(package, destination)
