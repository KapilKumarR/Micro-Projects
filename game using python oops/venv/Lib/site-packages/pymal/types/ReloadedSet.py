__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

import collections

import singleton_factory


class ReloadedSet(collections.Set):
    """
    A reloaded set - like frozenset but can fetch new data in the function reload.
    To inheritance you need to make:
     - _values
     - reload
    """
    @property
    def _values(self):
        raise NotImplemented()

    def reload(self):
        raise NotImplemented()

    def __contains__(self, item):
        return item in list(self._values)

    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)

    def issubset(self, other) -> frozenset:
        return self <= frozenset(other)

    def issuperset(self, other) -> frozenset:
        return self >= frozenset(other)

    def union(self, *others) -> frozenset:
        res = set(self)
        for other in others:
            res |= frozenset(other)
        return frozenset(res)

    def __or__(self, other) -> frozenset:
        return self.union(other)

    def intersection(self, *others) -> frozenset:
        other_lists = map(list, list(others) + [list(self)])
        def in_all(x):
            return all(map(lambda other_list: x in other_list, other_lists))

        import itertools
        other_union_lists = itertools.chain(other_lists)
        items_in_all = filter(in_all, other_union_lists)

        res = list()

        for item in items_in_all:
            if item not in res:
                res.append(item)

        return frozenset(res)

    def __and__(self, other) -> frozenset:
        return self.intersection(other)

    def difference(self, *others) -> frozenset:
        import itertools
        other_lists = map(list, others)
        other_union_lists = itertools.chain(other_lists)
        return frozenset(filter(lambda x: x not in other_union_lists, self))

    def __sub__(self, other) -> frozenset:
        return self.difference(other)

    def symmetric_difference(self, other) -> frozenset:
        self_list = list(self)
        other_not_in_self = frozenset(filter(lambda x: x not in self_list, other))

        other = list(other)
        self_not_in_other = frozenset(filter(lambda x: x not in other, self))

        return other_not_in_self | self_not_in_other

    def __xor__(self, other) -> frozenset:
        return self.symmetric_difference(other)


class ReloadedSetSingletonFactoryType(type(ReloadedSet), singleton_factory.SingletonFactory):
    """
    A singleton factory ReloadedSet type.
    """
    pass


class ReloadedSetSingletonFactory(ReloadedSet, metaclass=ReloadedSetSingletonFactoryType):
    """
    A singleton factory ReloadedSet.
    """
    pass