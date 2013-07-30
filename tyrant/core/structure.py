"""Basic structure containers."""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from tyrant.command import Command
from tyrant.tyrant import register_subcommand
from tyrant.config import Config, set_config
from six.moves import input


def blank_command(path, description):
    """
    Takes a list of command line args or space delimited string, the last of
    which is the new command name and a descriptiong and creates a basic
    command empty.
    """
    if not isinstance(path, (list, set, tuple)):
        path = path.split()
    register_subcommand(path[:-1], Command(path[-1], description))


blank_command("project", "Project management.")
blank_command("docs", "Documentation management.")
blank_command("test", "Unittest management.")
