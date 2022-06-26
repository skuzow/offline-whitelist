import time

from mcdreforged.api.all import *
from offline_whitelist.utils import get_config, find_file, generate_offline, load_file, dump_file, send_info, send_error


def whitelist_add(source: CommandSource, username):
    config = get_config()
    if find_file(source, config.whitelist_path):
        source.get_server().execute(f'whitelist add {username}')
        time.sleep(0.5)
        offline_uuid = generate_offline(source, username)
        whitelist_json = load_file(source, config.whitelist_path)
        # search player username inside whitelist & change uuid to offline one
        for player in whitelist_json:
            if player["name"] == username:
                if not player["uuid"] == offline_uuid:
                    player["uuid"] = offline_uuid
                    dump_file(source, config.whitelist_path, whitelist_json)
                    source.get_server().execute('whitelist reload')
                    return send_info(source, f'Successfully added to whitelist: {username}')
                else:
                    return send_error(source, f'Player already whitelisted: {username}', None)
        # couldn't find nickname because bad written / only for online players
        send_error(source, f'Username is misspelled: {username}', None)
        source.get_server().execute(f'whitelist remove {username}')
        source.get_server().execute('whitelist reload')
