"""Functions for both user-specific and guild-specific to-dos."""

import os
import json
from datetime import datetime

from .types import TodoItem

DIR_PATH = "data/todo/"


def init_todo(user_id: int, force_init=False):
    """
    Loads user-specific to-dos using the given filepath.
    """
    file_path = DIR_PATH + f"{user_id}.json"
    if not os.path.exists(DIR_PATH):
        os.makedirs(DIR_PATH)
    if (not os.path.exists(file_path)) or force_init:
        with open(file_path, 'w+', newline="\n", encoding='utf-8') as todo_file:
            todo_data = []
            json.dump(todo_data, todo_file)


def get_raw_todos(user_id: int):
    """
    Returns the raw to-do JSON dictionary-ish.
    """
    file_path = DIR_PATH + f"{user_id}.json"
    try:
        with open(file_path, newline="\n", encoding='utf-8') as todo_file:
            todo_data = json.load(todo_file)
            # does the user have to-do stuff
    except FileNotFoundError:
        # no
        init_todo(user_id=user_id)  # mess.
        todo_data = get_raw_todos(user_id)  # this works
    except json.JSONDecodeError:
        # yes but it's not right
        init_todo(user_id, True)
        todo_data = get_raw_todos(user_id)
    return todo_data


def get_todos(user_id: int):
    """Get the specified user's to-dos."""
    todo_data = get_raw_todos(user_id)
    return [TodoItem().from_dict(x) for x in todo_data]


def get_todo(user_id: int, index: int):
    """Get a specific to-do item from a user's to-do list."""
    return get_todos(user_id)[index]


def edit_todo(user_id: int, index: int, description: str):
    """Edit a user's to-do item."""
    todo_data = get_raw_todos(user_id)
    new_todo = {
        'desc': description,
        'time': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    }
    todo_data[index] = new_todo
    with open(f"data/todo/{user_id}.json", 'w+', newline="\n", encoding='utf-8') as todo_file:
        json.dump(todo_data, todo_file)


def add_todo(user_id: int, description: str):
    """Append a to-do item to a user's to-do list."""
    todo_data = get_raw_todos(user_id)
    new_todo = {
        'desc': description,
        'time': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    todo_data.append(new_todo)
    with open(f"data/todo/{user_id}.json", 'w+', newline="\n", encoding='utf-8') as todo_file:
        json.dump(todo_data, todo_file)
        todo_file.close()


def rm_todo(user_id: int, index: int):
    """Remove a to-do item from a user's to-do list."""
    todo_data = get_raw_todos(user_id)
    try:
        todo_data.pop(index)
    except IndexError as exception:
        raise IndexError(f"Index {index} does not exist in to-do data for user {user_id}") \
            from exception
    with open(f"data/todo/{user_id}.json", 'w+', newline="\n", encoding='utf-8') as todo_file:
        json.dump(todo_data, todo_file)
        todo_file.close()


# guild stuff


def get_raw_guild_todos(guild_id: int):
    """Gets raw to-dos in a dictionary format."""
    with open(f"data/servers/{guild_id}/todo.json", newline="\n", encoding='utf-8') as \
            todo_file:
        return json.load(todo_file)


def get_guild_todos(guild_id: int):
    """Gets every to-dos from a guild."""
    try:
        return [TodoItem().from_dict(x) for x in get_raw_guild_todos(guild_id)]
    except FileNotFoundError:
        init_guild_todos(guild_id)
    except json.JSONDecodeError:
        init_guild_todos(guild_id, True)
    return get_guild_todos(guild_id)


def init_guild_todos(guild_id: int, force_init=False):
    """
    Initialize a to-do list for a guild.

    NOTE: force_init will RESET the past to-do list, if it exists!
    Only set it to True if you know what you're doing.
    """
    if not os.path.exists(f"data/servers/{guild_id}/"):
        os.makedirs(f"data/servers/{guild_id}/")
    if (not os.path.exists(f"data/servers/{guild_id}/todo.json")) or force_init:
        json.dump([], open(f"data/servers/{guild_id}/todo.json", "w+"))


def rm_guild_todo(guild_id: int, index: int):
    """Remove a to-do item from a guild's to-do list."""
    todo_data = get_raw_guild_todos(guild_id)
    try:
        todo_data.pop(index)
    except IndexError as exception:
        raise IndexError(f"Index {index} does not exist in to-do data for guild {guild_id}") \
            from exception
    if len(todo_data) == 0:
        os.remove(f"data/servers/{guild_id}/todo.json")
    else:
        with open(f"data/servers/{guild_id}/todo.json", "w+", newline="\n", encoding='utf-8') \
                as todo_file:
            json.dump(todo_data, todo_file)
            todo_file.close()


def add_guild_todo(guild_id: int, description: str, author_id: int):
    """Add a to-do item to a guild's to-do list."""
    todo_data = get_raw_guild_todos(guild_id)
    new_todo = {
        'desc': description,
        'time': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        'author': author_id
    }
    todo_data.append(new_todo)
    with open(f"data/servers/{guild_id}/todo.json", 'w+', newline="\n", encoding='utf-8') as \
            todo_file:
        json.dump(todo_data, todo_file)
        todo_file.close()


def edit_guild_todo(guild_id: int, index: int, description: str):
    """Edit a to-do item from a guild's to-do list."""
    todo_data = get_raw_guild_todos(guild_id)
    new_todo = {
        'desc': description,
        'time': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'author': todo_data[index]['author']
    }
    todo_data[index] = new_todo
    with open(f"data/servers/{guild_id}/todo.json", 'w+', newline="\n", encoding='utf-8') as \
            todo_file:
        json.dump(todo_data, todo_file)
