"""
To create a new command for **Tyrant** the ``Command`` class needs to be
subclassed for your command and override the ``Command.execute`` method to
provide your command execution.
"""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'


class Command(object):
    """
    A command eases implementation of a **Tyrant** command.

    ``Command`` requires a command name to be used to call this command and a
    description that describes this commands usage.
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.commands = {"help": self.help}

    def __getitem__(self, key):
        return self.commands[key]

    def __setitem__(self, key, value):
        self.commands[key] = value

    def __len__(self):
        return len(self.commands)

    def __call__(self, args):
        if args and args[0] in self.commands:
            return self.commands[args[0]](args[1:])
        self.execute(args)

    def __delitem__(self, key):
        del self.commands[key]

    def add_command(self, command):
        """
        Add a subcommand to this command. Must be an instance of ``Command``.
        """
        assert isinstance(command, Command)
        self.commands[command.name] = command

    def execute(self, args):
        """Execute this command, by default just runs help."""
        self.help(args)

    def help(self, args):
        """Display command usage help."""
        print(self.name, ':')
        print(self.description + '\n')

        for key in sorted(self.commands.keys()):
            print("{0} - {1}".format(key, self.commands[key].description))
