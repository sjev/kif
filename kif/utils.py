#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utility functions
"""
from typing import Optional
import hashlib
import logging
import string
from pathlib import Path


import yaml  # type: ignore


def clean_str(s):
    """clean invalid characters"""

    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return "".join(c for c in s if c in valid_chars)


def configLogging(
    logFile=None, fileLevel=logging.DEBUG, consoleLevel=logging.INFO, filemode="w"
):
    """configure logging to console and file, returns root logger"""

    fmt_file = "%(asctime)s  %(levelname)s [%(filename)s-%(lineno)d] - %(message)s"
    fmt_console = "%(levelname)s - %(message)s"

    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    # Remove existing logging handlers
    log.handlers = []
    assert not log.hasHandlers(), "Deleting logging handlers failed"

    # file logging if requested
    if logFile is not None:
        file = logging.FileHandler(filename=logFile, mode=filemode)
        file.setLevel(fileLevel)
        formatter = logging.Formatter(fmt_file, datefmt="%Y-%m-%d %H:%M:%S")
        file.setFormatter(formatter)
        log.addHandler(file)

    console = logging.StreamHandler()
    console.setLevel(consoleLevel)
    formatter = logging.Formatter(fmt_console, datefmt="%H:%M:%S")
    console.setFormatter(formatter)
    log.addHandler(console)

    log.debug(f"Set up logging to {logFile}")
    return log


def get_next_id(path: Path, prefix: str, n_digits=4) -> int:
    """
    get next available number

    Parameters
    ----------
    path : Path
        path to find files
    prefix : str
        filename prefix like INR

    Returns
    -------
    int : next nuber

    """
    logging.debug("Finding next id")
    files = path.glob(prefix + "*")

    max_idx = 0

    for f in files:
        logging.debug(f.stem)
        s = f.stem.split("-")[1][:n_digits]
        i = int(s)
        if i > max_idx:
            max_idx = i

    return max_idx + 1


def md5(path):
    """calculate MD5 checksum may provide a dir or a file"""

    def hash_file(p):
        with p.open("rb") as fid:
            hasher = hashlib.md5()
            hasher.update(fid.read())
            hsh = hasher.hexdigest()

        return hsh

    if path.is_dir():
        hashes = []
        for f in path.glob("*"):
            if f.is_file():
                hashes.append(hash_file(f))
        return hashes

    elif path.is_file():
        return [hash_file(path)]

    else:
        raise ValueError("provide path to file or dir")


class Hasher:
    """class to manage file hashes
    hashes are stored as  hash per line

    """

    def __init__(self, path):
        self.data_file = path / ".hashes"

        if self.data_file.exists():
            with self.data_file.open("r") as fid:
                lines = fid.readlines()

            self.hashes = [line.strip() for line in lines]
        else:
            self.hashes = []

    def add(self, path):
        """add hashes of a file or path"""

        hashes = md5(path)
        with self.data_file.open("a") as f:
            for hsh in hashes:
                f.write(hsh + "\n")
                self.hashes.append(hsh)

    def delete_hashes(self):
        """clear all hashes"""
        self.hashes = []
        if self.data_file.exists():
            self.data_file.unlink()

    def is_present(self, path):
        """check if a file is present in hashes"""
        hsh = md5(path)[0]
        return hsh in self.hashes


def get_config_path() -> Path:
    """get config file path"""
    return Path.home() / ".kif" / "kif.yaml"


def load_config(path: Optional[Path] = None) -> list:
    """load config file"""

    if path is None:
        # load from user home dir
        path = get_config_path()

    if not path.exists():
        raise FileNotFoundError(f"Config file {path} not found")

    with path.open("r") as fid:
        data = yaml.load(fid, Loader=yaml.FullLoader)

    return data


def create_example_config(path: Optional[Path] = None):
    """create example yaml config file"""

    if path is None:
        # create in user home dir
        path = get_config_path()

    # don't overwrite existing file
    if path.exists():
        raise FileExistsError(f"Config file {path} already exists")

    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    item1 = {"name": "dest1", "path": "/tmp/kif/data", "prefix": None}
    item2 = {"name": "dest2", "path": "/tmp/kif/data2", "prefix": "INR"}

    data = [item1, item2]

    print(f"Creating config file {path}")

    with path.open("w") as fid:
        yaml.dump(data, fid)
