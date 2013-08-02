"""Plugin system for tyrant commands."""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from .config import ConfigPath
from .tyrant import register_subcommand
from .command import ShellCommand, FileCommand
import yaml
import os
from glob import glob


def get_plugins(self, command=''):
    """Return a dictionary of command plugins and their corrosponding paths."""
    paths = ["~/.tyrant/"]
    if ConfigPath:
        configdir = os.path.dirname(ConfigPath)
        paths.append(os.path.join(configdir, "tyrant"))

    tyrants = {}
    for path in paths:
        if not os.path.exists(path):
            continue
        for filename in glob(os.path.join(path, '{0}*.typ'.format(pattern))):
            plugins[os.path.split(path)[1][:-4]] = path
    return tyrants


CommandMap = {"shell": ShellCommand, "file": FileCommand}


def load_plugin(command, path):
    """Load the given command plugin from the path."""
    pdict = yaml.safe_load(path)
    register_subcommand(command, CommandMap[pdict["type"]](pdict))


def load_all_plugins():
    """Load all plugins that ``get_plugins`` can find."""
    for command, path in get_plugins().items():
        load_plugin(command, path)
