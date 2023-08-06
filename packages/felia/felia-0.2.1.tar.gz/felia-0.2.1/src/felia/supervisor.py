from ._internal import RootCommand

__all__ = ["echo_supervisord_conf"]


class EchoSupervisordConf(RootCommand):
    __name__ = "echo_supervisord_conf"
    globals = globals()


echo_supervisord_conf = EchoSupervisordConf()
