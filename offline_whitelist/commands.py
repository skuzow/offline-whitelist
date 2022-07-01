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
                player = whitelist_json_filter[0]
                if not player["uuid"] == offline_uuid:
                    # remove player with online uuid from whitelist & then change uuid to offline and add back
                    whitelist_json.remove(player)
                    player["uuid"] = offline_uuid
                    whitelist_json.append(player)
                    utils.dump_file(source, config.whitelist_path, whitelist_json)
                    utils.send_warning(source, f'Player already whitelisted online, changed online uuid to offline: {username}')
                # offline whitelisted
                else:
                    utils.send_error(source, f'Player already whitelisted: {username}', None)
            # online & offline whitelisted
            else:
                # clear online whitelist & keep offline
                # server.execute(f'whitelist remove {username}') not valid if player is in user-cache, removes offline
                online_player = [obj for obj in whitelist_json_filter if not obj["uuid"] == offline_uuid][0]
                whitelist_json.remove(online_player)
                utils.dump_file(source, config.whitelist_path, whitelist_json)
                utils.send_warning(source, f'Player already whitelisted online & offline, removed online: {username}')
        # player not inside whitelist or username misspelled
        else:
            server.execute(f'whitelist add {username}')
            time.sleep(0.1)
            whitelist_json_add = utils.load_file(source, config.whitelist_path)
            found = False
            for player in whitelist_json_add:
                if player["name"] == username:
                    found = True
                    if not player["uuid"] == offline_uuid:
                        player["uuid"] = offline_uuid
                    else:
                        # /whitelist add uses offline uuid because player already entered the server
                        server.logger.info(f'Player {username} already in user-cache, whitelisted like usual')
                    break
            if found:
                utils.dump_file(source, config.whitelist_path, whitelist_json_add)
                utils.send_info(source, f'Successfully added to whitelist: {username}')
            else:
                # couldn't find nickname because bad written / only for online players
                utils.dump_file(source, config.whitelist_path, whitelist_json)
                utils.send_error(source, f'Username is misspelled: {username}', None)
        server.execute('whitelist reload')


def whitelist_remove(source: PlayerCommandSource, username):
    config = utils.get_config()
    if utils.find_file(source, config.whitelist_path):
        whitelist_json = utils.load_file(source, config.whitelist_path)
        whitelist_json_filter = [obj for obj in whitelist_json if obj["name"] == username]
        server = source.get_server()
        # player inside whitelist
        len_whitelist_json_filter = len(whitelist_json_filter)
        if len_whitelist_json_filter > 0:
            for player in whitelist_json_filter:
                if player["name"] == username:
                    whitelist_json.remove(player)
            utils.dump_file(source, config.whitelist_path, whitelist_json)
            utils.send_info(source, f'Successfully removed from whitelist: {username}')
            server.execute('whitelist reload')
        # player not inside whitelist
        else:
            utils.send_error(source, f'Player not whitelisted: {username}', None)


def reload_plugin(source: PlayerCommandSource):
    plugin_metadata = utils.get_plugin_metadata()
    if source.get_server().reload_plugin(plugin_metadata.id):
        utils.send_info(source, f'{plugin_metadata.name} plugin successfully reloaded!')
    else:
        utils.send_error(source, f'There was an error reloading {plugin_metadata.name} plugin', None)
