import grp
import os
import shutil


def check_not_root() -> None:
    if os.geteuid() == 0:
        raise RuntimeError(
            "Repository builder must not be root."
        )
    print("Normal user (ok)")


def check_xbuilder_group() -> None:
    groups = {
        grp.getgrgid(gid).gr_name
        for gid in os.getgroups()
    }

    if "xbuilder" not in groups:
        raise RuntimeError(
            "Current user is not a member of the 'xbuilder' group."
        )
    print("User is a xbuilder (ok)")


def check_xbps_uchroot() -> None:
    if shutil.which("xbps-uchroot") is None:
        raise RuntimeError(
            "xbps-uchroot was not found. Please install the xtools package."
        )
    print("xbps-uchroot installed (ok)")


def run_checks() -> None:
    check_not_root()
    check_xbuilder_group()
    check_xbps_uchroot()
