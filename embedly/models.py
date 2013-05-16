"""
Models

Creates a sudo model class that makes it easy to access attributes
"""
from __future__ import unicode_literals
class AttrDict(object):
    """
    UserDict is a pain in the ass. Let's just make our own.
    """
    def __init__(self, data=None):
        if data is None:
            data = {}

        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = AttrDict(value)
            elif isinstance(value, list):
                values = []
                for v in value:
                    if isinstance(v, dict):
                        values.append(AttrDict(v))
                    else:
                        values.append(v)
                data[key] = values

        self.data = data

    def __getattr__(self, name):
        if name in ['data', 'method', 'original_url']:
            return object.__getattr__(self, name)
        try:
            return self.data[name]
        except KeyError:
            return None

    def __setattr__(self, name, value):
        if name in ['data', 'method', 'original_url']:
            object.__setattr__(self, name, value)
        else:
            self.data[name] = value

    def __getitem__(self, name): return self.data[name]
    def __setitem__(self, name, value): self.data[name] = value
    def __delitem__(self, name): del self.data[name]
    def __len__(self): return len(self.data)
    def get(self, name): return self.data.get(name)
    def keys(self): return self.data.keys()
    def values(self): return self.data.values()
    def items(self): return self.data.items()

    @property
    def dict(self):
        return self.data


class Url(AttrDict):

    def __init__(self, data=None, method=None, original_url=None):
        if data is None:
            data = {}
        super(Url, self).__init__(data)
        self.method = method or 'url'
        self.original_url = original_url

    def __str__(self):
        return self.__unicode__().encode("utf-8")

    def __unicode__(self):
        return '<%s %s>' % (self.method.title(), self.original_url or "")
