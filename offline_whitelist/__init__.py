import offline_whitelist.commands as commands
import offline_whitelist.utils as utils
from mcdreforged.api.all import *

PLUGIN_METADATA = ServerInterface.get_instance().as_plugin_server_interface().get_self_metadata()


prefix = '!!offw'
description = PLUGIN_METADATA.description
help_message = '''
--- MCDR {1} v{2} ---
- {3} plugin
§7{0} add §6[username] §rAdd offline player to whitelist
§7{0} reload §rReloads plugin itself
'''.strip().format(prefix, PLUGIN_METADATA.name, PLUGIN_METADATA.version, description)


def on_load(server: PluginServerInterface, old):
    utils.load_config(None, server)
    server.register_help_message(prefix, description)
    register_commands(server)


def register_commands(server: PluginServerInterface):
    def get_username(callback):
        return Text('username').runs(callback)
    server.register_command(
        Literal(prefix).
        requires(lambda src: src.has_permission(utils.get_config().minimum_permission_level)).
        on_error(RequirementNotMet, lambda src: src.reply(RText('Insufficient permission!', color=RColor.red)), handled=True).
        on_error(UnknownArgument, lambda src: src.reply(f'Parameter error! Please enter §7{prefix}§r to get plugin help'), handled=True).
        runs(lambda src: src.reply(help_message)).
        then(Literal('add').then(get_username(lambda src, ctx: commands.whitelist_add(src, ctx['username'])))).
        then(Literal('reload').runs(commands.reload_plugin))
    )
