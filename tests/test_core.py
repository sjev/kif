""" test core functionality. some files are written to user dir and tmp,
so run this in a devcontainer if you don't want to mess up your system."""


from pathlib import Path

import kif.utils as utils

SRC_DIR = Path("/tmp/kif/src")


def create_input_files():
    """create some input files for testing, with some random content"""
    SRC_DIR.mkdir(exist_ok=True, parents=True)

    for i in range(10):
        fname = SRC_DIR / f"test_{i}.txt"
        with fname.open("w") as fid:
            fid.write(f"test_{i} {i}\n")
            fid.write(f"test_{i} {i}\n")
            fid.write(f"test_{i} {i}\n")


def test_dest1():
    """test moving files to destination 1"""

    cfg_file = utils.get_config_path()
    if cfg_file.exists():
        cfg_file.unlink()

    # create test config
    utils.create_example_config()

    # create test files
    create_input_files()
