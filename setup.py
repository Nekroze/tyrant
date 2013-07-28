#!/usr/bin/python
import re
import os
import sys
import platform
from setuptools import setup


__version__ = '0.1.0'
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
SOURCE = 'tyrant'
TESTDIR = 'test'
PROJECTNAME = 'Tyrant'
PROJECTSITE = 'nekroze.eturnilnetwork.com'
PROJECTDESC = 'A project manager that can handle automatic building, unit testing and repository management in a simple CLI.'
PROJECTLICENSE = open("LICENSE").read()
PLATFORMS = ['*nix']

kwds = {}
kwds['version'] = __version__
kwds['description'] = PROJECTDESC
kwds['long_description'] = open('README.rst').read()
kwds['license'] = PROJECTLICENSE


setup(
    name=PROJECTNAME,
    author=__author__,
    author_email=__email__,
    url=PROJECTSITE,
    platforms=PLATFORMS,
    packages=[SOURCE],
    install_requires=['six'],
    entry_points={
        'console_scripts': [
            'tyrant = tyrant.tyrant:main',
            ]
    },
    classifiers=[
        # DEFINE YOURSELF
    ],
    **kwds
)
