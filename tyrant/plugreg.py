"""Plugin registry."""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'


PLUGINS = {}


def register_plugin(plugin):
    """Register a plugin."""
    PLUGINS[plugin.codename] = plugin
