#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main cli application

@author: jev
"""
import logging
from pathlib import Path

import click
from click import echo

import kif  # app version is defined in __init__.py
import kif.utils as utils

logging.basicConfig(level=logging.INFO)


log = logging.getLogger("cli")


@click.group()
@click.version_option(version=kif.__version__)
def cli():
    pass


@cli.command()
def config():
    """show configuraton"""
    cfg = utils.load_config()
    print(cfg)

    echo("name\tpath\tprefix")
    echo("------------------------------------------")
    for _, dest in cfg.items():
        echo(f"{dest.name}\t{dest.path}\tprefix={dest.prefix}")


@cli.command()
@click.argument("name")
def ls(name: str):
    """list files in destination folder"""

    cfg = utils.load_config()

    names = cfg.keys()
    if name not in names:
        echo(f"Destination {name} not found.")
        echo("Available destinations:")
        echo("\n".join(names))
        return

    dest = cfg[name]

    echo(f"Listing files in {dest.path}")

    files = [f for f in Path(dest.path).glob("*")]
    files.sort()

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
@click.argument("dest_name")
@click.argument("src", nargs=-1)
@click.option(
    "--start_nr", default=None, help="starting nubering at this number", type=int
)
@click.option("--debug", is_flag=True, help="debug mode")
def add_files(dest_name: str, src: tuple, start_nr, debug: bool):
    """add files to a destination folder src can be a file or glob pattern"""
    if debug:
        log.setLevel(logging.DEBUG)

    cfg = utils.load_config()
    if dest_name not in cfg:
        echo(f"Destination {dest_name} not found.")
        echo("Available destinations:")
        echo("\n".join(cfg.keys()))
        return

    log.debug(f"Adding file(s) {src} to {dest_name}")
    dest = Path(cfg[dest_name].path)

    for fname in src:
        try:
            src_file = Path(fname)
            assert src_file.exists()
            utils.add_file(src_file, dest, start_nr=start_nr)

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
