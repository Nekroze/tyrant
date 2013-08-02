"""Python project initialization."""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from tyrant.command import Command
from tyrant.tyrant import register_subcommand, Tyrant
from tyrant.config import Config, ConfigPath
import os

SetupBase = """#!/usr/bin/env python
import os
import sys

import {{project.source}}

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='{{project.name}}',
    version={{project.source}}.__version__,
    description='{{project.description}}',
    long_description=open('README.rst').read()
    author='{{developers.lead}}',
    author_email='{{developers.email}}',
    url='{{project.url}}',
    packages=['{{project.source}}'],
    package_dir={'{{project.source}}': '{{project.source}}'},
    include_package_data=True,
    install_requires=[
    ],
    license="{{project.license}}",
    zip_safe=False,
    keywords='{{project.name}}',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    tests_require=['nose>=1.3.0']
    test_suite='nose.collector',
)"""


class PythonInitCommand(Command):
    """Initialize a **Python** project."""
    def execute(self, args):
        """Create a new python setup.py."""
        Tyrant(['init'])
        print("Creating a python project setup.py")

        setupdir = os.path.dirname(ConfigPath())
        setupname = os.path.join(setupdir, "setup.py")
        with open(setupname, 'w') as setup:
            setup.write(Config.format(SetupBase))

        print("Python setup.py created")

register_subcommand('tyrant project init',
                    PythonInitCommand("python", "Initialize a python project.",
                                      "tyrant project init"))
