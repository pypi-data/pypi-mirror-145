import json
import re
from datetime import datetime
from booru import __version__


class Api():
    """Api class

    This class is used to parse the data from the api.

    Attributes:
        gelbooru (str): The base url for gelbooru.
        rule34 (str): The base url for rule34.
        tbib (str): The base url for tbib.
        safebooru (str): The base url for safebooru.
        xbooru (str): The base url for xbooru.
        realbooru (str): The base url for realbooru.
        hypnohub (str): The base url for hypnohub.
        danbooru (str): The base url for danbooru.
        yandere (str): The base url for yandere.
        konachan (str): The base url for konachan.
        konachan_net (str): The base url for konachan.net.
        e621 (str): The base url for e621.
        e926 (str): The base url for e926.
        derpibooru (str): The base url for derpibooru.
        behoimi (str): The base url for behoimi.

        e_handling_limit (str): The error message for the limit.
        e_handling_sameval (str): The error message for the same values.
        e_handling_cantparse (str): The error message for the parsing.
        e_handling_null (str): The error message for the null.
    """

    def __init__(self,
                 BASE_GELBOORU: str = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index",
                 BASE_RULE34: str = f"https://rule34.xxx/index.php?page=dapi&s=post&q=index",
                 BASE_TBIB: str = f"https://tbib.org/index.php?page=dapi&s=post&q=index",
                 BASE_SAFEBOORU: str = f"https://safebooru.org/index.php?page=dapi&s=post&q=index",
                 BASE_XBOORU: str = f"https://xbooru.com/index.php?page=dapi&s=post&q=index",
                 BASE_REALBOORU: str = f"https://realbooru.com/index.php?page=dapi&s=post&q=index",
                 BASE_HYPNOHUB: str = f"https://hypnohub.net/index.php?page=dapi&s=post&q=index",

                 BASE_DANBOORU: str = f"https://danbooru.donmai.us/posts.json",
                 BASE_YANDERE: str = f"https://yande.re/post.json",
                 BASE_KONACHAN: str = f"https://konachan.net/post.json",
                 BASE_KONACHAN_NET: str = f"https://konachan.net/post.json",

                 BASE_E621: str = f"https://e621.net/posts.json",
                 BASE_E926: str = f"https://e926.net/posts.json",
                 BASE_DERPIBOORU: str = f"https://derpibooru.org/api/v1/json/search/images",
                 BASE_BEHOIMI: str = f"http://behoimi.org/post/index.json",


                 e_handling_limit: str = "there is a hard limit of 100 posts per request.",
                 e_handling_sameval: str = "block values should not be hit to the query",
                 e_handling_cantparse: str = "failed to get data, the api is misleading",
                 e_handling_null: str = "no results, make sure you spelled everything right.",

                 BASE_headers={
                     'User-Agent': f'booru/v{__version__} (https://pypi.org/project/booru);',
                     'From': 'anakmancasan@gmail.com',
                 }

                 ):

        self.gelbooru = BASE_GELBOORU
        self.rule34 = BASE_RULE34
        self.tbib = BASE_TBIB
        self.safebooru = BASE_SAFEBOORU
        self.xbooru = BASE_XBOORU
        self.realbooru = BASE_REALBOORU
        self.hypnohub = BASE_HYPNOHUB
        self.danbooru = BASE_DANBOORU
        self.yandere = BASE_YANDERE
        self.konachan = BASE_KONACHAN
        self.konachan_net = BASE_KONACHAN_NET
        self.e621 = BASE_E621
        self.e926 = BASE_E926
        self.derpibooru = BASE_DERPIBOORU
        self.behoimi = BASE_BEHOIMI

        self.error_handling_limit = e_handling_limit
        self.error_handling_sameval = e_handling_sameval
        self.error_handling_cantparse = e_handling_cantparse
        self.error_handling_null = e_handling_null
        self.headers = BASE_headers


BASE_URL = Api()


def list_api():
    """Returns the api url.

    Returns
    -------
    list
    """
    # create this list for mocking
    api_list = [
        BASE_URL.gelbooru,
        BASE_URL.rule34,
        BASE_URL.tbib,
        BASE_URL.safebooru,
        BASE_URL.xbooru,
        BASE_URL.realbooru,
        BASE_URL.hypnohub,
        BASE_URL.danbooru,
        BASE_URL.yandere,
        BASE_URL.konachan,
        BASE_URL.konachan_net,
        BASE_URL.e621,
        BASE_URL.e926,
        BASE_URL.derpibooru,
        BASE_URL.behoimi
    ]
    return api_list


def better_object(parser: dict):
    """Converts the json object to a more readable object.

    Parameters
    ----------
    parser : dict

    Returns
    -------
    dict

    """
    return json.dumps(parser, sort_keys=True, indent=4, ensure_ascii=False)


def parse_image(raw_object: dict):
    """Return a lists instead extended json object.

    Parameters
    ----------
    obj : dict
        The object to be parsed.

    Returns
    -------
    list
    """
    if 'post' not in raw_object:
        data = raw_object

    elif 'post' in raw_object:
        data = raw_object['post']

    try:
        images = [i['file_url'] for i in data]

    except:
        images = [i['file']['url'] for i in data]  # furry stuff sigh

    return images


def get_hostname(url: str):
    """Returns the site of the url.

    Parameters
    ----------
    url : str

    Returns
    -------
    str
    """
    return re.sub(r'(.*://)?([^/?]+).*', '\g<1>\g<2>', url)
