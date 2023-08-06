from ._internal import RootCommand, parameter


class Python(RootCommand):
    __name__ = "python3"
    globals = globals()

    @parameter(long="-m")
    def m(self):
        """以脚本的方式运行指定模块

        -m mod : run library module as a script (terminates option list)
        """


python = Python()