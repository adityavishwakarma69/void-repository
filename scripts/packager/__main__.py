#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from .checks import run_checks
from .environment import setup_environment, prepare_environment
from .builder import Builder


def parse_args():
    parser = ArgumentParser(
        prog="repository",
        description="Void repository build tool"
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        required=True,
        help="Workspace directory used for building"
    )
    parser.add_argument(
        "--target",
        type=Path,
        required=True,
        help="Target directory for generating repositories"
    )
    parser.add_argument(
        "--arch",
        nargs="+",
        default=["x86_64"],
    )

    return parser.parse_args()


def main():
    args = parse_args()

    run_checks()

    workspace_dir = args.workspace
    void_dir = setup_environment(workspace_dir)
    target_dir = args.target
    project_dir = Path.cwd()

    prepare_environment(void_dir)
    builder = Builder(
        void_dir=void_dir,
        project_dir=project_dir,
        target_dir=target_dir,
        archs=args.arch)

    builder.build()


if __name__ == "__main__":
    main()
