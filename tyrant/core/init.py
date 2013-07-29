"""**Tyrant** config intialization."""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from tyrant.command import Command
from tyrant.tyrant import register_subcommand
from tyrant.config import Config, set_config
#pylint: disable=F0401
from six.moves import input
#pylint: enable=F0401


class InitCommand(Command):
    """Initialize a **Tyrant** project."""
    def __init__(self):
        super(InitCommand, self).__init__("init", "Initialize a new project.")
        self.add_argument('-a', '--author', action='append_const', const=str,
                          help="Name of the project authors.")
        self.add_argument('-p', '--project', action='append_const', const=str,
                          help="Project name")

    def execute(self, args):
        """Create a new config file from gathered information."""
        print("Creating a new polis.yml config file.")
        set_config()

        if not args.author:
            args.author = input("Author name(s):")
        args.author = [auth.strip() for auth in args.author.split(',')]
        Config.author = args.author

        if not args.project:
            args.project = input("Project name:")
        Config.project = args.project

        print("Tyrant project initialized.")

register_subcommand([], InitCommand())
