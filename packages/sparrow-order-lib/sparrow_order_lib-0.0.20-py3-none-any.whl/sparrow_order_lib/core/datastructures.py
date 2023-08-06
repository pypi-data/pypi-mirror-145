

class ImmutableList(tuple):
    """
    不可变列表
    """

    def __new__(cls, *args, warning='ImmutableList object is immutable.', **kwargs):
        self = tuple.__new__(cls, *args, **kwargs)
        self.warning = warning
        return self

    def complain(self, *wargs, **kwargs):
        if isinstance(self.warning, Exception):
            raise self.warning
        else:
            raise AttributeError(self.warning)

    # All list mutation functions complain.
    __delitem__ = complain
    __delslice__ = complain
    __iadd__ = complain
    __imul__ = complain
    __setitem__ = complain
    __setslice__ = complain
    append = complain
    extend = complain
    insert = complain
    pop = complain
    remove = complain
    sort = complain
    reverse = complain


class ImmutableDict(dict):

    def NotImplemented(self, *args, **kw):
        raise ValueError("Read Only dict proxy")

    popitem = update = clear = pop = __setitem__ = __delitem__ = NotImplementedError
