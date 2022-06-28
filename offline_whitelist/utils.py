import hashlib
import json
import os
from typing import Optional

from mcdreforged.api.all import *

PLUGIN_METADATA = ServerInterface.get_instance().as_plugin_server_interface().get_self_metadata()


class Config(Serializable):
    whitelist_path: str = './server/whitelist.json'


config: Optional[Config] = None


def generate_offline(source: CommandSource, username):
    # extracted from the java code:
    # new GameProfile(UUID.nameUUIDFromBytes(("OfflinePlayer:" + name).getBytes(Charsets.UTF_8)), name));
    string = "OfflinePlayer:" + username
    hash = hashlib.md5(string.encode('utf-8')).digest()
    byte_array = [byte for byte in hash]
    byte_array[6] = hash[6] & 0x0f | 0x30
    byte_array[8] = hash[8] & 0x3f | 0x80
    offline_uuid = __add_stripes(bytes(byte_array).hex())
    source.get_server().logger.info(f'Username converted: {username} -> uuid: {offline_uuid}')
    return offline_uuid


def __add_stripes(uuid):
    return uuid[:8] + '-' + uuid[8:12] + '-' + uuid[12:16] + '-' + uuid[16:20] + '-' + uuid[20:]


def check_permission(source: CommandSource, min_permission_level):
    if source.has_permission_higher_than(min_permission_level - 1):
        return True
    else:
        source.reply('You don\'t permission to run this command')
        return False


def load_config(source: Optional[CommandSource], server: PluginServerInterface):
    global config
    config_file_path = os.path.join('config', '{}.json'.format(PLUGIN_METADATA.id))
    config = server.load_config_simple(config_file_path, in_data_folder=False, source_to_reply=source,
                                       echo_in_console=False, target_class=Config)


def get_config():
    return config


def send_info(source: CommandSource, message):
    source.reply(message)
    source.get_server().logger.info(message)


def send_error(source: CommandSource, message, error):
    source.reply(message)
    source.get_server().logger.error(message)
    if error is not None:
        source.get_server().logger.error(error)


def find_file(source: CommandSource, file_path):
    # check if file with path given exists
    if os.path.isfile(file_path):
        return True
    send_error(source, f'Couldn\'t found file: {file_path}', None)
    return False


def load_file(source: CommandSource, file_path):
    try:
        # open, load & close file in read mode
        read_file = open(file_path, 'r')
        file_json = json.load(read_file)
        read_file.close()
        return file_json
    except Exception as error:
        send_error(source, f'Couldn\'t load file: {file_path}', error)


def dump_file(source: CommandSource, file_path, file_json):
    try:
        # open file in write mode
        write_file = open(file_path, 'w')
        # save changes into the file in the disk, then closes it
        json.dump(file_json, write_file, indent=2)
    except Exception as error:
        send_error(source, f'Couldn\'t dump file: {file_path}', error)
