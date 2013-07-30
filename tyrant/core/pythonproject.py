"""Python project initialization."""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from tyrant.command import Command
from tyrant.tyrant import register_subcommand
from tyrant.config import Config, ConfigPath
import os

SetupBase = """#!/usr/bin/env python
import os
import sys

import {project_name}

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='{project_name}',
    version={project_name}.__version__,
    description='{project_description}',
    long_description=open('README.rst').read()
    author='{author}',
    author_email='{email}',
    url='{projecturl}',
    packages=[
        '{project_name}',
    ],
    package_dir={'{project_name }': '{project_name}'},
    include_package_data=True,
    install_requires=[
    ],
    license="{license}",
    zip_safe=False,
    keywords='{project_name}',
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


class InitCommand(Command):
    """Initialize a **Python** project."""
    def execute(self, args):
        """Create a new python setup.py."""
        Tyrant(['init'])
        print("Creating a python project setup.py")

        setupname = os.path.join(os.path.dirname(ConfigPath), "setup.py")
        with open(setupname, 'w') as setup:
            setup.write(SetupBase.format(**Config.__dict__))

        print("Python setup.py created")

register_subcommand('tyrant project init',
                    PythonCommand("python", "Initialize a python project.",
                                  "tyrant project init"))
