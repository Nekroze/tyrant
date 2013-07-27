"""Tyrant command interface."""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'


class Command(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.map = {"help": self.help}

    def execute(self, args):
        """Execute the given command."""
        self.map[args[0]](args[1:])

    def help(self, args):
        """Display command usage help."""
        if len(args) and args[0] in self.map:
            print("{0} - {1}".format(args[0], self.map[args[0]].__docs__))
        else:
            for key in sorted(self.map.keys()):
                print("{0} - {1}".format(key, self.map[key].__docs__))
