"""Extra functions for drop-mod that I didn't think would fit anywhere else."""
import random
import re
from datetime import datetime

from .errors import InvalidTimeParsed, PastTimeError, PresentTimeError
from . import __version__ as version
from .types import Search, _SearchField, TumblrImages

from bs4 import BeautifulSoup
import parsedatetime
import aiohttp
from json import loads

cal = parsedatetime.Calendar()

owofy_letters = {'r': 'w',
                 'l': 'w',
                 'R': 'W',
                 'L': 'W',
                 'na': 'nya',  # please stop.
                 'ne': 'nye',
                 'ni': 'nyi',
                 ' no ': ' nu ',
                 ' nO ': ' nU ',
                 ' NO ': ' NU ',
                 ' No ': ' Nu ',
                 'no': 'nyo',
                 'nu': 'nyu',
                 'Na': 'Nya',  # oh no the capitalization
                 'Ne': 'Nye',
                 'Ni': 'Nyi',
                 'No': 'Nyo',
                 'Nu': 'Nyu',
                 'nA': 'nyA',  # aaaaaaaaaaaaaaaaaaaaaaaaaa
                 'nE': 'nyE',
                 'nI': 'nyI',
                 'nO': 'nyO',
                 'nU': 'nyU',
                 'NA': 'NYA',  # this is mental torture.
                 'NE': 'NYE',
                 'NI': 'NYI',
                 'NO': 'NYO',
                 'NU': 'NYU',  # I f***ing hate myself.
                 'the ': 'de ',
                 'THE ': 'DE ',
                 'THe ': 'De ',
                 'The ': 'De ',
                 'tHE ': 'dE ',
                 'thE ': 'dE ',  # you seem to have found the exact line where i lose motivation
                 'tt': 'dd',
                 'ock': 'awk',
                 'uck': 'ek',
                 'ou': 'u',
                 'tT': 'dD',
                 'Tt': 'Dd',
                 'TT': 'DD',
                 'ocK': 'awK',
                 'oCK': 'aWK',
                 'OCK': 'AWK',
                 'OCk': 'AWk',
                 'Ock': 'Awk',
                 'ucK': 'eK',
                 'uCK': 'eK',
                 'UCK': 'EK',
                 'UCk': 'Ek',
                 'Uck': 'Ek',
                 'oU': 'U',
                 'OU': 'U',
                 'Ou': 'u'}  # removed stuff because... well, some didn't even work right.
owofy_exclamations = [' OwO', ' @w@', ' #w#', ' UwU', ' ewe', ' -w-', ' \'w\'', ' ^w^', ' >w<',
                      ' ~w~', ' ¬w¬', ' o((>ω< ))o', ' (p≧w≦q)', ' ( •̀ ω •́ )y', ' ✪ ω ✪',
                      ' (。・ω・。)', ' (^・ω・^ )']
# Why'd I put so many here?


to_replace = {
    '<b>': '**',
    '</b>': '**',
    '<p>': '\n**',
    '</p>': '**\n',
    '</li>': '\n',
    '&amp;': '&',
    '&rsquo;': '\''
}

protondb_colors = {"Platinum": 0xB7C9DE, "Gold": 0xCFB526, "Silver": 0xC1C1C1, "Bronze": 0xCB7F22,
                   "Borked": 0xF90000}  # freaking pylint, man.


def format_html(str_input: str):
    """Removes any HTML formatting from a string."""
    for old, new in to_replace.items():
        str_input = str_input.replace(old, new)
    return re.sub(r'<.*?>', '', str_input)


def format_names(name_list: list):
    """
    Takes a list and returns a string formatting every string inside said list.

    For example, ['john', 'jane', 'joe'] would become "john, jane and joe"
    """
    name_count = len(name_list) - 1
    names = ""
    for idx, name in enumerate(name_list):
        if idx == 0:
            # First name
            names = name
        elif idx == name_count:
            # Last name
            names = names + " and " + name
        else:
            # A name.
            names = names + ", " + name
    return names


def parse_times(datetime_to_parse: str):
    """
    Parses strings containing time formats and returns a string format
    used for temporary punishments such as mute or temp-ban.
    """
    dt_obj = cal.parseDT(datetimeString=datetime_to_parse)
    now_dt = datetime.now()
    list_dt_obj = str(dt_obj[0]).split(":")
    list_now_dt = str(now_dt).split(":")

    str_now_dt = f'{list_now_dt[0]}:{list_now_dt[1]}'
    str_dt_obj = f'{list_dt_obj[0]}:{list_dt_obj[1]}'
    if dt_obj[1] == 0:
        raise InvalidTimeParsed(f"Time string {datetime_to_parse} could not be parsed")
    if dt_obj[0] <= now_dt:
        raise PastTimeError(f"Time {str(dt_obj)} is in the past: "
                            f"there's no logical way to unban them that way")
    if dt_obj[0] == now_dt or str_dt_obj == str_now_dt:
        raise PresentTimeError(f"Time {str(dt_obj)} is the same as now ({str(now_dt)})")
    return str_dt_obj


async def duckducksearch(to_search: str):
    # response = duckduckpy.query(to_search, user_agent=u'duckduckpy 0.2', no_redirect=False,
    #                             no_html=True, skip_disambig=True)
    # https://api.duckduckgo.com/?q=DuckDuckGo&format=json&pretty=1
    async with aiohttp.ClientSession(headers={'User-Agent': f'drop-mod {version}'}) as session:
        async with session.get(
                # f"https://api.qwant.com/api/search/web?count=10&offset=0&q={to_search}"
                f"https://api.duckduckgo.com/?q={to_search}&format=json&no_html=1") as r:
            response = await r.json(content_type=None)
    if response['Abstract']:
        infobox = []
        is_infobox = False
        image = None
        if response['Infobox']:
            infobox = response['Infobox']['content']
            is_infobox = True
        if response['Image']:
            response_image = response['Image']
            image = f'https://duckduckgo.com{response_image}' \
                if response_image.startswith('/') else response_image
        result = {
            "title": response['Heading'],
            "description": format_html(response['AbstractText']),
            "url": response['AbstractURL'],
            "source": response['AbstractSource'],
            "image": image,
            "fields": [{
                'name': x['label'],
                'value': ''.join(list(x['value'])[:253]) + '...' if len(x) >= 256 else x['value']
            } for x in infobox if x['data_type'] == 'string'],
            "infobox": is_infobox,
            "engine": "DuckDuckGo",
            "engine_icon": "https://duckduckgo.com/assets/icons/meta/DDG-icon_256x256.png"
        }
    else:
        return None
    return result


async def qwant_search(to_search: str):
    # response = requests.get(
    #     f"https://api.qwant.com/api/search/web?count=10&offset=0&q={to_search}"
    #     f"&t=web"
    #     f"&uiv=1"
    #     f"&safesearch=2"
    #     f"&locale=en_US",
    #     headers={'User-Agent': f'drop-mod {version}'}).json()
    async with aiohttp.ClientSession(headers={'User-Agent': f'drop-mod {version}'}) as session:
        async with session.get(
                f"https://api.qwant.com/api/search/web?count=10&offset=0&q={to_search}"
                f"&t=web"
                f"&uiv=1"
                f"&safesearch=2"
                f"&locale=en_US") as r:
            response = await r.json()
    items = response['data']['result']['items']
    if not items:
        return None

    result = Search()
    result.engine = "Qwant"
    result.engine_icon = "https://www.qwant.com/public/favicon-196" \
                         ".72d42c0cdb4ff221db29fea589d2e8d4.png"
    result.title = f"Search results for {response['data']['query']['query']}"  # this is logic
    result.fields = [_SearchField().from_dict(x) for x in items]
    return result


async def genius_get_lyrics(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                try:
                    # html = BeautifulSoup(
                    #     self._make_request(path, web=True).replace('<br/>', '\n'),
                    #     "html.parser"
                    # )
                    html = BeautifulSoup((await r.text()).replace('<br/>', '\n'), "html.parser")
                    div = html.find("div", class_=re.compile("^lyrics$|Lyrics__Root"))
                    if div is None:
                        return "The song probably does not have any lyrics."
                    return div.get_text()
                    # return BeautifulSoup(await r.text(), "html.parser") \
                    #     .find("div", class_=re.compile("^lyrics$|Lyrics__Root")).get_text()
                    # will not return any newlines. at all.
                except AttributeError:
                    return await genius_get_lyrics(url)


async def get_random_tumblr_post(blog_name: str):
    async with aiohttp.ClientSession(headers={'User-Agent': f'drop-mod {version}'}) as session:
        async with session.get(f'https://{blog_name}.tumblr.com/api/read/json') as r:
            if not r.status == 200:
                return
            tumblr_blog = loads((await r.text()).replace("var tumblr_api_read = ", "")
                                .replace(";\n", ""))
            # all of the replace statements here are to eliminate the javascript variable stuff.
            return random.choice(tumblr_blog['posts'])


async def random_tumblr_image(blog_name: str):
    post_dict = await get_random_tumblr_post(blog_name=blog_name)
    post = TumblrImages()
    if post_dict['type'] != 'regular':
        return await random_tumblr_image(blog_name)
    post.image = re.findall(r"img src=\"(.*?)\"", post_dict['regular-body'])[0]
    description = re.findall(r"</figure><p>(.*?)</p>", post_dict['regular-body'])
    if description:
        post.description = description[0]
    post.datetime = datetime.fromtimestamp(post_dict['unix-timestamp'])
    post.url = post_dict['url']
    post.blogger.from_dict(post_dict['tumblelog'])
    return post


genius_system_artists = ('Genius', 'Spotify', 'Ego Trip Magazine')
