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
        self.add_argument('--project', action='append_const', const=str,
                          help="Name of the project.")
        self.add_argument('--description', action='append_const', const=str,
                          help="Project description.")
        self.add_argument('--url', action='append_const', const=str,
                          help="Project website.")
        self.add_argument('--source', action='append_const', const=str,
                          help="Project source directory.")
        self.add_argument('--authors', action='append_const', const=str,
                          help="Name of the project authors.")
        self.add_argument('--email', action='append_const', const=str,
                          help="Contact email")
        self.add_argument('--license', action='append_const', const=str,
                          help="Project license")

    def execute(self, args):
        """Create a new config file from gathered information."""
        if os.path.exists(os.path.join(os.getcwd(), "polis.yml")):
            return None

        print("Creating a new polis.yml config file.")
        set_config()

        if args.project:
            Config.project_name = args.project
        else:
            Config.ask_for("project_name", "Project name")

        if args.description:
            Config.description = args.description
        else:
            Config.ask_for("description", "Project description")

        if args.url:
            Config.url = args.url
        else:
            Config.ask_for("url", "Project website")

        if args.source:
            Config.source_dir = args.source
        else:
            Config.ask_for("source", "Project source directory")

        if args.authors:
            Config.authors = args.authors
        else:
            Config.ask_for('authors', "Author name(s)")
            Config.authors = [auth.strip() for auth in Config.authors.split(',')]
        Config.author = Config.authors[0]

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
