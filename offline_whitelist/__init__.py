from mcdreforged.api.all import *
from offline_whitelist.commands import whitelist_add
from offline_whitelist.utils import load_config

PLUGIN_METADATA = ServerInterface.get_instance().as_plugin_server_interface().get_self_metadata()


prefix = '!!offw'
description = PLUGIN_METADATA.description
help_message = '''
--- MCDR {1} v{2} ---
- {3} plugin
{0} add §6[username] §rAdd offline player to whitelist
'''.strip().format(prefix, PLUGIN_METADATA.name, PLUGIN_METADATA.version, description)


def on_load(server: PluginServerInterface, old):
    load_config(None, server)
    server.register_help_message(prefix, description)
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
