"""Functions that returns lists of IDs, for any specific need."""

import os


def find_guilds():
    """Returns a list of every guilds."""
    try:
        return os.listdir('data/servers/')
    except FileNotFoundError:
        return []


def find_todos():
    """Returns a list of every to-do notes' ID."""
    todo_files = []
    try:
        files = os.listdir("data/todo/")
    except FileNotFoundError:
        return todo_files
    for file in files:
        if file.endswith(".json"):
            todo_files.append(file.split('.')[0])
    return todo_files


def find_warns(guild_id: int):
    """Returns a list of every warned user's ID."""
    warn_files = []
    try:
        files = os.listdir(f"data/servers/{guild_id}/warns/")
    except FileNotFoundError:
        return warn_files
    for file in files:
        if file.endswith(".json"):
            warn_files.append(file.split('.')[0])
    return warn_files
