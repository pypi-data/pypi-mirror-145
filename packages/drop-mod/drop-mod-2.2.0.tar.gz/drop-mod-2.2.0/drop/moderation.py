"""General moderation commands, ideal for a chat bot."""

import os
import json
from datetime import datetime
from .errors import NoWarnError, NoRulesError, BrokenRulesError, NoMutesForUser, \
    NoMutesForGuild, NoTempBansForGuild
from .mute import add_mutes, get_mute_status, unmute_user
from .tempban import add_bans, get_ban_status, unban_user
from .types import Warn


def warn(guild_id: int, user_id: int, author_id: int, author_name: str,
         channel_id: int, reason: str):
    """Warn a user inside a guild."""
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if not os.path.exists("data/servers/" + str(guild_id) + "/warns/"):
        os.makedirs("data/servers/" + str(guild_id) + "/warns/")
        # Checks if the folder for the guild exists. If it doesn't, create it.
    try:
        with open(f"data/servers/{guild_id}/warns/{user_id}.json", newline="\n", encoding='utf-8') \
                as warn_file:
            warn_data = json.load(warn_file)
        # See if the user has been warned
    except FileNotFoundError:
        # User has not been warned yet
        with open(f"data/servers/{guild_id}/warns/{user_id}.json", 'w+', newline="\n",
                  encoding='utf-8') as warn_file:
            warn_data = ({
                'warns': [
                    {
                        'warner': author_id,
                        'warner_name': author_name,
                        'reason': reason,
                        'channel': str(channel_id),
                        'datetime': dt_string
                    }
                ]
            })
            json.dump(warn_data, warn_file)
    else:
        # If the script made it this far, then the user has been warned
        warn_data["offender_name"] = user_id
        new_warn = ({
            'warner': author_id,
            'warner_name': author_name,
            'reason': reason,
            'channel': str(channel_id),
            'datetime': dt_string
        })
        warn_data["warns"].append(new_warn)
        json.dump(warn_data, open(f"data/servers/{guild_id}/warns/{user_id}.json", "w+",
                                  newline="\n", encoding='utf-8'))


def get_warn_file(guild_id: int, user_id: int):
    """
    Returns the JSON data of the user's warn file.
    Or the legacy "get_warns()", now that I think about it.
    """
    try:
        with open(f"data/servers/{guild_id}/warns/{user_id}.json", 'r', newline="\n",
                  encoding='utf-8') as warn_file:
            return json.load(warn_file)
        # See if the user has been warned
    except FileNotFoundError:
        # User does not have any warns.
        return None


def get_warns(guild_id: int, user_id: int):
    """Returns a user's warns inside a guild."""
    warns = get_warn_file(guild_id, user_id)
    warns_list = []
    for x in warns.get('warns'):
        y = Warn()
        y.from_dict(x)
        warns_list.append(y)
    return warns_list


def write_warns(guild_id: int, user_id: int, new_warns: dict):
    """Overwrite a user's warns to a specific dictionary.
    Please only use this if you know what you're doing."""
    try:
        with open(f"data/servers/{guild_id}/warns/{user_id}.json", 'w', newline="\n",
                  encoding='utf-8') as warn_file:
            json.dump(new_warns, warn_file)
    except FileNotFoundError:
        # User does not have any warns.
        pass


def get_warn(guild_id: int, user_id: int, warn_index: int):
    """Get a user's warn by a specific index."""
    try:
        with open(f"data/servers/{guild_id}/warns/{user_id}.json", newline="\n",
                  encoding='utf-8') as warn_file:
            warn_data = json.load(warn_file)
        # See if the user has been warned
    except FileNotFoundError:
        # User does not have any warns.
        return None
    warns = warn_data.get('warns')
    warning = Warn()
    warning.from_dict(warns[warn_index])
    try:
        return warning
    except IndexError as exception:
        raise IndexError(f"Warn index {warn_index} is not in current user's warns") from exception


def remove_warn(guild_id: int, user_id: int, warn_index: int):
    """Remove a user's warn using a specific index."""
    warn_data = get_warn_file(guild_id, user_id)
    if warn_data is None:
        raise NoWarnError(f"User {user_id} does not have any warns: impossible to remove warns "
                          f"if they don't exist")
    warns = warn_data['warns']
    # do the whole removing process.
    warns = [x for x in warns if x != warns[warn_index]]
    warn_data["warns"] = warns
    if len(warns) <= 0:
        # no warns, might as well remove the file
        clear_warns(guild_id, user_id)
    else:
        json.dump(warn_data, open(f"data/servers/{guild_id}/warns/{user_id}.json", 'w',
                                  newline="\n", encoding='utf-8'))


def clear_warns(guild_id: int, user_id: int):
    """Clear a user's entire config."""
    try:
        os.remove(f"data/servers/{guild_id}/warns/{user_id}.json")
    except FileNotFoundError:
        # raise NoWarnError(f"User {user_id} does not have any warns: "
        #                   f"impossible to clear warns if they don't exist")
        pass  # Raising an error just for that sounds INCREDIBLY dumb.


def edit_warn(guild_id: int, user_id: int, warn_index: int, new_reason: str):
    """Edit a user's warn by a specific index."""
    warns = get_warn_file(guild_id, user_id)
    warn_element = warns.get('warns')[warn_index]
    warn_element['reason'] = new_reason
    write_warns(guild_id, user_id, warns)

# warn stuff done
# lets do rules now


def get_rules(guild_id: int):
    """Get a guild's entire rules."""
    rule_file = 'data/servers/' + str(guild_id) + '/rules.json'
    try:
        return json.load(open(rule_file, "r", encoding="utf-8", newline="\n"))
    except FileNotFoundError as exception:
        raise NoRulesError(f"No rules had been set for guild {str(guild_id)}.") from exception
    except json.JSONDecodeError as exception:
        # wuh oh we may have a dead JSON file
        json.dump({}, open('data/servers/' + str(guild_id) + '/rules.json', 'w+', newline='\n',
                           encoding="utf-8"))
        raise BrokenRulesError(f"Invalid JSON rule file for guild {str(guild_id)}: "
                               f"it has been reset.") from exception


def get_rule(guild_id: int, index: str):
    """Get a specific rule from a guild."""
    return get_rules(guild_id).get(index.lower())


def set_rule(guild_id: int, index: str, description: str):
    """Set a guild's rule"""
    try:
        rules = get_rules(guild_id)
    except NoRulesError:
        # no rules, make from scratch
        rules = {}
    rules[index.lower()] = description
    json.dump(rules, open('data/servers/' + str(guild_id) + '/rules.json', 'w+', newline='\n',
                          encoding="utf-8"))


def pop_rule(guild_id: int, index: str):
    """Remove a rule from a guild."""
    rules = get_rules(guild_id)
    filepath = 'data/servers/' + str(guild_id) + '/rules.json'
    with open(filepath, 'r') as file:
        try:
            rules.pop(index.lower())
        except KeyError as exception:
            raise KeyError(f"Rule {index.lower()} does not exist for guild {guild_id}.") \
                from exception
        if rules is None:
            file.close()
            os.remove(filepath)
        else:
            json.dump(rules, open(filepath, 'w+'))


def migrate_user(guild_id: int, user_id: int, new_user_id: int):
    """Migrate an entire user's data to another."""
    user_warns = get_warns(guild_id, user_id)
    for warning in user_warns:
        warn(guild_id, new_user_id, warning.get('warner'),
             warning.get('warner_name'), warning.get('channel'), warning.get('reason'))
    try:
        mute = get_mute_status(guild_id, user_id)
    except (NoMutesForUser, NoMutesForGuild):
        pass
    else:
        add_mutes(guild_id, mute['mute_role_id'], new_user_id, mute['mute_author_id'],
                  mute['unmute_time'])
        unmute_user(guild_id, user_id)
    # temp bans
    try:
        temp_ban = get_ban_status(guild_id, user_id)
    except NoTempBansForGuild:
        pass
    else:
        if temp_ban:
            add_bans(guild_id, new_user_id, temp_ban['ban_author_id'], temp_ban['unban_time'])
            unban_user(guild_id, user_id)
