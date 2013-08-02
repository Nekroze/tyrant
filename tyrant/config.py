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
ConfigPath = lambda : _ConfigPath['path']
ConfigInfo = {}


class ConfigDict(dict):
    """A dictionary with attribute getters and setters."""
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        return self[key] = value


class ConfigAccessor(object):
    """
    Allows access to the configuration file if one is found.

    The config file holds a representation of the data stored in the
    ``ConfigAccessor`` and once loaded all top level data is accessable as a
    standard attribute and nesting values will store their data/dicts inside
    these attributes or other nested data/dicts themselves.
    """
    def __init__(self):
        self.__dict__ = ConfigDict()
        self.reload()

    def get(self, key):
        """
        Return the given key if it exists otherwise use the ``ConfigInfo`` to
        find out how to ask for the info.

        ``key`` may be a '.' delmited string for recursion.
        """
        output = self.get_data(key)
        if output is not None:
            return output

        message, default, post = ConfigInfo[key]
        output = input("{0}\n[{1}]|>".format(message, default))
        output = post(output) if output else default
        return self.set_data(key, output)

    def ask_for(self, key, message=None):
        """
        Return key if it exists and return it otherwise ask the user for input
        with the given message.

        The ``key`` argument is used to get and if required set the data from
        the ``get_data`` and ``set_data`` methods respectively.

        ``message`` will be printed before asking for input on the next line.
        """
        if message is None:
            return self.get(key)

        output = self.get_data(key)
        if output is not None:
            return output

        output = input(message + "\n|>")
        return self.set_data(key, output, field)

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
                self.__dict__.update(yaml.safe_load(configfile))

    def save(self):
        """
        Save the configuration file to disk for later loading. This gets
        automatically run at the end of a **Tyrant** execution.

        This will do nothing unless the ``ConfigPath`` global has been set.
        """
        if ConfigPath():
            with open(ConfigPath(), 'w') as configfile:
                yaml.dump(self.__dict__, configfile, default_flow_style=False)

    def get_data(self, field, default=None):
        """
        Retreive nested data or return default if it does not exist.

        The field argument can be a '.' delimited string of namespaces as such
        or a list of namespaces. Each will be looked for, and if needed
        entered, until the end of the list or a namespace is missing at which
        point it will either return the datapoint that has been reached or the
        default argument. Respectively.
        """
        if not isinstance(field, (list, set, tuple)):
            field = field.split('.')

        data = self.__dict__
        for slot in field:
            if slot in data:
                data = data[slot]
            else:
                return default
        return data

    def set_data(self, key, value):
        """
        Set the given field to the specified key value pair.

        The key argument can be a '.' delimited string of namespaces as such
        or a list of namespaces. Each will be looked for, and if needed
        entered, until the end of the list at which point it will set
        the value at the final field.

        Any missing fields will be created automatically.
        """
        if key is None or key == '':
            fields = []
        elif not isinstance(key, (list, set, tuple)):
            fields = fields.split('.')

        data = self.__dict__
        for slot in fields[:-1]:
            if slot not in data:
                data[slot] = ConfigDict()
            data = data[slot]
        data[fields[-1]] = value
        return value


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
