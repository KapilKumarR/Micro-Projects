__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

from pymal.searches import search_provider

__all__ = ['SearchMangasProvider']


class SearchMangasProvider(search_provider.SearchProvider):
    """
    Searching for mangas.
    """
    _SEARCH_NAME = 'manga'
    _SEARCHED_URL_SUFFIX = '/manga/'

    def _SEARCHED_OBJECT(self, mal_url: str):
        from pymal import manga

        mal_id = int(mal_url.split('/')[0])
        return manga.Manga(int(mal_id))
