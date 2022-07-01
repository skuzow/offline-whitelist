import time

import offline_whitelist.utils as utils
from mcdreforged.api.all import *


def whitelist_add(source: PlayerCommandSource, username):
    config = utils.get_config()
    if utils.find_file(source, config.whitelist_path):
        whitelist_json = utils.load_file(source, config.whitelist_path)
        whitelist_json_filter = [obj for obj in whitelist_json if obj["name"] == username]
        offline_uuid = utils.generate_offline(source, username)
        server = source.get_server()
        # player inside whitelist
        len_whitelist_json_filter = len(whitelist_json_filter)
        if len_whitelist_json_filter > 0:
            # online or offline whitelisted
            if len_whitelist_json_filter == 1:
                # online whitelisted
                if not whitelist_json_filter[0]["uuid"] == offline_uuid:
                    for player in whitelist_json:
                        if player["name"] == username:
                            player["uuid"] = offline_uuid
                            break
                    utils.dump_file(source, config.whitelist_path, whitelist_json)
                    server.logger.info(f'Player {username} whitelisted online, changed uuid to offline one')
                    utils.send_info(source, f'Successfully added to whitelist: {username}')
                # offline whitelisted
                else:
                    utils.send_error(source, f'Player already whitelisted: {username}', None)
            # online & offline whitelisted
            else:
                # clear online whitelist & keep offline
                # server.execute(f'whitelist remove {username}') not valid if player is in user-cache, removes offline
                online_index = -1
                for index, player in enumerate(whitelist_json):
                    if player["name"] == username and not player["uuid"] == offline_uuid:
                        online_index = index
                        break
                whitelist_json.pop(online_index)
                utils.dump_file(source, config.whitelist_path, whitelist_json)
                server.logger.info(f'Player {username} whitelisted online & offline, removed online')
                utils.send_error(source, f'Player already whitelisted: {username}', None)
        # player not inside whitelist or username misspelled
        else:
            server.execute(f'whitelist add {username}')
            time.sleep(0.1)
            whitelist_json = utils.load_file(source, config.whitelist_path)
            found = False
            for player in whitelist_json:
                if player["name"] == username:
                    found = True
                    if not player["uuid"] == offline_uuid:
                        player["uuid"] = offline_uuid
                    else:
                        # /whitelist add uses offline uuid because player already entered the server
                        server.logger.info(f'Player {username} already in user-cache, whitelisted like usual')
                    break
            if found:
                utils.dump_file(source, config.whitelist_path, whitelist_json)
                utils.send_info(source, f'Successfully added to whitelist: {username}')
            else:
                # couldn't find nickname because bad written / only for online players
                server.execute(f'whitelist remove {username}')
                utils.send_error(source, f'Username is misspelled: {username}', None)
        server.execute('whitelist reload')


def reload_plugin(source: PlayerCommandSource):
    plugin_metadata = utils.get_plugin_metadata()
    if source.get_server().reload_plugin(plugin_metadata.id):
        utils.send_info(source, f'{plugin_metadata.name} plugin successfully reloaded!')
    else:
        utils.send_error(source, f'There was an error reloading {plugin_metadata.name} plugin', None)
