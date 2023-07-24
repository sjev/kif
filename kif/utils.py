#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utility functions
"""
import hashlib
import logging
import shutil
import string
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

import yaml  # type: ignore

log = logging.getLogger("utils")


@dataclass
class Destination:
    """destination folder config"""

    name: str
    path: str
    prefix: str = ""


def clean_str(s):
    """clean invalid characters"""

    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return "".join(c for c in s if c in valid_chars)


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


def md5(path: Path):
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

    def __init__(self, path: Path):
        self.data_file = path / ".hashes"

        if self.data_file.exists():
            with self.data_file.open("r") as fid:
                lines = fid.readlines()

            self.hashes = [line.strip() for line in lines]
        else:
            self.hashes = []

    def add(self, path: Path):
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

    def is_present(self, path: Path):
        """check if a file is present in hashes"""

        hsh = md5(path)[0]
        present = hsh in self.hashes
        log.debug(f"Checking {path} in {self.data_file}: {present}")
        return present


def get_config_path() -> Path:
    """get config file path"""
    return Path.home() / ".kif" / "kif.yaml"


def load_config(path: Optional[Path] = None) -> dict:
    """load config file"""

    if path is None:
        # load from user home dir
        path = get_config_path()

    if not path.exists():
        raise FileNotFoundError(f"Config file {path} not found")

    with path.open("r") as fid:
        data = yaml.load(fid, Loader=yaml.FullLoader)

    return {k: Destination(name=k, **v) for k, v in data.items()}


def create_example_config(path: Optional[Path] = None) -> Path:
    """create example yaml config file"""

    if path is None:
        # create in user home dir
        path = get_config_path()

    # don't overwrite existing file
    if path.exists():
        raise FileExistsError(f"Config file {path} already exists")

    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    item1 = {"path": "/tmp/kif/data"}
    item2 = {"path": "/tmp/kif/data2", "prefix": "INR"}

    data = {"dest1": item1, "dest2": item2}

    log.info(f"Creating config file {path}")

    with path.open("w") as fid:
        yaml.dump(data, fid)

    return path


def add_file(
    src: Path, dest: Path, prefix: str = "", start_nr: Optional[int] = None
) -> int:
    """add a file to a destination folder, returns number id of file"""

    log.info(f"Adding {src} to {dest}")

    # create destination folder if not exists
    dest.mkdir(parents=True, exist_ok=True)

    assert src.exists(), "File not found"

    hsh = Hasher(dest)
    assert not hsh.is_present(src), f"File {src} already in database."

    if start_nr is None:
        next_id = get_next_id(dest, prefix)
    else:
        next_id = start_nr

    # generate prefix
    if prefix:
        dest_prefix = prefix + "-%04d_" % next_id
    else:
        dest_prefix = "%04d_" % next_id

    fname = dest_prefix + clean_str(src.stem.replace(" ", "_")) + src.suffix.lower()
    dest_file = dest / fname

    shutil.copy(src, dest_file)
    hsh.add(dest_file)

    return next_id
