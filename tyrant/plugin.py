"""Plugin system for tyrant commands."""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from .config import ConfigPath, Config
from .tyrant import register_subcommand
from .command import ShellCommand, FileCommand
import yaml
import os
from glob import glob


def get_plugins(command=''):
    """Return a dictionary of command plugins and their corrosponding paths."""
    paths = [os.path.expandusr('~/.tyrant')]
    if ConfigPath:
        configdir = os.path.dirname(ConfigPath)
        paths.append(os.path.join(configdir, "tyrant"))

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
