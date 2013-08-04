"""
A configuration file accessor and editor interface.

This module stores the ``Config`` and ``ConfigPath`` globals.

``ConfigPath`` stores the path to the nearest backsearch found ``polis.yml``
file or None if it is not found.

``Config`` holds a ``ConfigAccessor`` object and will only load and save if
``ConfigPath`` is set. This object loads from a config file if found and will
provide a programatic representation of this config until the end of execution
at which time it will be re-serialized and saved to disk.
"""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
import re
import atexit
import yaml
import os
#pylint: disable=F0401
from six.moves import input
#pylint: enable=F0401


def backsearch(path=None, filename="polis.yml"):
    """
    Search from the given path backwards to find the first occurance of
    filename.

    ``path`` will default to the current working directory.
    """
    if path is None:
        path = os.getcwd()
    os.path.abspath(path)

    def recurse(path):
        """Recurse backwards one directory at a time and filecheck."""
        if not path or path in ('/', ''):
            return None

        pathfile = os.path.join(path, filename)
        if os.path.exists(pathfile):
            return pathfile
        else:
            return recurse(os.path.split(path)[0])
    return recurse(path)


_ConfigPath = {'path': backsearch()}
ConfigPath = lambda: _ConfigPath['path']


class ConfigDict(object):
    """
    A dictionary with attribute getters and setters that supports config
    descriptors that can describe how to ask for missing information.
    """
    def __init__(self):
        self.data = {}
        self.descriptors = {}

    def __getitem__(self, key):
        if key not in self.data and key in self.descriptors:
            message, default = self.descriptors[key]
            output = input("{0}\n[{1}]|>".format(message, default))
            output = output if output else default
            self.data[key] = output
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def get_data(self, key):
        """Get the stored data as a dictionary excluding descriptors."""
        data = {}
        for key, value in data.items():
            if isinstance(value, ConfigDict):
                data[key] = value.data()
            else:
                data[key] = value
        return data

    def add_descriptor(self, key, message, default=None):
        """
        Add an info descriptor that informs the Config how to get missing
        information.
        """
        if '.' in key:
            fields = key.split('.')
            key = fields[0]
            if key not in self.data:
                self.data[key] = ConfigDict()
            self.data[key].add_descriptor('.'.join(fields[1:]), message, default)
        else:
            self.descriptors[key] = (message, default if default else '')


class ConfigAccessor(ConfigDict):
    """
    Allows access to the configuration file if one is found.

    The config file holds a representation of the data stored in the
    ``ConfigAccessor`` and once loaded all top level data is accessable as a
    standard attribute and nesting values will store their data/dicts inside
    these attributes or other nested data/dicts themselves.
    """
    def __init__(self):
        super(ConfigAccessor, self).__init__()
        self.reload()

    def reload(self):
        """
        Reload the configuration file, any changes will be lost if used before
        saving.

        This will do nothing unless the ConfigPath global has been set and the
        file it points to exists. Even if the file exists ``Config`` will be
        cleared.
        """
        self.__dict__.clear()
        if ConfigPath() and os.path.exists(ConfigPath()):
            with open(ConfigPath()) as configfile:
                self.data.update(yaml.safe_load(configfile))

    def save(self):
        """
        Save the configuration file to disk for later loading. This gets
        automatically run at the end of a **Tyrant** execution.

        This will do nothing unless the ``ConfigPath`` global has been set.
        """
        if ConfigPath():
            with open(ConfigPath(), 'w') as configfile:
                yaml.dump(self.get_data(), configfile, default_flow_style=False)

    def get(self, path):
        """
        Recursively get the value of path delimited by '.' in a string.
        """
        keys = path.split('.')
        if not keys:
            return None

        data = self
        for key in keys:
            data = self[key]
        return data

    def set(self, path, value):
        """
        Recursively set the value of path delimited by '.' in a string.
        """
        keys = path.split('.')
        if not keys:
            return None

        data = self
        for key in keys[:-1]:
            data = self[key]
        data[-1] = value


Config = ConfigAccessor()
atexit.register(Config.save)


def set_config(path=None):
    """
    Set the config path and reload it.
    """
    if path is None:
        path = os.getcwd()
    _ConfigPath['path'] = os.path.join(os.path.abspath(path), "polis.yml")
    Config.reload()
