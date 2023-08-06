import subprocess
import tempfile
import pathlib

WORK_DIR = pathlib.Path(__file__).resolve().parent
IN_FILE = WORK_DIR / "dev_env.yaml"

OS_MAP = {
    "unix": {"yaml_ignore": "# [win]", "build_names": ["linux-64", "osx-64"]},
    "win": {"yaml_ignore": "# [not win]", "build_names": ["win-64"],},
}


def _mk_os_yaml(os):
    # os map should be the string to comment for a given os
    with IN_FILE.open("r") as fi:
        data = fi.readlines()

    for i, val in enumerate(data):
        if OS_MAP[os]["yaml_ignore"] in val:
            data[i] = "  # " + val[2:]

    _, out_file = tempfile.mkstemp(prefix=os, suffix=".yaml")
    out_path = pathlib.Path(out_file)
    with out_path.open("w") as fo:
        fo.writelines(data)

    return out_path


def _mk_lock_files(os, in_file):
    lock_args = ["conda-lock", "--mamba", "-f", str(in_file)]
    for arg in OS_MAP[os]["build_names"]:
        lock_args.append("-p")
        lock_args.append(arg)
    subprocess.call(lock_args)
    in_file.unlink()


def _clean_lock_files(os):
    for conda_os in OS_MAP[os]["build_names"]:
        in_file = pathlib.Path(f"conda-{conda_os}.lock")

        with in_file.open("r") as fi:
            data = fi.readlines()

        # remove pywasp entries as we don't actually want to install them
        for i, val in enumerate(data):
            if f"{conda_os}/pywasp" in val:
                data.pop(i)

        with in_file.open("w") as fi:
            fi.writelines(data)


if __name__ == "__main__":
    for os in OS_MAP.keys():
        print(os)
        work_path = _mk_os_yaml(os)
        _mk_lock_files(os, work_path)
        _clean_lock_files(os)
