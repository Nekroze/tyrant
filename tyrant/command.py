"""
To create a new command for **Tyrant** the ``Command`` class needs to be
subclassed for your command and override the ``Command.execute`` method to
provide your command execution.

The ``Command.__init__`` initialization should be overriden and provide
``ArgumentParser`` args.

The following is a reimplementation of the argparse docs example as a
**Tyrant** command::
   class MyCommand(Command):
       def __init__(self):
           super(MyCommand, self).__init__("mycommand", "Do stuff")
           self.add_argument('integers', metavar='N', type=int, nargs='+',
                            help='an integer for the accumulator')
           self.add_argument('--sum', dest='accumulate',
                            action='store_const', const=sum, default=max,
                            help='sum the integers (default: find the max)')

       def execute(self, args):
           print(args.accumulate(args.integers))
"""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter as Formatter


class Command(ArgumentParser):
    """
    A command eases implementation of a **Tyrant** command.

    ``Command`` requires a command name to be used to call this command and a
    description that describes this commands usage.

    In order to add a subcommand to any given command use ``+=`` on the parent
    command. For example::
       from tyrant.tyrant import Tyrant
       Tyrant += MyCommand()

    Now the mycommand can be called as a subcommand of the tyrant command line
    application like such: ``tyrant mycommand 1 2 3 4 --sum``.
    """
    def __init__(self, name, description, path=None):
        if path:
            path += ' ' + name
        super(Command, self).__init__(description=description,
                                      formatter_class=Formatter, prog=path)
        self.name = name
        self.description = description
        self.commands = {}

    def __getitem__(self, key):
        return self.commands[key]

    def __setitem__(self, key, value):
        self.commands[key] = value

    def __len__(self):
        return len(self.commands)

    def __call__(self, args):
        if args and args[0] in self.commands:
            return self.commands[args[0]](args[1:])
        self.epilog = self.__help__()
        self.execute(self.parse_args(args))

    def __delitem__(self, key):
        del self.commands[key]

    def __str__(self):
        return "{0}  {1}".format(self.name, self.description)

    def __help__(self):
        output = ["Subcommands:"]
        for key in sorted(self.commands.keys()):
            output.append("  {0}".format(str(self.commands[key])))
        return "\n".join(output)

    def __iadd__(self, command):
        assert isinstance(command, Command)
        self.commands[command.name] = command
        return self

    def execute(self, args):
        """
        Override this to execute a command. The args argument is a Namespace
        object that is delivered by ArgumentParser.parse_args method.
        """
        self.print_help()
