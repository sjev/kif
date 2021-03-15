# kif
file database assistant


**kif** is a simple tool that copies files from one location to another. While doing this, *kif* makes sure that 

* files are only added once to the destination folder ( the files are md5 hashed, these are stored in `.hashes` in destination directory)
* filenames get a prefix and a number
* filenames are tidied up (replace spces with underscores)
* automatically determine at which numbering to start


## How it works

example command

`kif add /src/dir /dest/dir --prefix='INR21' --start_nr=14 --ext='pdf'`

will copy files and prefix them starting with `INR21-0014` and following numbers.


## Installation

get the code and run 
`python setup.py install`
