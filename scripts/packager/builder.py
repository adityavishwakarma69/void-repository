from subprocess import check_output
from shutil import copytree, move, rmtree
from pathlib import Path
from .utils import run

VALID_ARCHS = {"x86_64", "aarch64", "x86_64-musl", "aarch64-musl"}


def validate_archs(archs: list[str]) -> None:
    for arch in archs:
        if arch not in VALID_ARCHS:
            raise RuntimeError(f"invalid {arch} requested")


class Builder:
    def __init__(self, void_dir: Path, project_dir: Path, target_dir: Path,
                 archs: list[str]):
        print("init builder... ")
        self.project_dir = project_dir
        self.void_dir = void_dir
        self.target_dir = target_dir
        self.target_pkgs: list[str] = []
        validate_archs(archs)
        self.archs = archs
        self.host_arch = check_output(["xbps-uhelper", "arch"],
                                      text=True).strip()

    def populate_srcpkgs(self) -> list[str]:
        print("populating srcpkgs... ")
        srcpkgs = self.project_dir/"srcpkgs"
        dst = self.void_dir/"srcpkgs"
        pkgs: list[str] = []
        for pkg in srcpkgs.iterdir():
            if not pkg.is_dir():
                continue

            copytree(
                pkg,
                dst / pkg.name,
                dirs_exist_ok=True
            )
            pkgs.append(pkg.name)
        return pkgs

    def build_packages(self,
                       packages: list[str],
                       arch: str) -> None:

        print("building pkgs", *packages, f"for {arch}")
        args = ["./xbps-src"]
        if arch != self.host_arch:
            args.extend(["-a", arch])
        args.extend(["pkg", *packages])

        run(*args, cwd=self.void_dir)

    def collect_repo(self, arch: str) -> None:
        src = self.void_dir/"hostdir"/"binpkgs"
        dst = self.target_dir/arch
        print(f"collecting repository of {arch} to {dst}")
        if dst.exists():
            rmtree(dst)
        move(src, dst)

    def build(self) -> None:
        self.target_dir.mkdir(parents=True, exist_ok=True)
        self.target_pkgs = self.populate_srcpkgs()
        for arch in self.archs:
            self.build_packages(self.target_pkgs, arch)
            self.collect_repo(arch)
