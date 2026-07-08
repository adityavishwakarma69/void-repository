from pathlib import Path
from .utils import run
import os


def index_packages(arch: Path) -> None:
    env = os.environ.copy()
    env["XBPS_ARCH"] = arch.name
    packages = list(arch.glob("*.xbps"))
    if not packages:
        print(f"no packages in {arch.name} skipping")
        return
    run(
        "xbps-rindex",
        "-a", *(str(pkg) for pkg in packages),
        env=env
    )
    run(
        "xbps-rindex",
        "-r", str(arch),
        env=env
    )


def index(repository: Path) -> None:
    for arch in repository.iterdir():
        if not arch.is_dir():
            continue

        print(f"indexing {arch.name}")
        index_packages(arch)
