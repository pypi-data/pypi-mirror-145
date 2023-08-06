from .base import SubCommand, RootCommand
from .configuration import config


def parameter(short=None, default=None, long=None):
    """TODO short暂时没用途, 可能在未来的doc引用?"""
    def _parameter(func):
        def inner(self, value):
            value = value or default
            option = (long or "--" + func.__name__) + " " + value
            if option not in self.args:
                self.args.append(option)
            return self
        return inner
    return _parameter
