__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

from urllib import request

import requests
import singleton_factory

from pymal import global_functions
from pymal.decorators import load
from pymal.consts import HOST_NAME

__all__ = ['Account']


class Account(object, metaclass=singleton_factory.SingletonFactory):
    """
    Object that keeps all the account data in MAL.
    """

    __AUTH_CHECKER_URL =\
        request.urljoin(HOST_NAME, r'api/account/verify_credentials.xml')

    __MY_LOGIN_URL = request.urljoin(HOST_NAME, 'login.php')
    __DATA_FORM = 'username={0:s}&password={1:s}&cookie=1&sublogin=+Login+'

    def __init__(self, username: str, password: str or None=None):
        """
        :param username: The account username.
        :type username: str
        :param password: Required for quick connection, instead of calling later change_password.
        :type password: str or None
        """
        from pymal.account_objects import account_animes, account_mangas

        self.__username = username
        self.__password = password
        self.connect = global_functions.connect
        self.__user_id = None
        self.__auth_object = None

        self._main_profile_url = request.urljoin(HOST_NAME, 'profile/{0:s}'.format(self.username))

        self.__animes = account_animes.AccountAnimes(self)
        self.__mangas = account_mangas.AccountMangas(self)
        self.__friends = None
        self.__image_url = ""

        self.__session = global_functions.generate_session()

        self._is_loaded = False

        if password is not None:
            self.change_password(password)

    @property
    def username(self) -> str:
        """

        :returns: the user name.
        :rtype: str
        """
        return self.__username

    @property
    def user_id(self) -> int:
        """
        :returns: the user id. If unknown loading it.
        :rtype: int
        """
        if self.__user_id is None:
            import bs4

            ret = self.connect(self._main_profile_url)
            html = bs4.BeautifulSoup(ret)
            bla = html.find(name='input', attrs={'name': 'profileMemId'})
            self.__user_id = int(bla['value'])
        return self.__user_id

    @property
    def mangas(self):
        """
        :returns: list of account's mangas.
        :rtype: :class:`account_objects.account_mangas.AccountMangas`
        """
        return self.__mangas

    @property
    def animes(self):
        """
        :returns: list of account's animes.
        :rtype: :class:`account_objects.account_animes.AccountAnimes`
        """
        return self.__animes

    @property
    def friends(self) -> set:
        """
        :returns: list of account's friends.
        :rtype: :class:`account_objects.account_friends.AccountFriends`
        """
        from pymal.account_objects import account_friends

        if self.__friends is None:
            self.__friends = account_friends.AccountFriends(self)
        return self.__friends

    def search(self, search_line: str, is_anime: bool=True) -> map:
        """
        Searching like regular search but switching all the object in "my" lists to the "my" objects.

        :param search_line: the search line.
        :type search_line: str
        :param is_anime: True is searching for anime, False for manga.
        :type is_anime: bool
        :returns: searched objects
        :rtype: map
        """
        from pymal import searches

        if is_anime:
            results = searches.search_animes(search_line)
            account_object_list = self.animes
        else:
            results = searches.search_mangas(search_line)
            account_object_list = self.mangas

        def get_object(result):
            if result not in account_object_list:
                return result
            # if account_object_list was set:
            #     return account_object_list.intersection([result]).pop()
            return list(filter(
                lambda x: x == result,
                account_object_list
            ))[0]
        return map(get_object, results)

    def change_password(self, password: str) -> bool:
        """
        Checking if the new password is valid

        :param password: password
        :type password: str
        :returns: True if password is right.
        :rtype: bool
        :exception exceptions.FailedToParseError: when failed
        """
        from xml.etree import ElementTree
        from requests.auth import HTTPBasicAuth
        from pymal import exceptions

        self.__auth_object = HTTPBasicAuth(self.username, password)
        data = self.auth_connect(self.__AUTH_CHECKER_URL)
        if data == 'Invalid credentials':
            self.__auth_object = None
            self.__password = None
            return False
        xml_user = ElementTree.fromstring(data)

        if 'user' != xml_user.tag:
            raise exceptions.FailedToParseError('user == {0:s}'.format(xml_user.tag))
        l = list(xml_user)
        xml_username = l[1]
        if 'username' != xml_username.tag:
            raise exceptions.FailedToParseError('username == {0:s}'.format(xml_username.tag))
        if self.username != xml_username.text.strip():
            raise exceptions.FailedToParseError('username = {0:s}'.format(xml_username.text.strip()))

        xml_id = l[0]
        if 'id' != xml_id.tag:
            raise exceptions.FailedToParseError('id == {0:s}'.format(xml_id.tag))
        if self.user_id != int(xml_id.text):
            raise exceptions.FailedToParseError()

        self.__password = password

        data_form = self.__DATA_FORM.format(self.username, password).encode('utf-8')
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'name': 'loginForm',
        }

        self.auth_connect(self.__MY_LOGIN_URL, data=data_form, headers=headers)

        return True

    def auth_connect(self, url: str, data: str or None=None,
                     headers: dict or None=None) -> str:
        """
        :param url: The url to get.
        :type url: str
        :param data: The data to pass (will change the request to "POST")
        :type data: str or None
        :param headers: Headers for the request.
        :type headers: dict or None
        :returns: data after using the account authenticate to get the data.
        :rtype: str
        """
        from pymal import exceptions

        if not self.is_auth:
            raise exceptions.UnauthenticatedAccountError(self.username)
        return global_functions._connect(url, data=data, headers=headers,
                                         auth=self.__auth_object, session=self.__session).text.strip()

    @property
    @load
    def image_url(self):
        """
        :return: path for the image of the avatar of the account.
        :rtype: str
        """
        return self.__image_url

    def get_image(self):
        """
        :return: image of the account's avatar
        :rtype: :class:`PIL.Image.Image`
        """
        import io

        from PIL import Image

        sock = requests.get(self.image_url)
        data = io.BytesIO(sock.content)
        return Image.open(data)

    def reload(self):
        """
        reloading account image (all the other things are already lazy load!
        """
        div = global_functions.get_content_wrapper_div(self._main_profile_url, self.connect)
        profile_leftcell = div.table.tbody.tr.find(name="td", attrs={"class": "profile_leftcell"}, recursive=False)
        self.__image_url = profile_leftcell.div.img['src']

    @property
    def is_auth(self) -> bool:
        """
        :returns: True if the password is right (and able to authenticate).
        :rtype: bool
        """
        return self.__auth_object is not None

    def __repr__(self):
        return "<Account username: {0:s}>".format(self.username)

    def __hash__(self):
        import hashlib

        hash_md5 = hashlib.md5()
        hash_md5.update(self.username.encode())
        return int(hash_md5.hexdigest(), 16)

    def __format__(self, format_spec):
        return str(self).__format__(format_spec)
