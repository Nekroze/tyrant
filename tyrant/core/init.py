"""**Tyrant** config intialization."""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from tyrant.command import Command
from tyrant.tyrant import register_subcommand
from tyrant.config import Config, set_config, add_config_info
import os


add_config_info("project.name", "Project name")
add_config_info("project.description", "Project description")
add_config_info("project.url", "Project website")
add_config_info("project.source", "Project source directory")
add_config_info("project.license", "Project license")
add_config_info('developers.authors', "Author name(s)")
add_config_info("developers.lead", "Lead developer")
add_config_info("developers.email", "Contact email address")


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

        def ask_for(field, value=None):
            """Use the given value if defined otherwise ask."""
            if value:
                Config.set_data(field, value)
            else:
                Config.get(field)

        ask_for("project.name", args.project)
        ask_for("project.description", args.description)
        ask_for("project.url", args.url)
        ask_for("project.source", args.source)
        ask_for("project.license", args.license)
        ask_for('developers.authors', args.authors)
        ask_for("developers.email", args.email)

        authors = Config.get_data("developers.authors")
        if isinstance(authors, str):
            Config.set_data("developers.authors",
                            [auth.strip() for auth in authors.split(',')])
        ask_for("developers.lead", authors[0])

        print("Tyrant project initialized.")

register_subcommand([], InitCommand())
