"""
The **Tyrant** command line interface and Command accessor.

In order to add a command to tyrant import ``Tyrant`` from this module and add
a command to it inplace.
"""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from .command import Command
from .config import Config
from importlib import import_module
import sys


Tyrant = Command(
    "tyrant",
    """Tyrant A project manager that can handle automatic building, unit
    testing and repository management in a simple CLI.
    """, None)


def register_subcommand(path, command):
    """
    Register a subcommand to any currently registered **Tyrant** command.

    The ``path`` argument should either be a list or space delimited string of
    command names the last of which should be the command that you want to
    register the new subcommand under. An empty list will place the command as
    a subcommand of the tyrant command line itself. The first argument does not
    need to be 'tyrant' but must be something that is registered already under
    the ``Tyrant`` ``Command`` object.

    The ``command`` argument must be a subclass of ``tyrant.command.Command``.
    """
    assert isinstance(command, Command)
    if not isinstance(path, (list, set, tuple)):
        path = path.split()
    if path and path[0] == 'tyrant':
        path = path[1:]

    current = Tyrant
    for name in path:
        if name in current.commands:
            current = current.commands[name]
        else:
            assert False, "{0} does not contain {1}".format(current.name, name)
    current += command


def load_plugins():
    """Load any plugins listed in ``Config``."""
    plugins = Config.get_data("plugins", [])
    for name in plugins:
        import_module(name)


Prerun = [load_plugins]


def main():
    """Main entry point."""
    args = sys.argv
    for func in Prerun:
        func()
    Tyrant(args[1:])


from . import core
