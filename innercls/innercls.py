#!/usr/bin/env python
# encoding: utf-8

import functools


def innercls(cls=None, attr="outter"):
    if cls is None:
        return functools.partial(innercls, attr=attr)

    assert callable(cls)

    def init(outter, *args, **kwg):
        instance = cls(*args, **kwg)
        setattr(instance, attr, outter)
        return instance

    return init


def clsproxy(cls):
    class ClsProxy(object):
        def __getattribute__(self, name):
            return cls.__getattribute__(name)

        def __setattr__(self, name, val):
            raise Exception("read only proxy")

    return ClsProxy()


class Outter(object):
    @innercls(attr="parent")
    class Inner(object):
        def __init__(self, val):
            self.val = val


outter = Outter()
inner = outter.Inner(2)
proxy = clsproxy(inner)

print inner.parent is outter
print proxy is inner
print proxy.val is inner.val
print proxy.parent is outter

inner.parent = None
print inner.parent is outter
print proxy.parent is outter

proxy.parent = None
