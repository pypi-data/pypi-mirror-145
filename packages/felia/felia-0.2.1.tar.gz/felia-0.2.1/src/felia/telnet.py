from ._internal import RootCommand


class Telnet(RootCommand):
    """远程连接主机，跟ssh的区别是telnet采用明文传输"""
    __name__ = 'telnet'

