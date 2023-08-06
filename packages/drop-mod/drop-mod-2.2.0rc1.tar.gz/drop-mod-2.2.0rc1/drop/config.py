"""
Functions for guild/bot config files and whatnot.
"""

import json
import os

from .errors import ConfigParameterNotFound, ConfigNotFound

BOT_CONFIG = {}


def load_config(filepath: str):
    """
    Loads a bot's config file using the given filepath.
    """
    try:
        with open(filepath, "r", encoding="utf-8", newline="\n") as file:
            config = json.load(file)
    except FileNotFoundError as exception:
        raise ConfigNotFound(f"Config file {filepath} doesn't exist.") from exception
    global BOT_CONFIG
    global CONFIG_FILEPATH
    BOT_CONFIG = config
    CONFIG_FILEPATH = filepath


CONFIG_FILEPATH = "data/config.json"
try:
    load_config("data/config.json")
except ConfigNotFound:
    BOT_CONFIG = {}
    if not os.path.isdir("data/"):
        os.mkdir("data/")
    json.dump(BOT_CONFIG, open(CONFIG_FILEPATH, "w+", encoding="utf-8", newline="\n"), indent=2)


def save_config(new_config=None):
    """
    Saves any changes made to the bot's config.
    """
    if new_config is None:
        new_config = BOT_CONFIG
    json.dump(new_config, open(CONFIG_FILEPATH, "w+", encoding="utf-8", newline="\n"), indent=2)


def get_config_parameter(parameter, parameter_type=None):
    """
    Gets a specific value from the bot's config using a key. Because it's just a dictionary.
    """
    config_param = BOT_CONFIG.get(parameter)
    if config_param is None:
        raise ConfigParameterNotFound(f"Config file doesn't have key {parameter}")
    if not parameter_type:
        parameter_type = type(config_param)
    return parameter_type(config_param)


def get_config():
    """
    Returns the current bot config.
    """
    return BOT_CONFIG


def write_config_parameter(parameter, new_value, parameter_type=None):
    """
    Writes and saves a value inside the bot's config using a key.
    """
    if not parameter_type:
        parameter_type = type(new_value)
    BOT_CONFIG[parameter] = parameter_type(new_value)
    save_config()

# server config time


def get_server_config(guild_id, parameter, parameter_type=None):
    """
    Gets a value from a guild's config, using a key. Because, again, it's a dictionary.
    """
    try:
        config_parameter = get_entire_server_config(guild_id).get(parameter)
        if not config_parameter:
            raise ConfigParameterNotFound(f"Config file for guild {guild_id} doesn't "
                                          f"have key {parameter}")
        if not parameter_type:
            parameter_type = type(config_parameter)
        return parameter_type(config_parameter)
    except FileNotFoundError as exception:
        # No config exists for this server.
        raise ConfigNotFound(f"Config file not found for guild {guild_id}") from exception


def get_entire_server_config(guild_id):
    """
    Returns a guild's entire config
    """
    try:
        with open(f"data/servers/{guild_id}/config.json", "r", encoding="utf-8", newline="\n") \
                as file:
            server_config = json.load(file)
            return server_config
    except FileNotFoundError:
        touch_server_config(guild_id)
        return {}


def touch_server_config(guild_id):
    """
    Creates a server's guild, without writing anything to it.
    Similar to Linux's "touch" command.
    """
    if not os.path.exists('data/'):
        os.mkdir('data/')
    if not os.path.exists('data/servers/'):
        os.mkdir('data/servers/')
    if not os.path.exists(f'data/servers/{guild_id}/'):
        os.mkdir(f'data/servers/{guild_id}/')
    json.dump({}, open(f'data/servers/{guild_id}/config.json', 'w+'))


def write_server_config(guild_id, param, value):
    """
    Writes a value to a guild's config using a key.
    """
    filepath = f"data/servers/{guild_id}/config.json"
    server_config = get_entire_server_config(guild_id)
    server_config[param] = value
    json.dump(server_config, open(filepath, 'w+', encoding="utf-8", newline='\n'))


def write_entire_server_config(guild_id, config: dict):
    """
    Writes, or overwrites, a guild's entire config to a dictionary.
    """
    filepath = f"data/servers/{guild_id}/config.json"
    json.dump(config, open(filepath, 'w+', encoding="utf-8", newline='\n'))
