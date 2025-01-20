__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

from urllib import request
import time

import singleton_factory

from pymal import consts
from pymal import decorators
from pymal import exceptions

__all__ = ['MyAnime']


class MyAnime(object, metaclass=singleton_factory.SingletonFactory):
    """
    Saves an account data about anime.

    :ivar my_enable_discussion: boolean
    :ivar my_id: int
    :ivar my_status: int.  #TODO: put the dictionary here.
    :ivar my_score: int.
    :ivar my_start_date: string as mmddyyyy.
    :ivar my_end_date: string as mmddyyyy.
    :ivar my_priority: int.
    :ivar my_storage_type: int.  #TODO: put the dictanary here.
    :ivar my_storage_value: float.
    :ivar my_is_rewatching: boolean.
    :ivar my_completed_episodes: int.
    :ivar my_download_episodes: int.
    :ivar my_times_rewatched: int.
    :ivar my_rewatch_value: int.
    :ivar my_tags: frozenset.
    :ivar my_comments: string
    :ivar my_fan_sub_groups: string.
    """

    __TAG_SEPARATOR = ';'
    __MY_MAL_URL = request.urljoin(
        consts.HOST_NAME, 'editlist.php?type=anime&id={0:d}')
    __MY_MAL_DELETE_URL = request.urljoin(
        consts.HOST_NAME, 'api/animelist/delete/{0:d}.xml')
    __MY_MAL_UPDATE_URL = request.urljoin(
        consts.HOST_NAME, 'api/animelist/update/{0:d}.xml')

    def __init__(self, mal_id: int, my_mal_id, account):
        """
        """
        from pymal import anime
        if isinstance(mal_id, anime.Anime):
            self.obj = mal_id
        else:
            self.obj = anime.Anime(mal_id)

        self.__my_mal_url = self.__MY_MAL_URL.format(self.obj.id)

        self._is_my_loaded = False
        self._account = account

        self.__my_mal_id = my_mal_id
        self.__my_status = 0
        self.my_enable_discussion = False
        self.__my_score = 0.0
        self.__my_start_date = ''
        self.__my_end_date = ''
        self.__my_priority = 0
        self.__my_storage_type = 0
        self.__my_storage_value = 0.0
        self.__my_comments = ''
        self.__my_fan_sub_groups = ''
        self.__my_tags = frozenset()

        self.__my_is_rewatching = None
        self.__my_completed_episodes = None
        self.__my_download_episodes = 0
        self.__my_times_rewatched = 0
        self.__my_rewatch_value = None

    @property
    def my_id(self) -> int:
        """
        :return: the id in the account.
        :rtype: int
        """
        return self.__my_mal_id

    @property
    @decorators.my_load
    def my_status(self) -> int:
        """
        :return: the status as number between 1 to 6.
        :rtype: int
        """
        return self.__my_status

    @my_status.setter
    def my_status(self, status: int):
        """
        :param status: the value to put in status. must be between 1 to 6.
        :type: int
        """
        if not (1 <= status <= 6):
            raise RuntimeError("value of my_statue can be 1 to 6")
        self.__my_status = status

    @property
    @decorators.my_load
    def my_score(self) -> int:
        """
        :return: The score as int between 0 to 10.
        :rtype: int
        """
        return self.__my_score

    @my_score.setter
    def my_score(self, score: int):
        """
        :param score: The score. Must be between 0 to 10.
        :type: int
        """
        if not (0 <= score <= 10):
            raise RuntimeError("score must be between 0 to 10")
        self.__my_score = score

    @property
    @decorators.my_load
    def my_start_date(self) -> str:
        """
        :return: the start date of watching.
        """
        return self.__my_start_date

    @my_start_date.setter
    def my_start_date(self, start_date_string: str):
        """
        :param start_date_string: An string that look like {@link consts.MALAPI_FORMAT_TIME}".
        :type: str
        """
        time.strptime(start_date_string, consts.MALAPI_FORMAT_TIME)
        self.__my_start_date = start_date_string

    @property
    @decorators.my_load
    def my_end_date(self) -> str:
        """
        :return: the end date of watching.
        :type: str
        """
        return self.__my_end_date

    @my_end_date.setter
    def my_end_date(self, end_date_string: str):
        """
        :param end_date_string: An string that look like {@link consts.MALAPI_FORMAT_TIME}".
        :type: str
        """
        time.strptime(end_date_string, consts.MALAPI_FORMAT_TIME)
        self.__my_end_date = end_date_string

    @property
    @decorators.my_load
    def my_priority(self) -> int:
        """
        :return: The priority value as int between 0 to 3
        :rtype: int
        """
        return self.__my_priority

    @my_priority.setter
    def my_priority(self, priority: int):
        """
        :param priority: priority must be between 0 to 3.
        :type: int
        """
        if not (0 <= priority <= 3):
            raise RuntimeError("priority can be 0 to 3")
        self.__my_priority = priority

    @property
    @decorators.my_load
    def my_storage_type(self) -> int:
        """
        :return: The storage type of the downloaded episodes. Between 0 to 7.
        :rtype: int
        """
        return self.__my_storage_type

    @my_storage_type.setter
    def my_storage_type(self, storage_type: int):
        """
        :param storage_type: int between 0 to 7.
        :type: int
        """
        if not (0 <= storage_type <= 7):
            raise RuntimeError("value of my_storage_type can be 0 to 7")
        self.__my_storage_type = storage_type

    @property
    @decorators.my_load
    def my_storage_value(self) -> float:
        """
        :return: the storage value (the size you saved) - float but a real number!
        :rtype: float
        """
        return self.__my_storage_value

    @my_storage_value.setter
    def my_storage_value(self, storage_value: float):
        """
        :param storage_value: the storage value (the size you saved) - float but a real number!
        :type: float
        """
        int(storage_value)
        self.__my_storage_value = storage_value

    @property
    @decorators.my_load
    def my_is_rewatching(self) -> bool:
        """
        :return: a flag to know if rewatching now.
        :rtype: bool
        """
        return self.__my_is_rewatching

    @my_is_rewatching.setter
    def my_is_rewatching(self, is_rewatching: bool):
        """
        :param is_rewatching: a flag to know if rewatching now.
        :type: bool
        """
        self.__my_is_rewatching = is_rewatching

    @property
    @decorators.my_load
    def my_completed_episodes(self) -> int:
        """
        :return: the number of completed episodes.
        :rtype: int
        """
        return self.__my_completed_episodes

    @my_completed_episodes.setter
    def my_completed_episodes(self, completed_episodes: int):
        """
        :param completed_episodes: the number of completed episodes. Between 0 to number of episodes.
        :type: int
        """
        if not (0 <= completed_episodes <= self.episodes):
            raise RuntimeError("value of my_completed_episodes can be 0 to self.episodes")
        self.__my_completed_episodes = completed_episodes

    @property
    @decorators.my_load
    def my_download_episodes(self) -> int:
        """
        :return: the number of downloaded episodes.
        :rtype: int
        """
        return self.__my_download_episodes

    @my_download_episodes.setter
    def my_download_episodes(self, downloaded_episodes: int):
        """
        :param downloaded_episodes: the number of downloaded episodes. Between 0 to number of episodes.
        :type: int
        """
        if not (0 <= downloaded_episodes <= self.episodes):
            raise RuntimeError("downloaded episodes can be 0 to self.episodes")
        self.__my_download_episodes = downloaded_episodes

    @property
    @decorators.my_load
    def my_times_rewatched(self) -> int:
        """
        :return: The times of rewatching is a positive value.
        :type: int
        """
        return self.__my_times_rewatched

    @my_times_rewatched.setter
    def my_times_rewatched(self, times_rewatched: int):
        """
        :param times_rewatched: the times of rewatching must be a positive value.
        :type: int
        """
        if not (0 <= times_rewatched):
            raise RuntimeError("value of my_times_rewatched can be 0 or more")
        self.__my_times_rewatched = times_rewatched

    @property
    @decorators.my_load
    def my_rewatch_value(self) -> int:
        """
        :return: The rewatching is between 0 to 5.
        :type: int
        """
        return self.__my_rewatch_value

    @my_rewatch_value.setter
    def my_rewatch_value(self, rewatch_value: int):
        """
        :param rewatch_value: The rewatching must be between 0 to 5.
        :type: int
        """
        if not (0 <= rewatch_value <= 5):
            raise RuntimeError("rewatch value can be 0 to 5")
        self.__my_rewatch_value = rewatch_value

    @property
    @decorators.my_load
    def my_tags(self):
        """
        :return: the account tags.
        :rtype: frozenset
        """
        return self.__my_tags

    @property
    @decorators.my_load
    def my_comments(self):
        """
        :return: the comment of the account about the anime.
        :rtype: str
        """
        return self.__my_comments

    @property
    @decorators.my_load
    def my_fan_sub_groups(self):
        """
        :return: the fan sub groups
        :rtype: str
        """
        return self.__my_fan_sub_groups

    def my_reload(self):
        """
        Reloading data from MAL.
        """
        from pymal import global_functions

        # Getting content wrapper <div>
        content_wrapper_div = global_functions.get_content_wrapper_div(
            self.__my_mal_url, self._account.auth_connect)

        bas_result = content_wrapper_div.find(name='div',
                                              attrs={'class': 'badresult'})
        if bas_result is not None:
            raise exceptions.FailedToReloadError(bas_result)

        # Getting content <td>
        content_div = content_wrapper_div.find(
            name="div", attrs={"id": "content"}, recursive=False)
        if content_div is None:
            raise exceptions.FailedToReloadError(content_wrapper_div)
        content_td = content_div.table.tr.td
        if content_td is None:
            raise exceptions.FailedToReloadError(content_div)

        # Getting content rows <tr>
        content_form = content_td.find(name="form", attrs={'id': "myAnimeForm"})
        if content_form is None:
            raise exceptions.FailedToReloadError(content_td)
        content_rows = content_form.table.tbody.findAll(
            name="tr", recursive=False)

        contents_divs_index = 2

        # Getting my_status
        status_select = content_rows[contents_divs_index].find(
            name="select", attrs={"id": "status", "name": "status"})
        if status_select is None:
            raise exceptions.FailedToReloadError(content_rows)

        # TODO: make this look better
        status_selected_options = list(filter(
            lambda x: 'selected' in x.attrs,
            status_select.findAll(name="option")
        ))
        if 1 != len(status_selected_options):
            raise exceptions.FailedToReloadError(status_selected_options)
        self.__my_status = int(status_selected_options[0]['value'])

        is_rewatch_node = content_rows[contents_divs_index].find(
            name="input", attrs={"id": "rewatchingBox"})
        if is_rewatch_node is None:
            raise exceptions.FailedToReloadError(content_rows)
        self.__my_is_rewatching = bool(is_rewatch_node['value'])
        contents_divs_index += 1

        # Getting watched episodes
        watched_input = content_rows[contents_divs_index].\
            find(name="input", attrs={"id": "completedEpsID",
                                      "name": "completed_eps"})
        if watched_input is None:
            raise exceptions.FailedToReloadError(content_rows)
        self.__my_completed_episodes = int(watched_input['value'])
        contents_divs_index += 1

        # Getting my_score
        score_select = content_rows[contents_divs_index].find(
            name="select", attrs={"name": "score"})
        if score_select is None:
            raise exceptions.FailedToReloadError(content_rows)
        score_selected_option = score_select.find(
            name="option", attrs={"selected": ""})
        if score_selected_option is None:
            raise exceptions.FailedToReloadError(score_select)
        self.__my_score = int(float(score_selected_option['value']))
        contents_divs_index += 1

        # Getting my_tags...
        tag_content = content_rows[contents_divs_index]
        tag_textarea = tag_content.find(
            name="textarea", attrs={"name": "tags"})
        self.__my_tags = frozenset(tag_textarea.text.split(self.__TAG_SEPARATOR))
        contents_divs_index += 1

        # Getting start date
        start_month_date_node = content_rows[contents_divs_index].find(
            name="select", attrs={"name": "startMonth"})
        if start_month_date_node is None:
            raise exceptions.FailedToReloadError(content_rows)
        start_month_date = start_month_date_node.find(
            name="option", attrs={"selected": ""})

        start_day_date_node = content_rows[contents_divs_index].find(
            name="select", attrs={"name": "startDay"})
        if start_day_date_node is None:
            raise exceptions.FailedToReloadError(content_rows)
        start_day_date = start_day_date_node.find(
            name="option", attrs={"selected": ""})

        start_year_date_node = content_rows[contents_divs_index].find(
            name="select", attrs={"name": "startYear"})
        if start_year_date_node is None:
            raise exceptions.FailedToReloadError(content_rows)
        start_year_date = start_year_date_node.find(
            name="option", attrs={"selected": ""})

        start_month_date = str(start_month_date['value']).zfill(2)
        start_day_date = str(start_day_date['value']).zfill(2)
        start_year_date = str(start_year_date['value']).zfill(2)
        self.__my_start_date = start_month_date + \
            start_day_date + start_year_date
        contents_divs_index += 1

        # Getting end date
        end_month_date_node = content_rows[contents_divs_index].find(
            name="select", attrs={"name": "endMonth"})
        if end_month_date_node is None:
            raise exceptions.FailedToReloadError(content_rows)
        end_month_date = end_month_date_node.find(
            name="option", attrs={"selected": ""})

        end_day_date_node = content_rows[contents_divs_index].find(
            name="select", attrs={"name": "endDay"})
        if end_day_date_node is None:
            raise exceptions.FailedToReloadError(content_rows)
        end_day_date = end_day_date_node.find(
            name="option", attrs={"selected": ""})

        end_year_date_node = content_rows[contents_divs_index].find(
            name="select", attrs={"name": "endYear"})
        if end_year_date_node is None:
            raise exceptions.FailedToReloadError(content_rows)
        end_year_date = end_year_date_node.find(
            name="option", attrs={"selected": ""})

        end_month_date = str(end_month_date['value']).zfill(2)
        end_day_date = str(end_day_date['value']).zfill(2)
        end_year_date = str(end_year_date['value']).zfill(2)
        self.__my_end_date = end_month_date + end_day_date + end_year_date
        contents_divs_index += 1

        # Getting fansub group
        fansub_group_content = content_rows[contents_divs_index]
        fansub_group_input = fansub_group_content.find(
            name="input", attrs={"name": "fansub_group"})
        self.__my_fan_sub_groups = fansub_group_input.text
        contents_divs_index += 1

        # Getting priority
        priority_node = content_rows[contents_divs_index].find(
            name="select", attrs={"name": "priority"})
        if priority_node is None:
            raise exceptions.FailedToReloadError(content_rows)
        selected_priority_node = priority_node.find(
            name="option", attrs={"selected": ""})
        if selected_priority_node is None:
            raise exceptions.FailedToReloadError(content_rows)
        self.__my_priority = int(selected_priority_node['value'])
        contents_divs_index += 1

        # Getting storage
        storage_type_node = content_rows[contents_divs_index].find(
            name="select", attrs={"id": "storage"})
        if storage_type_node is None:
            raise exceptions.FailedToReloadError(content_rows)
        selected_storage_type_node = storage_type_node.find(
            name="option", attrs={"selected": ""})
        if selected_storage_type_node is None:
            raise exceptions.FailedToReloadError(content_rows)

        self.__my_storage_type = int(selected_storage_type_node['value'])

        storage_value_node = content_rows[contents_divs_index].find(
            name="input", attrs={"id": "storageValue"})
        if storage_value_node is None:
            raise exceptions.FailedToReloadError(content_rows)
        self.__my_storage_value = float(storage_value_node['value'])
        contents_divs_index += 1

        # Getting downloaded episodes
        downloaded_episodes_node = content_rows[contents_divs_index].\
            find(name="input", attrs={'id': "epDownloaded",
                                      'name': 'list_downloaded_eps'})
        if downloaded_episodes_node is None:
            raise exceptions.FailedToReloadError(content_rows)
        self.__my_download_episodes == int(downloaded_episodes_node['value'])
        contents_divs_index += 1

        # Getting time rewatched
        times_rewatched_node = content_rows[contents_divs_index].find(
            name="input", attrs={'name': 'list_times_watched'})
        self.__my_times_rewatched == int(times_rewatched_node['value'])
        if times_rewatched_node is None:
            raise exceptions.FailedToReloadError(content_rows)
        contents_divs_index += 1

        # Getting rewatched value
        rewatch_value_node = content_rows[contents_divs_index].find(
            name="select", attrs={'name': 'list_rewatch_value'})
        if rewatch_value_node is None:
            raise exceptions.FailedToReloadError(content_rows)
        rewatch_value_option = rewatch_value_node.find(
            name='option', attrs={'selected': ''})
        if rewatch_value_option is None:
            raise exceptions.FailedToReloadError(content_rows)

        self.__my_rewatch_value = int(rewatch_value_option['value'])
        contents_divs_index += 1

        # Getting comments
        comment_content = content_rows[contents_divs_index]
        comment_textarea = comment_content.find(
            name="textarea", attrs={"name": "list_comments"})
        self.__my_comments = comment_textarea.text
        contents_divs_index += 1

        # Getting discuss flag
        discuss_node = content_rows[contents_divs_index].find(
            name='select', attrs={"name": "discuss"})
        if discuss_node is None:
            raise exceptions.FailedToReloadError(content_rows)
        self._is_my_loaded = True

    def to_xml(self):
        """
        :return: the anime as an xml string.
        :rtype: str
        """
        data = self.MY_MAL_XML_TEMPLATE.format(
            self.my_completed_episodes,
            self.my_status,
            self.my_score,
            self.my_download_episodes,
            self.my_storage_type,
            self.my_storage_value,
            self.my_times_rewatched,
            self.my_rewatch_value,
            self.my_start_date,
            self.my_end_date,
            self.my_priority,
            self.my_enable_discussion,
            self.my_is_rewatching,
            self.my_comments,
            self.my_fan_sub_groups,
            self.__TAG_SEPARATOR.join(self.my_tags)
        )
        return data

    def add(self, account):
        """
        Adding the anime to an account.
        If its the same account as this owner returning this.

        :param account: account to connect to the anime.
        :type account: :class:`account.Account`
        :return: anime connected to the account
        :rtype: :class:`account_objects.my_anime.MyAnime`
        """
        if account == self._account:
            return self
        return self.obj.add(account)

    def update(self):
        """
        Updating the anime data.
        """
        xml = ''.join(map(lambda x: x.strip(), self.to_xml().splitlines()))
        update_url = self.__MY_MAL_UPDATE_URL.format(self.id)
        ret = self._account.auth_connect(
            update_url,
            data='data=' + xml,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        if ret != 'Updated':
            raise exceptions.MyAnimeListApiUpdateError(ret)

    def delete(self):
        """
        Deleteing the anime from the list.
        """
        xml = ''.join(map(lambda x: x.strip(), self.to_xml().splitlines()))
        delete_url = self.__MY_MAL_DELETE_URL.format(self.id)
        ret = self._account.auth_connect(
            delete_url,
            data='data=' + xml,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        if ret != 'Deleted':
            raise exceptions.MyAnimeListApiDeleteError(ret)

    def increase(self) -> bool:
        """
        Increasing the watched episode.
        If it is completed, setting the flag of rewatching.

        :return: True if succeed to set every.
        :rtype: bool
        """
        if self.my_completed_episodes >= self.obj.episodes:
            return False
        if 0 == self.my_completed_episodes and 2 != self.my_status:
            self.my_is_rewatching = True
            self.my_times_rewatched += 1
            self.my_completed_episodes = 0
        self.my_completed_episodes += 1
        return True

    def increase_downloaded(self) -> bool:
        """
        Increasing the downloaded episode.

        :return: True if succeed to set every.
        :rtype: bool
        """
        if self.my_download_episodes >= self.obj.episodes:
            return False
        self.my_download_episodes += 1
        return True

    @property
    def is_completed(self) -> bool:
        """
        :return: True if the number of completed episode is equal to number of episode in anime.
        :rtype: bool
        """
        return self.my_completed_episodes == self.obj.episodes

    def set_completed(self) -> bool:
        """
        Setting the anime as completed.

        :return: True if succeed
        :rtype: bool
        """
        if self.obj.episodes == float('inf'):
            return False
        self.my_completed_episodes = self.obj.episodes
        self.my_is_rewatching = False
        self.my_status = 2
        return True

    def set_completed_download(self) -> bool:
        """
        Setting the number of downloaded episodes as completed.

        :return: True if succeed
        :rtype: bool
        """
        if self.obj.episodes == float('inf'):
            return False
        self.my_download_episodes = self.obj.episodes
        return True

    def __getattr__(self, name):
        return getattr(self.obj, name)

    def __dir__(self):
        return list(set(dir(type(self)) + list(self.__dict__.keys()) + dir(self.obj)))

    def __eq__(self, other):
        return self.obj == other

    def __hash__(self):
        return hash(self.obj)

    def __repr__(self):
        title = " '{0:s}'".format(self.title) if self.obj._is_loaded else ''
        return "<{0:s}{1:s} of account '{2:s}' id={3:d}>".format(
            self.__class__.__name__, title, self._account.username, self.id)
