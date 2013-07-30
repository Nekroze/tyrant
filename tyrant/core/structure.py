"""Basic structure containers."""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from tyrant.command import Command
from tyrant.tyrant import register_subcommand
from tyrant.config import Config, set_config


def blank_command(path, description):
    """
    Takes a list of command line args or space delimited string, the last of
    which is the new command name and a descriptiong and creates a basic
    command empty.
    """
    if not isinstance(path, (list, set, tuple)):
        path = path.split()
    if path and path[0] != 'tyrant':
        path.insert(0, 'tyrant')
    register_subcommand(path[:-1], Command(path[-1], description,
                                           ' '.join(path[:-1])))


blank_command("project", "Project management.")
blank_command("project init", "Project initialization.")
blank_command("docs", "Documentation management.")
blank_command("docs init", "Documentation initialization.")
blank_command("test", "Unittest management.")
blank_command("test init", "Unittest initialization.")
