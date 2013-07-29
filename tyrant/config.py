"""
A configuration file accessor and editor interface.
"""
from __future__ import print_function
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
import atexit
import yaml
import os


def backsearch(path, filename="polis.yml"):
    """
    Search from the given path backwards to find the first occurance of
    filename.
    """
    def recurse(pathlist):
        """Recurse backwards one directory at a time and filecheck."""
        if not pathlist or pathlist[0] in ('/', '') or ':/' in pathlist[0]:
            return None
        pathname = os.path.join(pathlist[0], filename)
        if os.path.exists(pathname):
            return pathname
        else:
            return recurse(pathlist[:-1])

    path = os.path.abspath(path)
    if not isinstance(path, (list, set, tuple)):
        path = os.path.split(path)
    return recurse(path)


class ConfigAccessor(object):
    """
    Allows access to the configuration file if one is found.

    The config file holds a representation of the data stored in the
    ``ConfigAccessor`` and once loaded all top level data is accessable as a
    standard attribute and nesting values will store their data/dicts inside
    these attributes or other nested data/dicts themselves.
    """
    def __init__(self):
        self.reload()

    def reload(self):
        """
        Reload the configuration file, any changes will be lost if used before
        saving.
        """
        filename = backsearch(os.getcwd())
        if filename is None:
            return None

        with open(filename) as configfile:
            self.__dict__.update = yaml.safe_load(configfile)

    @atexit.register
    def save(self):
        """
        Save the configuration file to disk for later loading. This gets
        automatically run at the end of a **Tyrant** execution.
        """
        filename = backsearch(os.getcwd())
        if filename is None:
            return None

        with open(filename, 'w') as configfile:
            yaml.dump(self.__dict__, configfile)

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


Config = ConfigAccessor()
