__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

from singleton3 import Singleton

from pymal import decorators

__all__ = ['Seasons']


class Seasons(object, metaclass=Singleton):
    """
    Lazy making of Season from online db.
    
    :ivar seasons: :class:`frozenset` of :class:`inner_objects..season.Season`.
    """

    __SEASONS_URL = 'http://malupdater.com/MalUpdater/Seasons/index.txt'

    def __init__(self):
        self.__seasons = frozenset()
        self._is_loaded = False

    @property
    @decorators.load
    def seasons(self) -> frozenset:
        return self.__seasons

    def reload(self):
        """
        reloading all the known seasons.
        """
        import requests
        import bs4

        from pymal.inner_objects import season

        sock = requests.get(self.__SEASONS_URL)
        body = bs4.BeautifulSoup(sock.text).body

        seasons_lines = body.text.splitlines()
        splitted_lines = map(lambda x: reversed(x.split('_')), seasons_lines)
        seasons = map(lambda x: season.Season(*tuple(x)), splitted_lines)
        self.__seasons = frozenset(seasons)

        self._is_loaded = True

    def __contains__(self, item) -> bool:
        return any(map(lambda x: item in x, self.seasons))

    def __repr__(self):
        import os

        return (os.linesep + '\t').join(map(str, ['<Seasons>'] +
                                            list(self.seasons)))

    def __iter__(self):
        return iter(self.seasons)

    def __len__(self) -> int:
        return sum(map(lambda x: len(x), self.seasons))
