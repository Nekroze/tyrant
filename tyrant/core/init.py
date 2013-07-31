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

        def ask_for(field, description, value=None):
            """Ask for or use the given data."""
            if value:
                Config.set_data(field, description)
            else:
                Config.ask_for(field, description)

        ask_for("project.name", "Project name", args.project)
        ask_for("project.description", "Project description", args.description)
        ask_for("project.url", "Project website", args.url)
        ask_for("project.source", "Project source directory", args.source)
        ask_for('developers.authors', "Author name(s)", args.authors)
        ask_for("developers.email", "Contact email address", args.email)
        ask_for("project.license", "Project license", args.license)

        authors = Config.get_data("developers.authors")
        if isinstance(authors, str):
            authors = [auth.strip() for auth in
                       authors.split(',')]
            Config.set_data("developers.authors", authors)
        Config.set_data("developers.lead", authors[0])

        print("Tyrant project initialized.")

register_subcommand([], InitCommand())
