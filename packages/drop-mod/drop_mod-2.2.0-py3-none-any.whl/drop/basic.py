"""
Simple-to-use set of functions/commands that don't have a specific goal,
but still are great commands that every bot should have.
"""
import random

from . import ext
from .types import Search, Lyrics, UrbanDefinition
import aiohttp
import json

GENIUS = None


def owofy(string: str):
    """
    Applies an "owospeak" filter over a passed string. God I hate myself.
    """
    for old, new in ext.owofy_letters.items():
        string = string.replace(old, new)
    while '!' in string:
        string = string.replace('!', random.choice(ext.owofy_exclamations), 1)
    return string


async def search(to_search: str):
    """
    Searches for a query across 2 engines: DuckDuckGo (for Instant Answers) and Qwant
    (for general search results).
    """
    engines = [lambda: ext.duckducksearch(to_search), lambda: ext.qwant_search(to_search)]
    result = None
    for engine in engines:
        result = await engine()
        if result:
            break
    if not result:
        return None
    return Search().from_dict(result) if isinstance(result, dict) else result


async def ud_definition(to_search: str):
    """
    Searches for a definition on Urban Dictionary.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.urbandictionary.com/v0/define?term={to_search}") as r:
            return [UrbanDefinition().from_dict(x) for x in (await r.json())['list']]


async def ud_random():
    """
    Gets a random word definition on Urban Dictionary.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.urbandictionary.com/v0/random") as r:
            return UrbanDefinition().from_dict(random.choice((await r.json())['list']))


async def cat_image():
    """
    Fetches an URL of a random cat image.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get('https://aws.random.cat/meow') as r:
            try:
                return json.loads(await r.read())['file']
            except json.JSONDecodeError:
                # fucking hell this API isn't always reliable and might not always return something
                return await cat_image()


async def dog_image():
    """
    Fetches an URL of a random dog image.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get("https://dog.ceo/api/breeds/image/random") as r:
            return (await r.json())['message']


def init_genius(token):
    """
    Initializes Genius' lyrics command (such as get_lyrics() or get_artist()).
    """
    global GENIUS
    GENIUS = token


async def lyrics(query: str):
    """
    Does a Genius search.
    """
    async with aiohttp.ClientSession(headers={'Authorization': f'Bearer {GENIUS}'}) as session:
        async with session.get(f"https://api.genius.com/search?q={query}") as r:
            if r.status == 400:
                print("Genius API token probably not working")
            results = (await r.json())['response']['hits']
            song_result = None
            for song in results:
                if song['result']['primary_artist']['name'] in ext.genius_system_artists:
                    pass
                else:
                    song_result = song['result']
                    break
            if not song_result:
                return None
            # try:
            #     song_result = results[0]['result']
            # except IndexError:
            #     return None
    song_path = f"https://genius.com{song_result['path']}"

    song = Lyrics()

    song.title = song_result["title"]

    extracted_lyrics = (await ext.genius_get_lyrics(song_path)).replace(f"{song.title} Lyrics", '')
    # extracted_lyrics = re.sub(r"([0-9]|[0-9][0-9])Embed", "", extracted_lyrics)  Preliminary BS.

    if extracted_lyrics.endswith('Embed'):
        pyongs = song_result['pyongs_count']
        if pyongs:
            extracted_lyrics = extracted_lyrics.replace(f"{song_result['pyongs_count']}Embed", '')
        else:
            extracted_lyrics = extracted_lyrics[:-5]

    song.lyrics = extracted_lyrics
    song.artist = song_result["primary_artist"]["name"]
    song.url = song_path
    song.thumbnail = song_result["song_art_image_url"]
    song.set_source('Genius', "http://images.genius.com/8ed669cadd956443e29c70361ec4f372"
                              ".1000x1000x1.png")
    return song
