import hashlib

from mcdreforged.api.all import CommandSource


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
