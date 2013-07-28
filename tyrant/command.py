"""
To create a new command for **Tyrant** the ``Command`` class needs to be
subclassed for your command and override the ``Command.execute`` method to
provide your command execution.
"""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from argparse import ArgumentParser


class Command(ArgumentParser):
    """
    A command eases implementation of a **Tyrant** command.

    ``Command`` requires a command name to be used to call this command and a
    description that describes this commands usage.
    """
    def __init__(self, name, description):
        super(Command, self).__init__(description=description)
        self.name = name
        self.description = description
        self.commands = {}

    def __getitem__(self, key):
        return self.commands[key]

    def __setitem__(self, key, value):
        self.commands[key] = value

    def __len__(self):
        return len(self.commands)

    def __call__(self, args, command=None):
        if command is None:
            command = []
        if args and args[0] in self.commands:
            return self.commands[args[0]](args[1:], command + [self.name])
        self.prog = ' '.join(command)
        self.epilog = self.help()
        self.parse_args(args)

    def __delitem__(self, key):
        del self.commands[key]

    def __str__(self):
        return "{0}  {1}".format(self.name, self.description)

    def add_command(self, command):
        """
        Add a subcommand to this command. Must be an instance of ``Command``.
        """
        assert isinstance(command, Command)
        self.commands[command.name] = command

    def help(self):
        """Return subcommand help string."""
        output = ["Subcommands:"]
        for key in sorted(self.commands.keys()):
            output.append("  {0}".format(str(self.commands[key])))
        return '\n'.join(output)
