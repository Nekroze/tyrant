"""Tyrant command interface."""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'


class Command(object):
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

    def execute(self, args):
        """Execute the given command."""
        if args:
            if args[0] in self.commands:
                self.commands[args[0]](args[1:])
            else:
                pass

    def help(self, args):
        """Display command usage help."""
        if args and args[0] in self.commands:
            print("{0} - {1}".format(args[0], self.commands[args[0]].__docs__))
        else:
            print(self.name, ':')
            print(self.description + '\n')

            for key in sorted(self.map.keys()):
                print("{0} - {1}".format(key, self.commands[key].__docs__))
