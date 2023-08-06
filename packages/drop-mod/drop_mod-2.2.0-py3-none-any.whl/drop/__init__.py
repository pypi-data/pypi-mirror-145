"""
A Python moderation toolkit built for chat bots
"""

__version__ = "2.2.0"


def licenses(markdown_links=False):
    """
    Returns all of the licenses for drop-mod's dependencies.
    """
    license_list = [
        {
            "name": "Drop",
            "license": "Apache 2.0",
            "link": "https://github.com/AtlasC0R3/drop-moderation/blob/master/LICENSE",
            "changes": "no changes made"
        },
        {
            "name": "Parsedatetime",
            "license": "Apache 2.0",
            "link": "https://github.com/bear/parsedatetime/blob/master/LICENSE.txt",
            "changes": "no changes made"
        },
        {
            "name": "aiohttp",
            "license": "Apache 2.0",
            "link": "https://github.com/aio-libs/aiohttp/blob/master/LICENSE.txt ",
            #         "(http://www.apache.org/licenses/LICENSE-2.0)",
            # The LICENSE.txt directs the user there anyways.
            "changes": "no changes made"
        },
        {
            "name": "BeautifulSoup",
            "license": "MIT License",
            "link": "https://mit-license.org/",
            # AFAIK there's no official link to its own license. Correct me if I'm wrong.
            # I'll gladly correct that error.
            "changes": "no changes made"
        }
    ]
    # If you installed these from PyPI directly (or just ran setup.py or pip to install this), then
    # no changes have been made, so you don't need to stress out about that.
    license_str = ""
    for dep in license_list:
        to_add = f"{dep['name']}, licensed under "
        if markdown_links:
            to_add += f" [{dep['license']}]({dep['link']})"
        else:
            to_add += f"{dep['license']} ({dep['link']})"
        if dep['changes']:
            to_add += ", " + dep['changes'] + "\n"
        license_str += to_add
    return license_str
