from pathlib import Path
from .utils import run

VOID_REPO = "https://github.com/void-linux/void-packages.git"


def prepare_environment(void_dir: Path) -> None:
    print(f"preparing {void_dir} for bulding packages")
    print("setting appropriate mirror")
    run(
        "common/travis/set_mirror.sh",
        cwd=void_dir
    )
    print("applying environment patches and bootstraping environment")
    run(
        "common/travis/prepare.sh",
        cwd=void_dir
    )


def setup_environment(workspace: Path):
    workspace.mkdir(parents=True, exist_ok=True)
    void_dir = workspace/"void-packages"

    if void_dir.exists():
        print(f"{void_dir} already exists, skipping git clone")
        return void_dir

    run("git", "clone", "--depth=1", VOID_REPO, str(void_dir))

    return void_dir
