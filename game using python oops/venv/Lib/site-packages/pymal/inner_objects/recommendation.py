__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

from pymal import exceptions


class Recommendation(object):
    """
    Recommendation holds all the data from a recommendation in MAL about an anime.

    :ivar recommended_anime: :class:`anime.Anime`
    :ivar recommends: :class:`dict`
    """
    def __init__(self, div):
        """
        :param div: The dic of the recommendation to parse all the data from it.
        :type div: bs4.element.Tag
        """
        from pymal import account, anime

        recommended, recommends_divs = div.table.tbody.tr.findAll(name="td", recursive=False)

        self.recommended_anime = anime.Anime(int(recommended.div.a["href"].split('/')[2]))

        data = recommends_divs.findAll(name="div", recursive=False)
        if 3 == len(data):
            recommends = [data[2]]
        elif 5 == len(data):
            _, _, first_recommend, _, other_recommends = data
            recommends = [first_recommend] + other_recommends.findAll(name="div", recursive=False)
        else:
            raise exceptions.FailedToReloadError( "Unknown size of data: " + str(len(data)))

        self.recommends = dict()

        for recommend in recommends:
            recommend_data, user_data = recommend.findAll(name="div", recursive=False)
            username = user_data.find(name='a', recursive=False)["href"].split('/')[2]
            self.recommends[account.Account(username)] = recommend_data.text

    def __repr__(self):
        return "<{0:s} for {1:s} by {2:d} users>".format(
            self.__class__.__name__,
            self.recommended_anime,
            len(self.recommends)
        )
