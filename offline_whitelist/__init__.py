from mcdreforged.api.all import *
from offline_whitelist.commands import whitelist_add
from offline_whitelist.utils import load_config

PLUGIN_METADATA = ServerInterface.get_instance().as_plugin_server_interface().get_self_metadata()


prefix = '!!offw'
plugin_name = PLUGIN_METADATA.name
version = PLUGIN_METADATA.version
help_message = '''
--- MCDR {1} v{2} ---
- Offline whitelist helper plugin
{0} add §6[username] §rAdd offline player to whitelist
'''.strip().format(prefix, plugin_name, version)


def on_load(server: PluginServerInterface, old):
    load_config(None, server)
    server.register_help_message(prefix, PLUGIN_METADATA.description)
    register_commands(server)


def register_commands(server: PluginServerInterface):
    def get_username(callback):
        return Text('username').runs(callback)
    server.register_command(
        Literal(prefix).
        runs(lambda src: src.reply(help_message)).
        on_error(UnknownArgument, lambda src: src.reply(f'Parameter error! Please enter §7{prefix}§r to get plugin help'), handled=True).
        then(Literal('add').then(get_username(lambda src, ctx: whitelist_add(src, ctx['username']))))
    )
