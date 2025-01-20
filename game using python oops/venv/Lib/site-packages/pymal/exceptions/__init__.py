__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"


__all__ = ['UnauthenticatedAccountError', 'NotASeasonError', 'GotRobotError', ]


class UnauthenticatedAccountError(ValueError):
    pass


class NotASeasonError(ValueError):
    def __init__(self, tried_season_name):
        super().__init__("The wanted season '{0:s}' is not: 'Winter', 'Spring', 'Summer' or 'Fall'.".format(
            tried_season_name
        ))


class GotRobotError(RuntimeError):
    pass


from pymal.exceptions.failed_to_parse_error import *
from pymal.exceptions.my_anime_list_api_error import *
