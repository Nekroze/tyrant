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
           super(MyCommand, self).__init__("mycommand", "Do stuff", "tyrant")
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
from subprocess import check_call
from jinja2 import Template
import os
from .config import Config, ConfigPath


class Command(ArgumentParser):
    """
    A command eases implementation of a **Tyrant** command.

    ``Command`` requires a command name to be used to call this command and a
    description that describes this commands usage.

    The final argument to construct a ``Command`` is used in printing its usage
    help output to properly show the command path. If your command is under the
    root tyrant command line then path should be ``'tyrant'`` but for example
    if your command will be registered under ``tyrant docs`` path should be
    ``'tyrant docs'``. Getting this incorrect will not break anything, just
    make the command line help minorly incorrect.

    In order to add a subcommand to any given command use ``+=`` on the parent
    command. For example::
       from tyrant.tyrant import Tyrant
       Tyrant += MyCommand()

    Now the mycommand can be called as a subcommand of the tyrant command line
    application like such: ``tyrant mycommand 1 2 3 4 --sum``.
    """
    def __init__(self, name, description, path):
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

#pylint: disable=W0613
    def execute(self, args):
        """
        Override this to execute a command. The args argument is a Namespace
        object that is delivered by ArgumentParser.parse_args method.
        """
        self.print_help()
#pylint: disable=W0613


class ShellCommand(Command):
    """
    A command that executes one or many shell commands, typically loaded from a
    ``.typ`` plugin file.
    """
    def __init__(self, name, description, path, commands, pre=None, post=None,
                 **kwargs):
        super(ShellCommand, self).__init__(name, description, path)
        self.commands = commands
        self.pre = pre if pre else []
        self.post = post if post else []

    def execute(self, _):
        """Execute all shell commands after formatting them with the config."""
        from .tyrant import Tyrant
        for command in self.pre:
            Tyrant(command.split())

        for command in self.commands:
            check_call(Config.format(command))

        for command in self.post:
            Tyrant(command.split())


class FileCommand(Command):
    """
    A command that creates one or many formatted files on command, typically
    loaded from a ``.typ`` plugin file.
    """
    def __init__(self, name, description, path, files, pre=None, post=None,
                 **kwargs):
        super(FileCommand, self).__init__(name, description, path)
        self.files = {}
        for path, text in files.items():
            self.files[path] = Template(text)
        self.pre = pre if pre else []
        self.pre.insert(0, "init")
        self.post = post if post else []

    def execute(self, _):
        """Write all files to disk after formatting with config."""
        from .tyrant import Tyrant
        for command in self.pre:
            Tyrant(command.split())

        for filename, template in self.files:
            dirname = os.path.dirname(ConfigPath())
            path = os.path.join(dirname, filename)

            if not os.path.exists(dirname):
                os.makedirs(dirname)

            with open(path, 'w') as output:
                output.write(template.render(Config))

        for command in self.post:
            Tyrant(command.split())
