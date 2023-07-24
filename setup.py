#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
import kif

requirements = ['click']

setup(
    name='kif',
    version=kif.__version__,
    description="Assistant for copying files to a database",
    packages=find_packages(include=['kif']),
    author="Jev Kuznetsov",
    url="https://github.com/sjev/kif",
    install_requires=requirements,
    license='BSD',
    entry_points={
        'console_scripts': ['kif=kif.cli:cli'], }
)
