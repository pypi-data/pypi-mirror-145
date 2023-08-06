import json
import re
from datetime import datetime


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

        e_handling_limit (str): The error message for the limit.
        e_handling_sameval (str): The error message for the same values.
    """

    def __init__(self,
                 BASE_GELBOORU: str = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index",
                 BASE_RULE34: str = f"https://rule34.xxx/index.php?page=dapi&s=post&q=index",
                 BASE_TBIB: str = f"https://tbib.org/index.php?page=dapi&s=post&q=index",
                 BASE_SAFEBOORU: str = f"https://safebooru.org/index.php?page=dapi&s=post&q=index",
                 BASE_XBOORU: str = f"https://xbooru.com/index.php?page=dapi&s=post&q=index",
                 BASE_REALBOORU: str = f"https://realbooru.com/index.php?page=dapi&s=post&q=index",

                 e_handling_limit: str = "limit cannot be greater than 100",
                 e_handling_sameval: str = "block value should not be in the query",
                 e_handling_cantparse: str = "failed to get data, the api is misleading"

                 ):

        self.gelbooru = BASE_GELBOORU
        self.rule34 = BASE_RULE34
        self.tbib = BASE_TBIB
        self.safebooru = BASE_SAFEBOORU
        self.xbooru = BASE_XBOORU
        self.realbooru = BASE_REALBOORU

        self.error_handling_limit = e_handling_limit
        self.error_handling_sameval = e_handling_sameval
        self.error_handling_cantparse = e_handling_cantparse


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
        BASE_URL.realbooru
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

    images = [i['file_url'] for i in data]
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
