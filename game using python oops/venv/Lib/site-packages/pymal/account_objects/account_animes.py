__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

from urllib import request

from pymal.consts import HOST_NAME
from pymal import decorators
from pymal.types import ReloadedSet

__all__ = ['AccountAnimes']


class AccountAnimes(ReloadedSet.ReloadedSetSingletonFactory):
    """
    A slow loading of an account anime list.

    :ivar watching: :class:`frozenset` of the watching animes.
    :ivar completed: :class:`frozenset` of the completed animes.
    :ivar on_hold: :class:`frozenset` of the "on hold" animes.
    :ivar dropped: :class:`frozenset` of the dropped animes.
    :ivar plan_to_watch: :class:`frozenset` of th "plan to watch" animes.
    """

    __URL = request.urljoin(HOST_NAME, "animelist/{0:s}&status=")

    def __init__(self, account):
        """
        :param account: Which account this anime list is connected to.
        :type account: :class:`account.Account`
        """
        self.__account = account
        self.__url = self.__URL.format(account.username)

        self.__watching = frozenset()
        self.__completed = frozenset()
        self.__on_hold = frozenset()
        self.__dropped = frozenset()
        self.__plan_to_watch = frozenset()

        self.map_of_lists = {
            1: self.__watching,
            2: self.__completed,
            3: self.__on_hold,
            4: self.__dropped,
            6: self.__plan_to_watch,

            '1': self.__watching,
            '2': self.__completed,
            '3': self.__on_hold,
            '4': self.__dropped,
            '6': self.__plan_to_watch,

            'watching': self.__watching,
            'completed': self.__completed,
            'onhold': self.__on_hold,
            'dropped': self.__dropped,
            'plantowatch': self.__plan_to_watch,
        }

        self._is_loaded = False

    @property
    @decorators.load
    def watching(self) -> frozenset:
        """
        :return: The watching list
        :rtype: frozenset
        """
        return self.__watching

    @property
    @decorators.load
    def completed(self) -> frozenset:
        """
        :return: The completed list
        :rtype: frozenset
        """
        return self.__completed

    @property
    @decorators.load
    def on_hold(self) -> frozenset:
        """
        :return: The on hold list
        :rtype: frozenset
        """
        return self.__on_hold

    @property
    @decorators.load
    def dropped(self) -> frozenset:
        """
        :return: The dropped list
        :rtype: frozenset
        """
        return self.__dropped

    @property
    @decorators.load
    def plan_to_watch(self) -> frozenset:
        """
        :return: The plan to watch list
        :rtype: frozenset
        """
        return self.__plan_to_watch

    @property
    def _values(self) -> frozenset:
        """
        :return: The all the animes
        :rtype: frozenset
        """
        return self.watching | self.completed | self.on_hold | self.dropped |\
               self.plan_to_watch

    def reload(self):
        """
        reloading data from MAL.
        """
        self.__watching = self.__get_my_animes(1)
        self.__completed = self.__get_my_animes(2)
        self.__on_hold = self.__get_my_animes(3)
        self.__dropped = self.__get_my_animes(4)
        self.__plan_to_watch = self.__get_my_animes(6)

        self._is_loaded = True

    def __get_my_animes(self, status: int) -> frozenset:
        import bs4

        if self.__account.is_auth:
            data = self.__account.auth_connect(self.__url + str(status))
        else:
            data = self.__account.connect(self.__url + str(status))
        body = bs4.BeautifulSoup(data).body

        main_div = body.find(name='div', attrs={'id': 'list_surround'})
        tables = main_div.findAll(name='table', reucrsive=False)
        if 4 >= len(tables):
            return frozenset()
        rows = tables[3: -1]

        return frozenset(map(self.__parse_obj_table, rows))

    def __parse_obj_table(self, div):
        from urllib import parse

        from pymal.account_objects.my_anime import MyAnime as obj

        links_div = div.findAll(name='td', recorsive=False)[1]

        link = links_div.find(name='a', attrs={'class': 'animetitle'})
        link_id = int(link['href'].split('/')[2])

        if self.__account.is_auth:
            my_link = links_div.find(name='a', attrs={'class': 'List_LightBox'})
            _, query = parse.splitquery(my_link['href'])
            my_link_id = int(parse.parse_qs(query)['id'][0])
        else:
            my_link_id = 0

        return obj(link_id, my_link_id, self.__account)

    def __repr__(self):
        return "<User animes' number is {0:d}>".format(len(self))

    def __hash__(self):
        import hashlib

        hash_md5 = hashlib.md5()
        hash_md5.update(self.__account.username.encode())
        hash_md5.update(self.__class__.__name__.encode())
        return int(hash_md5.hexdigest(), 16)
