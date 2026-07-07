import subprocess


def run(*args, cwd=None):
    print("+", " ".join(args))
    subprocess.run(args, cwd=cwd, check=True)
