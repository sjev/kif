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

utils.configLogging(consoleLevel=logging.DEBUG)


log = logging.getLogger('cli')


@click.group()
@click.version_option(version=kif.__version__)
def cli():
    pass


@click.command('add')
@click.argument('src')
@click.argument('dest')
@click.option('--prefix', default='INR21', help='Filename prefix, will be automatically added before number')
@click.option('--ext', default='pdf', help='filename extension')
@click.option('--start_nr', default=None, help='starting nubering at this number', type=int)
def add_files(src, dest, prefix, ext, start_nr):
    """ add files to a destination folder """

    log.debug(
        f'Adding files from {src} to {dest} with extension {ext}, prefix: {prefix}, start_nr: {start_nr}')

    src = Path(src)
    dest = Path(dest)

    files = [f for f in src.glob('*') if f.suffix.lower()[1:] == ext]

    log.info('Found %i files' % len(files))

    hsh = utils.Hasher(dest)

    if start_nr is None:
        next_id = utils.get_next_id(dest, prefix)
    else:
        next_id = start_nr

    log.info('Next number: %i' % next_id)

    for src_file in files:
        try:
            assert src_file.exists(), 'File not found'
            assert hsh.is_present(
                src_file) == False, f'{src_file} is already in database.'

            # generate prefix
            dest_prefix = prefix+'-%04d_' % next_id
            next_id += 1

            dest_file = dest / \
                (dest_prefix + utils.clean_str(src_file.stem.replace(' ','_')) + src_file.suffix.lower())

            log.info(f'{src_file.as_posix()} -> {dest_file.as_posix()}')
            shutil.copy(src_file, dest_file)
            hsh.add(dest_file)

        except AssertionError as e:
            echo(e)

# -----------------------------------------


cli.add_command(add_files)
