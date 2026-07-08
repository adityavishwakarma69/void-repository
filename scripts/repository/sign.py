from pathlib import Path
import os
from .utils import run


def sign_repositor(arch: Path, key_file: Path, signer: str) -> None:
    env = os.environ.copy()
    env["XBPS_ARCH"] = arch.name
    packages = list(arch.glob("*.xbps"))
    if not packages:
        print(f"no packages in {arch.name} skipping")
        return
    run(
        "xbps-rindex",
        "-S", *(str(pkg) for pkg in packages),
        env=env
    )
    run(
        "xbps-rindex",
        "-s", str(arch),
        "--signedby", signer,
        env=env
    )


def sign(repository: Path, key_file: Path, signer: str):
    for arch in repository.iterdir():
        if not arch.is_dir():
            continue

        print(f"signing {arch.name}")
        sign_repositor(arch)
