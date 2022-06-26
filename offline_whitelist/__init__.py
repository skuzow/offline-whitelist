import os
from typing import Optional

from mcdreforged.api.all import *

PLUGIN_METADATA = ServerInterface.get_instance().as_plugin_server_interface().get_self_metadata()


class Config(Serializable):
    whitelist_path: str = '/server/whitelist.json'


config: Optional[Config] = None
server_inst: PluginServerInterface
prefix = '!!offw'
plugin_name = PLUGIN_METADATA.name
version = PLUGIN_METADATA.version
help_message = '''
--- MCDR {1} v{2} ---
- Offline whitelist helper plugin
{0}
'''.strip().format(prefix, plugin_name, version)


def on_load(server: PluginServerInterface, old):
    global server_inst
    server_inst = server
    load_config(None)
    server.register_help_message(prefix, help_message)


def load_config(source: Optional[CommandSource]):
    global config, server_inst
    config_file_path = os.path.join('config', '{}.json'.format(PLUGIN_METADATA.id))
    config = server_inst.load_config_simple(config_file_path, in_data_folder=False, source_to_reply=source,
                                            echo_in_console=False, target_class=Config)
