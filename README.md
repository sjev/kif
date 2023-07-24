# kif

![](misc/kif-picture.webp)

file database assistant

**kif** is a simple tool that copies files from one location to another. While doing this, `kif` makes sure that

- files are only added once to the destination folder ( the files are md5 hashed, these are stored in `.hashes` in destination directory)
- filenames get a prefix and a number
- filenames are tidied up (replace spces with underscores)
- automatically determine at which numbering to start

## How it works

- create example configuration with `kif init`
- configuration is saved in `~/.kif/kif.yaml` . Each entry has a name, destination and optional prefix.

`kif add DEST_NAME FILE` will copy `FILE` (or pattern) to destination name in `kif.yaml`

## Installation

get the code and run
`python setup.py install`
