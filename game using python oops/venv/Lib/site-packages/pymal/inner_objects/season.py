__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

import singleton_factory

from pymal import consts
from pymal import decorators

__all__ = ['Season']


class Season(object, metaclass=singleton_factory.SingletonFactory):
    """
    Lazy load of season data.
    
    Attributes:
        animes - a frozenset of animes.
        year - the season year.
        season_name - The season name. Can be 'Winter', 'Spring', 'Summer' or 'Fall'.
    """
    __all__ = ['animes', 'reload']

    __SEASON_URL = "http://malupdater.com/MalUpdater/Seasons/{0:d}_{1:s}.xml"
    __SEAONS_NAME_TO_START_MONTH = {
        'Winter': 1,
        'Spring': 4,
        'Summer': 7,
        'Fall': 10
    }

    def __init__(self, season_name: str, year: int or str):
        """
        :param season_name: the name of the season. see __SEAONS_NAME_TO_START_MONTH keys.
        :type season_name: str
        :param year: the year of the season
        :type year: int or str
        """
        import time
        from pymal import exceptions

        self.year = int(year)
        self.season_name = season_name.title()
        if self.season_name not in self.__SEAONS_NAME_TO_START_MONTH:
            raise exceptions.NotASeasonError(season_name)
        self.url = self.__SEASON_URL.format(self.year, self.season_name)

        self._is_loaded = False
        self.__animes = frozenset()

        month = str(self.__SEAONS_NAME_TO_START_MONTH[self.season_name])
        start_time_string = str(year) + ' ' + month
        self.start_time = time.strptime(start_time_string, '%Y %m')

    @property
    @decorators.load
    def animes(self) -> frozenset:
        """
        :return: all the animes in this season
        :rtype: frozenset
        """
        return self.__animes

    def reload(self):
        """
        fetching data.
        """
        import requests
        import bs4

        from pymal import anime

        sock = requests.get(self.url)
        xml = bs4.BeautifulSoup(sock.text)
        animes_xml = frozenset(xml.body.findAll(name='anime', recursive=False))
        animes_xml_with_id = frozenset(filter(lambda x: x.malid.text.isdigit(), animes_xml))
        if consts.DEBUG and 0 != len(animes_xml - animes_xml_with_id):
            print("animes with no id:", animes_xml - animes_xml_with_id)
        animes_ids = map(lambda x: int(x.malid.text), animes_xml_with_id)
        self.__animes = frozenset(map(lambda x: anime.Anime(x), animes_ids))

    def __iter__(self):
        return iter(self.animes)

    def __len__(self):
        return len(self.animes)

    def __hash__(self):
        import hashlib

        hash_md5 = hashlib.md5()
        hash_md5.update(str(self.year).encode())
        hash_md5.update(self.season_name.encode())
        return int(hash_md5.hexdigest(), 16)

    def __repr__(self):
        return "<{0:s} {1:s} {2:d}>".format(self.__class__.__name__,
                                            self.season_name, self.year)
