"""The **Tyrant** command line interface."""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from .command import Command
import sys


Tyrant = Command(
    "tyrant",
    """
    Tyrant A project manager that can handle automatic building, unit
    testing and repository management in a simple CLI.
    """)


def main():
    """Main entry point."""
    args = sys.argv
    Tyrant(args[1:])
