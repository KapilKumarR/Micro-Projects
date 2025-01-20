__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

from pymal.searches import search_accounts_provider, search_animes_provider, search_mangas_provider

__all__ = ['search_animes', 'search_mangas', 'search_accounts']

__SearchAccounts = search_accounts_provider.SearchAccountsProvider()
__SearchAnimes = search_animes_provider.SearchAnimesProvider()
__SearchMangas = search_mangas_provider.SearchMangasProvider()


def search_accounts(search_string: str) -> frozenset:
    """
    :param search_string: a name of an account
    :type search_string: str
    :return: the found accounts that match the searched one
    :rtype: map.
    """
    return __SearchAccounts.search(search_string)


def search_animes(search_string: str) -> frozenset:
    """
    :param search_string: a name of an anime
    :type search_string: str
    :return: the found animes that match the searched one
    :rtype: map.
    """
    return __SearchAnimes.search(search_string)


def search_mangas(search_string: str) -> frozenset:
    """
    :param search_string: a name of a manga
    :type search_string: str
    :return: the found mangas that match the searched one
    :rtype: map.
    """
    return __SearchMangas.search(search_string)
