from datetime import datetime


class Moderator:
    """Someone who moderates. Has an ID and name for the moderator."""
    id = 0
    name = ""


class Warn:
    """A warning, usually to a user"""
    warner = Moderator()
    reason = ""
    channel = ""
    datetime = ""

    def from_dict(self, warn_dict: dict):
        self.warner = Moderator()
        self.warner.id = warn_dict['warner']
        self.warner.name = warn_dict['warner_name']
        self.reason = warn_dict['reason']
        self.channel = warn_dict['channel']
        self.datetime = warn_dict['datetime']
        return self

    def to_dict(self):
        return {
            "warner": self.warner.id,
            "warner_name": self.warner.name,
            "reason": self.reason,
            "channel": self.channel,
            "datetime": self.datetime
        }

    def __getitem__(self, item):
        # so that people using drop-mod with dictionaries will still be able to use it
        # hopefully without changing much. sort-of legacy support, I guess you can call it that?
        return getattr(self, item) if hasattr(self, item) else self.to_dict().get(item)

    def get(self, item):
        # since some might still use dictionary.get()
        return self.__getitem__(item)


class TodoItem:
    description = ""
    time = ""
    author = 0

    def to_dict(self):
        return {
            "desc":   self.description,
            "time":   self.time,
            "author": self.author
        }

    def __getitem__(self, item):
        return getattr(self, item) if hasattr(self, item) else self.to_dict().get(item)

    def from_dict(self, todo_dict: dict):
        self.description = todo_dict.get('desc')
        self.time = todo_dict.get('time')
        self.author = todo_dict.get('author')
        return self


class _SearchField:
    """A search field. Can be from a Wikipedia result field to a search result."""
    name = ""
    value = ""
    url = ""

    def __getitem__(self, item):
        return getattr(self, item)

    def from_dict(self, field: dict):
        self.name = field.get('name') if field.get('name') else field.get('title')
        self.value = field.get('desc') if field.get('desc') else field.get('value')
        self.url = field.get('url')
        return self


class Search:
    """The class for search results."""
    """
    {'title': 'Wikipedia',
     'description': 'Wikipedia is a free, multilingual online encyclopedia written ...',
     'url': 'https://en.wikipedia.org/wiki/Wikipedia', 'source': 'Wikipedia',
     'image': 'https://duckduckgo.com/i/a96348db.png',
     'fields': [{'name': 'Available in', 'value': 'languages'},
                {'name': 'Country of origin', 'value': 'United States'},
                {'name': 'Created by', 'value': 'Jimmy Wales, Larry Sanger'},
                {'name': 'Website', 'value': 'wikipedia.org'},
                {'name': 'Commercial', 'value': 'No'},
                {'name': 'Registration', 'value': 'Optional'}],
     'infobox': True}
    """
    title = ""
    description = ""
    url = ""
    source = ""
    engine = ""
    engine_icon = ""
    image = ""
    fields = []

    def __getitem__(self, item):
        # so that people using drop-mod with dictionaries will still be able to use it
        # hopefully without changing much. sort-of legacy support, I guess you can call it that?
        return getattr(self, item)

    def from_dict(self, search_result: dict):
        self.title = search_result['title']
        self.description = search_result['description']
        self.url = search_result['url']
        self.image = search_result['image']
        self.fields = [_SearchField().from_dict(x) for x in search_result['fields']]
        self.engine = search_result.get('engine')
        self.engine_icon = search_result.get('engine_icon')
        return self


class Lyrics:
    title = "Silence"
    artist = "Nature"
    url = ""
    thumbnail = ""
    source = "Nowhere"
    source_icon = ""
    lyrics = "Yeah, well, silence has no sound."

    def __getitem__(self, item):
        return getattr(self, item)

    def get(self, item):
        return self.__getitem__(item)

    def from_dict(self, lyrics_dict: dict):
        self.title = lyrics_dict.get('title')
        self.artist = lyrics_dict.get('artist')
        self.url = lyrics_dict.get('url')
        self.thumbnail = lyrics_dict.get('song_art_image_url')
        self.lyrics = lyrics_dict.get('lyrics')
        return self

    def set_source(self, name: str, icon: str):
        self.source = name
        self.source_icon = icon
        return self


class MuteState:
    unmute_time = ""
    mute_author_id = 0
    index = 0
    mute_data = [0, 0, 0]
    role_id = 0

    def from_dict(self, mute_dict: dict):
        self.unmute_time = mute_dict.get('unmute_time')
        self.mute_author_id = mute_dict.get('mute_author_id')
        self.index = mute_dict.get('mute_index')
        self.mute_data = mute_dict.get('mute_data')
        return self

    def __getitem__(self, item):
        return getattr(self, item)


class MuteEnd:
    """I have no other name ideas."""
    guild_id = 0
    role_id = 0
    user_id = 0

    def from_dict(self, mute_dict: dict):
        self.guild_id = mute_dict.get('guild_id')
        self.role_id = mute_dict.get('role_id')
        self.user_id = mute_dict.get('user_id')
        return self

    def __getitem__(self, item):
        return getattr(self, item)


class TempbanState:
    unban_time = ""
    ban_author_id = 0
    index = 0
    ban_data = [0, 0]

    def from_dict(self, mute_dict: dict):
        self.unban_time = mute_dict.get('unban_time')
        self.ban_author_id = mute_dict.get('ban_author_id')
        self.index = mute_dict.get('ban_index')
        self.ban_data = mute_dict.get('ban_data')
        return self

    def __getitem__(self, item):
        return getattr(self, item)


class TempbanEnd:
    """I have no other name ideas."""
    guild_id = 0
    user_id = 0

    def from_dict(self, mute_dict: dict):
        self.guild_id = mute_dict.get('guild_id')
        self.user_id = mute_dict.get('user_id')
        return self

    def __getitem__(self, item):
        return getattr(self, item)


class UrbanDefinition:
    word = ""
    definition = ""
    example = ""
    url = ""
    thumbs_up = 0
    author = ""
    time = ""

    def from_dict(self, ud_dict: dict):
        self.definition = ud_dict.get('definition')
        self.url = ud_dict.get('permalink')
        self.thumbs_up = ud_dict.get('thumbs_up')
        self.author = ud_dict.get('author')
        self.word = ud_dict.get('word')
        self.time = ud_dict.get('written_on')
        self.example = ud_dict.get('example')
        return self


class TumblrBlog:
    title = ""
    name = ""
    url = ""
    avatar = ""

    def from_dict(self, tumblelog: dict):
        self.title = tumblelog.get('title')
        self.name = tumblelog.get('name')
        self.url = tumblelog.get('url')
        self.avatar = tumblelog.get('avatar_url_512')
        return self


class TumblrImages:
    post_id = ""
    url = ""
    datetime = datetime
    image = ""
    description = ""
    blogger = TumblrBlog()
