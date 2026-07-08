import subprocess


def run(*args, **kwargs):
    print("+", " ".join(map(str, args)))
    return subprocess.run(args, check=True, **kwargs)
