"""
The **Tyrant** command line interface and Command accessor.

In order to add a command to tyrant import ``Tyrant`` from this module and add
a command to it inplace.
"""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from .command import Command, ShellCommand, FileCommand
from .config import Config, ConfigPath
from importlib import import_module
import sys
import yaml
import os
from glob import glob


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


def get_plugins(command=''):
    """
    Return a dictionary of command plugins and their corrosponding paths.

    This will first look in the user home directory, then the current tyrant
    project directory (containing 'polis.yml') and finally in the current
    directory for a '.tyrant' folder containing ``'*.typ'`` files.
    """
    paths = [os.path.expanduser('~/.tyrant')]
    if ConfigPath():
        configdir = os.path.dirname(ConfigPath())
        paths.append(os.path.join(configdir, "tyrant"))

    current = os.path.join(os.getcwd(), ".tyrant")
    if os.path.exists(current):
        paths.append(current)

    plugins = {}
    for path in paths:
        if not os.path.exists(path):
            continue
        for filename in glob(os.path.join(path, '{0}*.typ'.format(command))):
            plugins[os.path.split(filename)[1][:-4]] = filename
    return plugins


CommandMap = {"shell": ShellCommand, "file": FileCommand}


def load_plugin(command, path):
    """Load the given command plugin from the path."""
    pdict = yaml.safe_load(path)

    if "descriptors" in pdict:
        descriptors = pdict["descriptors"]
        if isinstance(descriptors, (list, set, tuple)):
            for descriptor in descriptors:
                Config.add_descriptor(*descriptor)
        elif isinstance(descriptors, str):
            Config.add_descriptor(*descriptors)

    commandclass = CommandMap[pdict["type"]]
    register_subcommand(command, commandclass(path=command, **pdict))


def load_all_plugins():
    """Load all plugins that ``get_plugins`` can find."""
    for command, path in get_plugins().items():
        load_plugin(command, path)


Prerun = [load_all_plugins]


def main():
    """Main entry point."""
    args = sys.argv
    for func in Prerun:
        func()
    Tyrant(args[1:])


from . import init
