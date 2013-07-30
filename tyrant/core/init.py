"""**Tyrant** config intialization."""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from tyrant.command import Command
from tyrant.tyrant import register_subcommand
from tyrant.config import Config, set_config
import os


class InitCommand(Command):
    """Initialize a **Tyrant** project."""
    def __init__(self):
        super(InitCommand, self).__init__("init", "Initialize tyrant control.",
                                          "tyrant")
        self.add_argument('-a', '--author', action='append_const', const=str,
                          help="Name of the project authors.")
        self.add_argument('-p', '--project', action='append_const', const=str,
                          help="Project name")

    def execute(self, args):
        """Create a new config file from gathered information."""
        if os.path.exists(os.path.join(os.getcwd(), "polis.yml")):
            return None

        print("Creating a new polis.yml config file.")
        set_config()

        if not args.author:
            Config.ask_for('author', "Author name(s)")
            Config.author = [auth.strip() for auth in Config.author.split(',')]
        else:
            Config.author = args.author

        if not args.project:
            Config.ask_for('project', "Project name")
        else:
            Config.project = args.project

        print("Tyrant project initialized.")

register_subcommand([], InitCommand())
