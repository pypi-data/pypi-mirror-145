"""Functions useful for temporary mutes, for any chat bot."""

from datetime import datetime
import json
from .errors import NoMutesForGuild, NoMutesForUser
from .ext import parse_times
from .types import MuteState, MuteEnd

import parsedatetime
cal = parsedatetime.Calendar()


def check_mutes(get_role=True, clear_mutes=True):
    """
    Returns any mutes that should end by now.
    Ideally run this command every minute or so, for maximum efficiency.
    """
    unmute_list = []
    to_clear = []
    dt_string = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open("data/unmutes.json", "r", encoding="utf-8", newline="\n") as file:
        unmutes = json.load(file)
    if dt_string in unmutes:
        # we have stuff to do
        # DON'T TAKE THE WORDS "TO DO" WITH THE SAME DEFINITION AS BONK'S BRITISH DEFINITION
        for to_unmute in unmutes.get(dt_string):
            guild_id = to_unmute[2]
            if get_role:
                role_id = to_unmute[1]
            else:
                role_id = None
            user_id = to_unmute[0]
            unmute_list.append(MuteEnd().from_dict({
                "guild_id": guild_id,
                "role_id": role_id,
                "user_id": user_id
            }))
            if clear_mutes:
                to_clear.append([guild_id, user_id])
        if clear_mutes:
            unmutes = json.load(open("data/unmutes.json", "r", encoding="utf-8", newline="\n"))
            unmutes.pop(dt_string)
            for to_remove in to_clear:
                guild = to_remove[0]
                user = to_remove[1]
                unmutes[str(guild)].pop(str(user))
                if not unmutes.get(str(guild)):
                    unmutes.pop(str(guild))
            json.dump(unmutes, open("data/unmutes.json", "w+", encoding="utf-8", newline="\n"))
    return unmute_list


def add_mutes(guild_id: int, role_id: int, user_id: int, author_id: int, datetime_to_parse: str):
    """
    Add a temporary mute to a user.
    NOTE: datetime_to_parse should be a string like: "1 hour 30 minutes"
    """
    with open("data/unmutes.json", "r+", newline='\n', encoding='utf-8') as temp_file:
        mutes = json.load(temp_file)
    new_mute_data = (user_id, role_id, guild_id)
    str_dt_obj = parse_times(datetime_to_parse)
    # if the script made it this far, this is real we have to store mute data
    if str_dt_obj not in mutes:
        mutes[str_dt_obj] = []
    mutes[str_dt_obj].append(new_mute_data)
    mute_index = len(mutes[str_dt_obj]) - 1
    if str(guild_id) not in mutes:
        mutes[str(guild_id)] = {}
    if str(user_id) in mutes[str(guild_id)]:
        mutes[str(guild_id)].pop(str(user_id))
    if not str(user_id) in mutes[str(guild_id)]:
        mutes[str(guild_id)][str(user_id)] = []
    mutes[str(guild_id)][str(user_id)] = [str_dt_obj, author_id, mute_index]
    json.dump(mutes, open("data/unmutes.json", "w+", newline='\n', encoding='utf-8'))
    return str_dt_obj
    # Don't worry I can't read this mess either.


def get_mute_status(guild_id: int, user_id: int):
    """
    Return data of the user's mute.
    """
    with open("data/unmutes.json", "r", newline='\n', encoding='utf-8') as temp_file:
        mutes = json.load(temp_file)
    guild_mutes = mutes.get(str(guild_id))
    if guild_mutes is None:
        raise NoMutesForGuild(f"Guild {guild_id} does not have any current mutes.")
    user_mutes = guild_mutes.get(str(user_id))
    if not user_mutes:
        raise NoMutesForUser(f"User {user_id} in guild {guild_id} does not have any current mutes.")
    # user has been muted.
    mute_index = user_mutes[2]
    mute_data = mutes.get(user_mutes[0])[mute_index]
    mute_role_id = mute_data[1]
    return MuteState().from_dict({
        "unmute_time": user_mutes[0],
        "mute_author_id": user_mutes[1],
        "mute_index": mute_index,
        "mute_data": mute_data,
        "mute_role_id": mute_role_id
    })


def get_mutes():
    """
    Gets all mutes.
    """
    with open("data/unmutes.json", "r", newline='\n', encoding='utf-8') as temp_file:
        return json.load(temp_file)


def unmute_user(guild_id: int, user_id: int):
    """
    Remove the mute status from a user.
    """
    mutes = get_mutes()
    guild_mutes = mutes.get(str(guild_id))
    user_mute = get_mute_status(guild_id, user_id)
    mute_time = user_mute.unmute_time
    mute_index = user_mute.mute_index
    mute_role_id = user_mute.mute_role_id
    mutes.get(mute_time).pop(mute_index)
    if not mutes.get(mute_time):
        mutes.pop(mute_time)
    guild_mutes.pop(str(user_id))
    if not guild_mutes:
        mutes.pop(str(guild_id))
    else:
        for value in mutes[str(guild_id)].items():
            value[2] = value[2] - 1
    json.dump(mutes, open("data/unmutes.json", "w+", newline='\n', encoding='utf-8'))
    return mute_role_id
