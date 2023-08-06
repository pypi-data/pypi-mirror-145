import logging

from ._internal import SubCommand, RootCommand, parameter


class Go(RootCommand):
    __name__ = 'go'
    globals = globals()


@Go.subcommand
class Mod(SubCommand):
    """项目和包管理"""
    subcmd = "mod"

    @parameter
    def init(self):
        """在当前目录初始化"""


go = Go()
