__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

from urllib import request

import requests
import bs4
import singleton_factory

from pymal import decorators
from pymal import consts
from pymal import global_functions

__all__ = ['Anime']


class Anime(object, metaclass=singleton_factory.SingletonFactory):
    """
    Object that keeps all the anime data in MAL.

    :ivar image_url: :class:`str`
    :ivar title: :class:`str`
    :ivar english: :class:`str`
    :ivar synonyms: :class:`str`
    :ivar japanese: :class:`str`
    :ivar type: :class:`str`
    :ivar status: :class:`int`
    :ivar start_time: :class:`int`
    :ivar end_time: :class:`int`
    :ivar creators: :class:`dict`
    :ivar genres: :class:`dict`
    :ivar duration: :class:`int`
    :ivar score: :class:`float`
    :ivar rank: :class:`int`
    :ivar popularity: :class:`int`
    :ivar rating: :class:`str`
    :ivar episodes: :class:`int`
    :ivar synopsis: :class:`str`

    :ivar adaptations: :class:`frozenset`
    :ivar characters: :class:`frozenset`
    :ivar sequels: :class:`frozenset`
    :ivar prequels: :class:`frozenset`
    :ivar spin_offs: :class:`frozenset`
    :ivar alternative_versions: :class:`frozenset`
    :ivar side_stories: :class:`frozenset`
    :ivar summaries: :class:`frozenset`
    :ivar others: :class:`frozenset`
    :ivar parent_stories: :class:`frozenset`
    :ivar alternative_settings: :class:`frozenset`
    :ivar full_stories: :class:`frozenset`
    """

    __GLOBAL_MAL_URL = request.urljoin(consts.HOST_NAME, "anime/{0:d}")
    __MY_MAL_ADD_URL = request.urljoin(
        consts.HOST_NAME, 'api/animelist/add/{0:d}.xml')

    def __init__(self, mal_id: int):
        """
        :param mal_id: the anime id in mal.
        :type mal_id: int
        """
        self.__id = mal_id
        self._is_loaded = False

        self.__mal_url = self.__GLOBAL_MAL_URL.format(self.__id)

        # Getting staff from html
        # staff from side content
        self.__title = ''
        self.__image_url = ''
        self.__english = ''
        self.__synonyms = ''
        self.__japanese = ''
        self.__type = ''
        self.__status = 0
        self.__start_time = 0
        self.__end_time = 0
        self.__creators = dict()
        self.__genres = dict()
        self.__duration = 0
        self.__score = 0.0
        self.__rank = 0
        self.__popularity = 0

        self.__rating = ''
        self.__episodes = 0

        # staff from main content
        # staff from row 1
        self.__synopsis = ''

        # staff from row 2
        self.__adaptations = set()
        self.__characters = set()
        self.__sequels = set()
        self.__prequels = set()
        self.__spin_offs = set()
        self.__alternative_versions = set()
        self.__side_stories = set()
        self.__summaries = set()
        self.__others = set()
        self.__parent_stories = set()
        self.__alternative_settings = set()
        self.__full_stories = set()

        self.related_str_to_set_dict = {
            'Adaptation:': self.__adaptations,
            'Character:': self.__characters,
            'Sequel:': self.__sequels,
            'Prequel:': self.__prequels,
            'Spin-off:': self.__spin_offs,
            'Alternative version:': self.__alternative_versions,
            'Side story:': self.__side_stories,
            'Summary:': self.__summaries,
            'Other:': self.__others,
            'Parent story:': self.__parent_stories,
            'Alternative setting:': self.__alternative_settings,
            'Full story:': self.__full_stories,
        }

    @property
    def id(self) -> int:
        """
        :return: The id of the anime.
        :rtype: :class:`int`
        """
        return self.__id

    @property
    @decorators.load
    def title(self) -> str:
        return self.__title

    @property
    @decorators.load
    def image_url(self) -> str:
        return self.__image_url

    def get_image(self):
        """
        :return: The image of the anime
        :rtype: :class:`PIL.Image.Image`
        """
        import io

        from PIL import Image

        sock = requests.get(self.image_url)
        data = io.BytesIO(sock.content)
        return Image.open(data)

    @property
    @decorators.load
    def english(self) -> str:
        return self.__english

    @property
    @decorators.load
    def synonyms(self) -> str:
        return self.__synonyms

    @property
    @decorators.load
    def japanese(self) -> str:
        return self.__japanese

    @property
    @decorators.load
    def type(self) -> str:
        return self.__type

    @property
    @decorators.load
    def status(self) -> int:
        return self.__status

    @property
    @decorators.load
    def start_time(self) -> int:
        return self.__start_time

    @property
    @decorators.load
    def end_time(self) -> int:
        return self.__end_time

    @property
    @decorators.load
    def creators(self) -> dict:
        return self.__creators

    @property
    @decorators.load
    def genres(self) ->dict:
        return self.__genres

    @property
    @decorators.load
    def duration(self) -> int:
        return self.__duration

    @property
    @decorators.load
    def score(self) -> float:
        return self.__score

    @property
    @decorators.load
    def rank(self) -> int:
        return self.__rank

    @property
    @decorators.load
    def popularity(self) -> int:
        return self.__popularity

    @property
    @decorators.load
    def synopsis(self) -> str:
        return self.__synopsis

    # staff from main content
    @property
    @decorators.load
    def adaptations(self) -> frozenset:
        return frozenset(self.__adaptations)

    @property
    @decorators.load
    def characters(self) -> frozenset:
        return frozenset(self.__characters)

    @property
    @decorators.load
    def sequels(self) -> frozenset:
        return frozenset(self.__sequels)

    @property
    @decorators.load
    def prequels(self) -> frozenset:
        return frozenset(self.__prequels)

    @property
    @decorators.load
    def spin_offs(self) -> frozenset:
        return frozenset(self.__spin_offs)

    @property
    @decorators.load
    def alternative_versions(self) -> frozenset:
        return frozenset(self.__alternative_versions)

    @property
    @decorators.load
    def side_stories(self) -> frozenset:
        return frozenset(self.__side_stories)

    @property
    @decorators.load
    def summaries(self) -> frozenset:
        return frozenset(self.__summaries)

    @property
    @decorators.load
    def others(self) -> frozenset:
        return frozenset(self.__others)

    @property
    @decorators.load
    def parent_stories(self) -> frozenset:
        return frozenset(self.__parent_stories)

    @property
    @decorators.load
    def alternative_settings(self) -> frozenset:
        return frozenset(self.__alternative_settings)

    @property
    @decorators.load
    def full_stories(self) -> frozenset:
        return frozenset(self.__full_stories)

    @property
    @decorators.load
    def rating(self) -> int:
        return self.__rating

    @property
    @decorators.load
    def episodes(self) -> int:
        return self.__episodes

    def reload(self):
        """
        :exception exceptions.FailedToReloadError: when failed.
        """
        import os
        from pymal import exceptions

        # Getting content wrapper <div>
        content_wrapper_div = global_functions.get_content_wrapper_div(self.__mal_url, global_functions.connect)

        # Getting title <div>
        self.__title = content_wrapper_div.h1.contents[1].strip()

        # Getting content <div>
        content_div = content_wrapper_div.find(
            name="div", attrs={"id": "content"}, recursive=False)

        if content_div is None:
            raise exceptions.FailedToReloadError(content_wrapper_div)

        content_table = content_div.table

        contents = content_table.tbody.tr.findAll(name="td", recursive=False)

        # Data from side content
        side_content = contents[0]
        side_contents_divs = side_content.findAll(name="div", recursive=False)

        # Getting anime image url <img>
        img_div = side_contents_divs[0]
        img_link = img_div.find(name="a")
        if img_link is None:
            raise exceptions.FailedToReloadError(content_wrapper_div)
        self.__image_url = img_link.img['src']

        side_contents_divs_index = 4

        # english <div>
        english_div = side_contents_divs[side_contents_divs_index]
        if global_functions.check_side_content_div('English', english_div):
            english_span, self_english = english_div.contents
            self.__english = self_english.strip()
            side_contents_divs_index += 1
        else:
            self.__english = ''

        # synonyms <div>
        synonyms_div = side_contents_divs[side_contents_divs_index]
        if global_functions.check_side_content_div('Synonyms', synonyms_div):
            synonyms_span, self_synonyms = synonyms_div.contents
            self.__synonyms = self_synonyms.strip()
            side_contents_divs_index += 1
        else:
            self.__synonyms = ''

        # japanese <div>
        japanese_div = side_contents_divs[side_contents_divs_index]
        if global_functions.check_side_content_div('Japanese', japanese_div):
            japanese_span, self_japanese = japanese_div.contents
            self.__japanese = self_japanese.strip()
            side_contents_divs_index += 1
        else:
            self.__japanese = ''

        # type <div>
        type_div = side_contents_divs[side_contents_divs_index]
        if not global_functions.check_side_content_div('Type', type_div):
            raise exceptions.FailedToReloadError(content_wrapper_div)
        type_span, self_type = type_div.contents
        self.__type = self_type.strip()
        side_contents_divs_index += 1

        # episodes <div>
        episodes_div = side_contents_divs[side_contents_divs_index]
        if not global_functions.check_side_content_div('Episodes', episodes_div):
            raise exceptions.FailedToReloadError(content_wrapper_div)
        episodes_span, self_episodes = episodes_div.contents
        self.__episodes = global_functions.make_counter(self_episodes.strip())

        side_contents_divs_index += 1

        # status <div>
        status_div = side_contents_divs[side_contents_divs_index]
        if not global_functions.check_side_content_div('Status', status_div):
            raise exceptions.FailedToReloadError(content_wrapper_div)
        status_span, self.__status = status_div.contents
        self.__status = self.__status.strip()
        side_contents_divs_index += 1

        # aired <div>
        aired_div = side_contents_divs[side_contents_divs_index]
        if not global_functions.check_side_content_div('Aired', aired_div):
            raise exceptions.FailedToReloadError(content_wrapper_div)
        aired_span, aired = aired_div.contents
        self.__start_time, self.__end_time = global_functions.make_start_and_end_time(aired)
        side_contents_divs_index += 1

        # producers <div>
        producers_div = side_contents_divs[side_contents_divs_index]
        if not global_functions.check_side_content_div('Producers', producers_div):
            raise exceptions.FailedToReloadError(content_wrapper_div)
        for producer_link in producers_div.findAll(name='a'):
            self.__creators[producer_link.text.strip()] = producer_link['href']
        side_contents_divs_index += 1

        # genres <div>
        genres_div = side_contents_divs[side_contents_divs_index]
        if not global_functions.check_side_content_div('Genres', genres_div):
            raise exceptions.FailedToReloadError(content_wrapper_div)
        for genre_link in genres_div.findAll(name='a'):
            self.__genres[genre_link.text.strip()] = genre_link['href']
        side_contents_divs_index += 1

        # duration <div>
        duration_div = side_contents_divs[side_contents_divs_index]
        if not global_functions.check_side_content_div('Duration', duration_div):
            raise exceptions.FailedToReloadError(content_wrapper_div)

        duration_span, duration_string = duration_div.contents
        self.__duration = 0
        duration_parts = duration_string.strip().split('.')
        duration_parts = list(map(lambda x: x.strip(), duration_parts))[:-1]
        for duration_part in duration_parts:
            number, scale = duration_part.split()
            number = int(number)
            if scale == 'min':
                self.__duration += number
            elif scale == 'hr':
                self.__duration += number * 60
            else:
                raise exceptions.FailedToReloadError('scale {0:s} is unknown'.format(scale))
        side_contents_divs_index += 1

        # rating <div>
        rating_div = side_contents_divs[side_contents_divs_index]
        if not global_functions.check_side_content_div('Rating', rating_div):
            raise exceptions.FailedToReloadError(content_wrapper_div)
        rating_span, self.__rating = rating_div.contents
        self.__rating = self.__rating.strip()
        side_contents_divs_index += 1

        # score <div>
        score_div = side_contents_divs[side_contents_divs_index]
        if not global_functions.check_side_content_div('Score', score_div):
            raise exceptions.FailedToReloadError(content_wrapper_div)
        score_span, self_score = score_div.contents[:2]
        self.__score = float(self_score)
        side_contents_divs_index += 1

        # rank <div>
        rank_div = side_contents_divs[side_contents_divs_index]
        if not global_functions.check_side_content_div('Ranked', rank_div):
            raise exceptions.FailedToReloadError(content_wrapper_div)
        rank_span, self_rank = rank_div.contents[:2]
        self_rank = self_rank.strip()
        if not self_rank.startswith("#"):
            raise exceptions.FailedToReloadError(self_rank)
        self.__rank = int(self_rank[1:])
        side_contents_divs_index += 1

        # popularity <div>
        popularity_div = side_contents_divs[side_contents_divs_index]
        if not global_functions.check_side_content_div('Popularity', popularity_div):
            raise exceptions.FailedToReloadError(content_wrapper_div)
        popularity_span, self_popularity = popularity_div.contents[:2]
        self_popularity = self_popularity.strip()
        if not self_popularity.startswith("#"):
            raise exceptions.FailedToReloadError(self_popularity)
        self.__popularity = int(self_popularity[1:])

        # Data from main content
        main_content = contents[1]
        main_content_inner_divs = main_content.findAll(
            name='div', recursive=False)
        if 2 != len(main_content_inner_divs):
            raise exceptions.FailedToReloadError(
            "Got len(main_content_inner_divs) == {0:d}".format(
                len(main_content_inner_divs)))
        main_content_datas = main_content_inner_divs[
            1].table.tbody.findAll(name="tr", recursive=False)

        synopsis_cell = main_content_datas[0]
        main_content_other_data = main_content_datas[1]

        # Getting synopsis
        synopsis_cell = synopsis_cell.td
        synopsis_cell_contents = synopsis_cell.contents
        if 'Synopsis' != synopsis_cell.h2.text.strip():
            raise exceptions.FailedToReloadError(synopsis_cell.h2.text.strip())
        self.__synopsis = os.linesep.join([
            synopsis_cell_content.strip()
            for synopsis_cell_content in synopsis_cell_contents[1:-1]
            if isinstance(synopsis_cell_content, bs4.element.NavigableString)
        ])

        # Getting other data
        main_content_other_data = main_content_other_data.td
        other_data_kids = [i for i in main_content_other_data.children]

        # Getting all the data under 'Related Anime'
        index = 0
        index = global_functions.get_next_index(index, other_data_kids)
        if 'h2' == other_data_kids[index].name and\
           'Related Anime' == other_data_kids[index].text.strip():
            index += 1
            while other_data_kids[index + 1].name != 'br':
                index = global_functions.make_set(
                    self.related_str_to_set_dict[
                        other_data_kids[index].strip()],
                    index, other_data_kids)
        else:
            index -= 2
        next_index = global_functions.get_next_index(index, other_data_kids)

        if consts.DEBUG:
            if next_index - index != 2:
                raise exceptions.FailedToReloadError("{0:d} - {1:d}".format(next_index, index))
            index = next_index + 1

            # Getting all the data under 'Characters & Voice Actors'
            if 'h2' != other_data_kids[index].name:
                raise exceptions.FailedToReloadError('h2 == {0:s}'.format(other_data_kids[index].name))
            if 'Characters & Voice Actors' != other_data_kids[index].contents[-1]:
                raise exceptions.FailedToReloadError(other_data_kids[index].contents[-1])

        tag_for_reviews = main_content_other_data.find(text='More reviews').parent
        link_for_reviews = request.urljoin(consts.HOST_NAME, tag_for_reviews['href'])
        self.__parse_reviews(link_for_reviews)

        tag_for_recommendations = main_content_other_data.find(text='More recommendations').parent
        link_for_recommendations = request.urljoin(consts.HOST_NAME, tag_for_recommendations['href'])
        self.__parse_recommendations(link_for_recommendations)

        self._is_loaded = True

    def __parse_reviews(self, link_for_reviews: str):
        from pymal.inner_objects import review

        content_wrapper_div = global_functions.get_content_wrapper_div(link_for_reviews, global_functions.connect)
        content_div = content_wrapper_div.find(name="div", attrs={"id": "content"}, recursive=False)
        _,  main_cell = content_div.table.tbody.tr.findAll(name='td', recursive=False)
        _, reviews_data_div = main_cell.findAll(name='div', recursive=False)
        reviews_data = reviews_data_div.findAll(name='div', recursive=False)[2:-2]
        self.reviews = frozenset(map(review.Review, reviews_data))

    def __parse_recommendations(self, link_for_recommendations: str):
        from pymal.inner_objects import recommendation

        content_wrapper_div = global_functions.get_content_wrapper_div(link_for_recommendations, global_functions.connect)
        content_div = content_wrapper_div.find(name="div", attrs={"id": "content"}, recursive=False)
        _,  main_cell = content_div.table.tbody.tr.findAll(name='td', recursive=False)
        _, recommendations_data_div = main_cell.findAll(name='div', recursive=False)
        recommendations_data = recommendations_data_div.findAll(name='div', recursive=False)[2:-1]
        self.recommendations = frozenset(map(recommendation.Recommendation, recommendations_data))

    @property
    def MY_MAL_XML_TEMPLATE(self) -> str:
        return """<?xml version="1.0" encoding="UTF-8"?>
<entry>
    <episode>{0:d}</episode>
    <status>{1:d}</status>
    <score>{2:d}</score>
    <downloaded_episodes>{3:d}</downloaded_episodes>
    <storage_type>{4:d}</storage_type>
    <storage_value>{5:f}</storage_value>
    <times_rewatched>{6:d}</times_rewatched>
    <rewatch_value>{7:d}</rewatch_value>
    <date_start>{8:s}</date_start>
    <date_finish>{9:s}</date_finish>
    <priority>{10:d}</priority>
    <enable_discussion>{11:d}</enable_discussion>
    <enable_rewatching>{12:d}</enable_rewatching>
    <comments>{13:s}</comments>
    <fansub_group>{14:s}</fansub_group>
    <tags>{15:s}</tags>
</entry>"""

    def add(self, account):
        """
        :param account: the account to add him self anime.
        :type account: :class:`account.Account`
        :rtype: :class:`account_objects.my_anime.MyAnime`
        :exception exceptions.MyAnimeListApiAddError: when failed.
        """
        from pymal import exceptions

        data = self.MY_MAL_XML_TEMPLATE.format(
            0, 6, 0, 0, 0, 0, 0, 0, consts.MALAPI_NONE_TIME,
            consts.MALAPI_NONE_TIME, 0, False, False, '', '', ''
        )
        xml = ''.join(map(lambda x: x.strip(), data.splitlines()))
        delete_url = self.__MY_MAL_ADD_URL.format(self.id)
        ret = account.auth_connect(
            delete_url,
            data='data=' + xml,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        try:
            html_obj = bs4.BeautifulSoup(ret)
            if html_obj is None:
                raise exceptions.FailedToAddError(html_obj)

            head_obj = html_obj.head
            if head_obj is None:
                raise exceptions.FailedToAddError(head_obj)

            title_obj = head_obj.title
            if title_obj is None:
                raise exceptions.FailedToAddError(title_obj)

            data = title_obj.text
            if data is None:
                raise exceptions.FailedToAddError(data)

            my_id, string = data.split()
            if not my_id.isdigit():
                raise exceptions.FailedToAddError(my_id)
            if string != 'Created':
                raise exceptions.FailedToAddError(string)
        except exceptions.FailedToAddError:
            raise exceptions.MyAnimeListApiAddError(ret)

        from pymal.account_objects import my_anime
        return my_anime.MyAnime(self, my_id, account)

    def __eq__(self, other):
        if isinstance(other, Anime):
            return self.id == other.id
        elif isinstance(other, int):
            return self.id == other
        elif isinstance(other, str) and other.isdigit():
            return self.id == int(other)
        elif hasattr(other, 'id'):
            return self.id == other.id
        return False

    def __hash__(self):
        import hashlib

        hash_md5 = hashlib.md5()
        hash_md5.update(str(self.id).encode())
        hash_md5.update(b'Anime')
        return int(hash_md5.hexdigest(), 16)

    def __repr__(self):
        title = '' if self.__title is None else ' ' + self.__title
        return "<{0:s}{1:s} id={2:d}>".format(self.__class__.__name__, title,
                                              self.__id)

    def __format__(self, format_spec):
        return str(self).__format__(format_spec)
