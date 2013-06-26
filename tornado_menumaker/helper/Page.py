#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""

"""
import inspect
from tornado.web import Application

from .Route import Route
from .Index import IndexRoute

__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '16.06.13 - 23:46'


class Page(Route):
    """
        A Page
    """

    def __init__(self, url: str=None, **kwargs):
        super().__init__(url=url, **kwargs)

        self._index = None

    def __call__(self, *args, **kwargs):
        if isinstance(args[0], Application):
            if self._index is not None:
                return self._index(*args, **kwargs)

            self.handler = self.cls(*args, **kwargs)
            return self.handler
        elif isinstance(args[0], type):
            self.cls = args[0]

            for n, route in inspect.getmembers(self.cls, Route.isroute):
                route.url = self._url + route.url
                route.cls = self.cls

            for n, method in inspect.getmembers(self.cls, IndexRoute.isindex):
                self._index = method

            return self
        raise Exception()
