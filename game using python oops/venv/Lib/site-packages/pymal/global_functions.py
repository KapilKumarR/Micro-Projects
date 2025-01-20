__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

from urllib import request
import time

import requests
try:
    import httpcache
except ImportError:
    httpcache = None
import bs4

from pymal import consts
from pymal import exceptions

__all__ = ['connect', 'get_next_index', 'make_set', 'check_side_content_div', 'get_content_wrapper_div']


def generate_session():
    session = requests.session()
    if httpcache is not None:
        session.mount('http://', httpcache.CachingHTTPAdapter())
    return session

__SESSION = generate_session()


def url_fixer(url: str) -> str:
    url = url.encode('utf-8')
    for i in range(128, 256):
        url = url.replace(bytes([i]), '%{0:X}'.format(i).encode("utf-8"))
    return url.decode('utf-8')


def _connect(url: str, data: str=None, headers: dict or None=None,
             auth=None, session: requests.session=__SESSION) -> requests.Response:
    """
    :param url: url
    :type url: :class:`str`
    :param data: data to post
    :type data: :class:`str`
    :param headers: headers to send
    :type headers: :class:`dict` or :class:`None`
    :param auth: the authenticate for the session.
    :type auth: :class:`requests.auth.HTTPBasicAuth`
    :param session: the session to connect to, otherwise using the default ones.
    :type session: :class:`requests.Session`

    :return: the respond of the connection
    :rtype: :class:`requests.Response`
    """
    if headers is None:
        headers = dict()

    url = url_fixer(url)

    headers['User-Agent'] = consts.USER_AGENT
    if data is not None:
        sock = session.post(url, data=data, headers=headers, auth=auth)
    else:
        sock = session.get(url, headers=headers, auth=auth)
    return sock


def connect(url: str, data: str=None, headers: dict or None=None,
            auth=None) -> str:
    """
    :param url: url
    :param data: data to post
    :param headers: headers to send
    :rtype : responded data
    """
    return _connect(url, data, headers, auth).text.strip()


def get_next_index(i: int, list_of_tags: list) -> int:
    """
    return the i after the next <br/>

    :type i: int
    :param i: an index
    :type list_of_tags: list
    :param list_of_tags: list of tags to check the i on
    :rtype: int
    """
    while i < len(list_of_tags) and list_of_tags[i].name != 'br':
        i += 1
    return i + 1


def make_set(self_set: set, i: int, list_of_tags: list) -> int:
    """
    return the index after the next <br/> and inserting all the link until it.

    :type self_set: set
    :param self_set: a list to append links to
    :type i: int
    :param i: an index
    :type list_of_tags: list
    :param list_of_tags: list of tags to check the index on
    :rtype: int
    """
    from pymal import anime
    from pymal import manga

    n_i = get_next_index(i, list_of_tags)
    for i in range(i + 1, n_i, 2):
        if 'a' != list_of_tags[i].name:
            exceptions.FailedToParseError(list_of_tags[i].name)
        tag_href = list_of_tags[i]['href']
        if '/anime/' in tag_href:
            obj = anime.Anime
            splitter = '/anime/'
        elif '/manga/' in tag_href:
            obj = manga.Manga
            splitter = '/manga/'
        else:
            print('unknown tag', tag_href)
            self_set.add(
                request.urljoin(consts.HOST_NAME, list_of_tags[i]['href']))
            continue
        obj_id = tag_href.split(splitter)[1].split('/')[0]
        if not obj_id.isdigit():
            print('unknown tag', tag_href)
            continue
        self_set.add(obj(int(obj_id)))
    return n_i


def check_side_content_div(expected_text: str, div_node: bs4.element.Tag):
    span_node = div_node.span
    if span_node is None:
        raise exceptions.FailedToParseError(div_node)
    expected_text += ":"
    if ['dark_text'] != span_node['class']:
        return False
    return expected_text == span_node.text.strip()


def __get_myanimelist_div(url: str, connection_function) -> bs4.element.Tag:
    got_robot = False
    for try_number in range(consts.RETRY_NUMBER):
        time.sleep(consts.RETRY_SLEEP)
        data = connection_function(url)
        html = bs4.BeautifulSoup(data, "html5lib").html
        if html.head.find(name="meta", attrs={"name": "robots"}) is not None:
            got_robot = True
            continue
        div = html.body.find(name="div", attrs={"id": 'myanimelist'})
        if div is not None:
            return div
    if got_robot:
        raise exceptions.GotRobotError()
    raise exceptions.FailedToParseError("my anime list div wasn't found")


def get_content_wrapper_div(url: str, connection_function) -> bs4.element.Tag:
    myanimelist_div = __get_myanimelist_div(url, connection_function)

    # Getting content wrapper <div>
    content_wrapper_div = myanimelist_div.find(
        name="div", attrs={"id": "contentWrapper"}, recursive=False)
    if content_wrapper_div is None:
        raise exceptions.FailedToParseError(myanimelist_div)
    return content_wrapper_div


def make_start_and_end_time(start_and_end_string: str) -> tuple:
    """
    getting mal site airing / publishing format and return it as tuple(int, int)
    """
    splited = start_and_end_string.split('to')
    if len(splited) == 1:
        start_time = splited[0].strip()
        end_time = start_time
    else:
        start_time, end_time = splited
    start_time, end_time = start_time.strip(), end_time.strip()
    return make_time(start_time), make_time(end_time)


def make_time(time_string: str) -> int:
    """
    getting mal site time string format and return it as int
    """
    if '?' == time_string or consts.MALAPPINFO_NONE_TIME == time_string:
        return float('inf')
    if time_string.isdigit():
        return int(time_string)
    try:
        start_time = time.strptime(time_string, consts.SHORT_SITE_FORMAT_TIME)
    except ValueError:
        try:
            start_time = time.strptime(time_string, consts.LONG_SITE_FORMAT_TIME)
        except ValueError:
            time_string = time_string[:4] + time_string[4:].replace('00', '01')
            start_time = time.strptime(time_string, consts.MALAPPINFO_FORMAT_TIME)
    return time.mktime(start_time)


def make_counter(counter_string: str) -> int or float:
    """
    getting mal site counter string format and return it as int
    """
    if 'Unknown' == counter_string:
        return float('inf')
    return int(counter_string)
