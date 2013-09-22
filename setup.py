#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://tyrant.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='tyrant',
    version='0.1.0',
    description='A CLI project management system.',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Taylor "Nekroze" Lawson',
    author_email='nekroze@eturnilnetwork.com',
    url='https://github.com/Nekroze/tyrant',
    packages=[
        'tyrant',
    ],
    package_dir={'tyrant': 'tyrant'},
    include_package_data=True,
    install_requires=[
    ],
    license='MIT',
    zip_safe=False,
    keywords='tyrant',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    tests_require=['pytest>=2.3.5']
)
