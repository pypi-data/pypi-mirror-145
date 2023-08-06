import requests
import json
import re
from ..utils.parser import Api, better_object, parse_image, get_hostname
from random import shuffle

Booru = Api()


# note: if your application rely on displaying images, you should implement a 'sync' stuff to behoimi.org itself
# these referer request just help you out to interacts with the API, not for displaying images

class Behoimi(object):
    """ 3d booru / Behoimi wrapper

    Methods
    -------
    search : function
        Search and gets images from behoimi.

    get_image_only : function
        Gets images, image urls only from behoimi.

    """
    @staticmethod
    def mock(site: str, params: dict):
        bypass = requests.get(site, params,
                              headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1)',
                                       'Referer': 'http://behoimi.org/data/ff/f3/',
                                       'From': 'anakmancasan@gmail.com'})
        return bypass

    @staticmethod
    def append_obj(raw_object: dict):
        """ Extends new object to the raw dict

        Parameters
        ----------
        raw_object : dict
            The raw object returned by behoimi.

        Returns
        -------
        str
            The new value of the raw object
        """
        for i in range(len(raw_object)):
            raw_object[i][
                'post_url'] = f"{get_hostname(Booru.behoimi)}/post/show/{raw_object[i]['id']}"

        return raw_object

    def __init__(self):
        self.specs = {}

    async def search(self, query: str, limit: int = 100, page: int = 1, random: bool = True):

        """ Search and gets images from behoimi.

        Parameters
        ----------
        query : str
            The query to search for.

        limit : int
            The limit of images to return.

        page : int
            The number of desired page

        random : bool
            Shuffle the whole dict, default is True.

        Returns
        -------
        dict
            The json object returned by behoimi.
        """

        if limit > 100:
            raise ValueError(Booru.error_handling_limit)

        else:
            self.query = query

        self.specs['tags'] = str(self.query)
        self.specs['limit'] = str(limit)
        self.specs['page'] = str(page)

        self.data = Behoimi.mock(Booru.behoimi, params=self.specs)

        self.final = json.loads(better_object(
            self.data.json()), encoding="utf-8")

        try:
            if random:
                self.not_random = Behoimi.append_obj(self.final)
                shuffle(self.not_random)
                return better_object(self.not_random)

            else:
                return better_object(Behoimi.append_obj(self.final))

        except Exception as e:
            raise ValueError(f'Failed to get data: {e}')

    async def get_image_only(self, query: str, limit: int = 100, page: int = 1):

        """ Gets images, meant just image urls from behoimi.

        Parameters
        ----------
        query : str
            The query to search for.

        limit : int
            The limit of images to return.

        page : int
            The number of desired page

        Returns
        -------
        dict
            The json object returned by behoimi.

        """

        if limit > 100:
            raise ValueError(Booru.error_handling_limit)

        else:
            self.query = query

        self.specs['tags'] = str(self.query)
        self.specs['limit'] = str(limit)
        self.specs['page'] = str(page)

        try:
            self.data = Behoimi.mock(Booru.behoimi, params=self.specs)
            self.final = json.loads(better_object(
                self.data.json()), encoding="utf-8")

            self.not_random = parse_image(self.final)
            shuffle(self.not_random)
            return better_object(self.not_random)

        except Exception as e:
            print(f'Failed to get data: {e}')
