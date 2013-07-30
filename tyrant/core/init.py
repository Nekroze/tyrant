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
        self.add_argument('-e', '--email', action='append_const', const=str,
                          help="Contact email")
        self.add_argument('-l', '--license', action='append_const', const=str,
                          help="Project license")

    def execute(self, args):
        """Create a new config file from gathered information."""
        if os.path.exists(os.path.join(os.getcwd(), "polis.yml")):
            return None

        print("Creating a new polis.yml config file.")
        set_config()

        if args.author:
            Config.authors = args.author
        else:
            Config.ask_for('authors', "Author name(s)")
            Config.authors = [auth.strip() for auth in Config.authors.split(',')]

        if args.project:
            Config.project_name = args.project
        else:
            Config.ask_for('project_name', "Project name")

        if args.email:
            Config.email = args.email
        else:
            Config.ask_for("email", "Contact email address")

        if args.license:
            Config.license = args.license
        else:
            Config.ask_for("license", "Project license")

        print("Tyrant project initialized.")

register_subcommand([], InitCommand())
