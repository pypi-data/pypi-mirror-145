from .base import SubCommand, RootCommand
from .configuration import config


def parameter(short=None, default=None, long=None, use_shell=False):
    """TODO short暂时没用途, 可能在未来的doc引用?
    """
    def _parameter(func):
        def inner(self, value=None):
            value = value or default
            option = (long or "--" + func.__name__)
            if value:
                option += " " + value
            if option not in self.args:
                self.args.append(option)
            if use_shell:
                if isinstance(self, SubCommand):
                    setattr(self.root, "use_shell2", use_shell)
                else:
                    setattr(self, "use_shell2", use_shell)
            return self
        return inner
    return _parameter
