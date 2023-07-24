#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main cli application

@author: jev
"""
import shutil
from click import echo
import click
from pathlib import Path
import kif  # app version is defined in __init__.py
import logging
import kif.utils as utils

logging.basicConfig(level=logging.DEBUG)


log = logging.getLogger("cli")


@click.group()
@click.version_option(version=kif.__version__)
def cli():
    pass


@cli.command()
def config():
    """show configuraton"""
    cfg = utils.load_config()

    echo("name\tpath\tprefix")
    echo("------------------------------------------")
    for dest in cfg:
        echo(f"{dest.name}\t{dest.path}\tprefix={dest.prefix}")


@cli.command()
@click.argument("name")
def ls(name: str):
    """list files in destination folder"""

    cfg = utils.load_config()

    names = [d.name for d in cfg]
    if name not in names:
        echo(f"Destination {name} not found.")
        echo("Available destinations:")
        echo("\n".join(names))
        return

    dest = [d for d in cfg if d.name == name][0]

    echo(f"Listing files in {dest.path}")

    files = [f for f in Path(dest.path).glob("*")]

    for f in files:
        echo(f.name)


@cli.command()
def init():
    """create sample config file"""
    try:
        p = utils.create_example_config()
        echo(f"Created {p}")
    except FileExistsError as e:
        echo(e)


@click.command("add")
@click.argument("src")
@click.argument("dest_name")
@click.option(
    "--start_nr", default=None, help="starting nubering at this number", type=int
)
def add_files(src: str, dest_name: str, start_nr):
    """add files to a destination folder src can be a file or glob pattern"""

    cfg = utils.load_config()

    log.debug(f"Adding file(s) {src} to {dest}")
    dest = Path(dest)

    if "*" in src:  # working with glob
        files = [f for f in Path.glob(src)]
        log.info("Found %i files" % len(files))
    else:
        files = [Path(src)]

    for src_file in files:
        try:
            print(src_file)

        except AssertionError as e:
            log.warning(e)


@click.command()
@click.argument("dest")
def rehash(dest):
    """rehash files in destination directory"""

    dest = Path(dest)
    hsh = utils.Hasher(dest)
    hsh.delete_hashes()
    hsh.add(dest)


# -----------------------------------------


cli.add_command(add_files)
cli.add_command(rehash)
