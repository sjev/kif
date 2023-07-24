""" test core functionality. some files are written to user dir and tmp,
so run this in a devcontainer if you don't want to mess up your system."""


from pathlib import Path
import shutil
import logging
import pytest

import kif.utils as utils


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("core")

SRC_DIR = Path("/tmp/kif/src")

log.info("testing core functionality")
print("testing core functionality")


def create_config():
    cfg_file = utils.get_config_path()
    if cfg_file.exists():
        cfg_file.unlink()

    # create test config
    utils.create_example_config()


def create_input_files():
    """create some input files for testing, with some random content"""
    SRC_DIR.mkdir(exist_ok=True, parents=True)
    log.info("%s", f"creating test files in {SRC_DIR}")
    for i in range(10):
        fname = SRC_DIR / f"test_{i}.txt"

        with fname.open("w") as fid:
            fid.write(f"test_{i} {i}\n")
            fid.write(f"test_{i} {i}\n")
            fid.write(f"test_{i} {i}\n")
    # add some pdf files
    for i in range(3):
        fname = SRC_DIR / f"foo_{i}.pdf"
        with fname.open("w") as fid:
            fid.write(f"test_{i} {i}\n")
            fid.write(f"test_{i} {i}\n")
            fid.write(f"test_{i} {i}\n")


def test_dest1():
    """test moving files to destination 1"""
    create_config()

    # create test files
    create_input_files()

    config = utils.load_config()

    dest = Path(config[0].path)

    # remove dest folder if exists
    if dest.exists():
        shutil.rmtree(dest)

    # check hasher
    hsh = utils.Hasher(dest)
    assert hsh.hashes == []

    src = SRC_DIR / "test_0.txt"

    nr = utils.add_file(src, dest)
    assert nr == 1

    # try to add same file again and check for assertion error
    with pytest.raises(AssertionError):
        utils.add_file(src, dest)


def test_dest2():
    """test adding files with prefix to destination 2"""
    config = utils.load_config()

    dest = Path(config[1].path)

    # remove dest folder if exists
    if dest.exists():
        shutil.rmtree(dest)

    # check hasher
    hsh = utils.Hasher(dest)
    assert hsh.hashes == []

    src = SRC_DIR / "test_0.txt"

    nr = utils.add_file(src, dest)
    assert nr == 1

    # try to add same file again and check for assertion error
    with pytest.raises(AssertionError):
        utils.add_file(src, dest)
