import collections
from functools import reduce


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
    __fields__ = ()


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
        if item in self.__fields__:
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

    @classmethod
    def get_name(cls):
        return cls.__name__

    @classmethod
    def get_readable_name(cls):
        return reduce(lambda x, y: x + (' ' if y.isupper() else '') + y, cls.get_name())

    @classmethod
    def get_func_name(cls):
        return reduce(lambda x, y: x + ('_' if y.isupper() else '') + y, cls.get_name()).lower()


def read_name(f, offset=None):
    if offset:
        f.seek(offset)
    return ''.join(list(iter(lambda: f.read(1).decode(), '\x00')))


def write_name(f, name, offset=None):
    if offset:
        f.seek(offset)
    f.write(name.encode())
    f.write(b'\x00')
