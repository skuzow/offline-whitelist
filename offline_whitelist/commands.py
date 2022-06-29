import time

import offline_whitelist.utils as utils
from mcdreforged.api.all import *


def whitelist_add(source: CommandSource, username):
    config = utils.get_config()
    if utils.find_file(source, config.whitelist_path):
        source.get_server().execute(f'whitelist add {username}')
        time.sleep(0.5)
        offline_uuid = utils.generate_offline(source, username)
        whitelist_json = utils.load_file(source, config.whitelist_path)
        # search player username inside whitelist & change uuid to offline one
        for player in whitelist_json:
            if player["name"] == username:
                if not player["uuid"] == offline_uuid:
                    player["uuid"] = offline_uuid
                    utils.dump_file(source, config.whitelist_path, whitelist_json)
                    source.get_server().execute('whitelist reload')
                    return utils.send_info(source, f'Successfully added to whitelist: {username}')
                else:
                    return utils.send_error(source, f'Player already whitelisted: {username}', None)
        # couldn't find nickname because bad written / only for online players
        utils.send_error(source, f'Username is misspelled: {username}', None)
        source.get_server().execute(f'whitelist remove {username}')
        source.get_server().execute('whitelist reload')


def reload_plugin(source: PlayerCommandSource):
    PLUGIN_METADATA = utils.get_plugin_metadata()
    if source.get_server().reload_plugin(PLUGIN_METADATA.id):
        utils.send_info(source, f'{PLUGIN_METADATA.name} plugin successfully reloaded!')
    else:
        utils.send_error(source, f'There was an error reloading {PLUGIN_METADATA.name} plugin', None)
