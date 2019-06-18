import collections


def merge_dict(d1, d2):
    """
    Modifies d1 in-place to contain values from d2.  If any value
    in d1 is a dictionary (or dict-like), *and* the corresponding
    value in d2 is also a dictionary, then merge them in-place.
    """
    for k, v2 in d2.items():
        v1 = d1.get(k)  # returns None if v1 has no value for this key
        if (isinstance(v1, collections.Mapping) and
                isinstance(v2, collections.Mapping)):
            merge_dict(v1, v2)
        else:
            d1[k] = v2
            if isinstance(v1, set):
                d1[k].update(v1)


class EmptyRecord:
    __attrs__ = ()


class BaseRecord(object):
    data = EmptyRecord()
    dependencies = {}

    def __getattr__(self, item):
        try:
            return self.data.__getattribute__(item)
        except AttributeError:
            return super().__getattribute__(item)

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __setattr__(self, item, value):
        if item in self.__attrs__:
            self.data.__setattr__(item, value)
        else:
            super().__setattr__(item, value)

    def __setitem__(self, item, value):
        self.__setattr__(item, value)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        return self.__dict__.update(d)

    def __repr__(self):
        return self.data.__repr__()

    def __str__(self):
        return self.data.__str__()

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ != other.__dict__

    def __hash__(self):
        return hash(self.__dict__.values())

    def get_name(self):
        return type(self).__name__

    def get_readable_name(self):
        return self.get_name()
