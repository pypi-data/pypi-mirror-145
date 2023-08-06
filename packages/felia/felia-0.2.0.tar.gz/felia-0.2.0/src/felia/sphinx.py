from ._internal import RootCommand, parameter


class SphinxQuickstart(RootCommand):
    """初始化sphinx项目
    """
    __name__ = 'sphinx-quickstart'
    __main__ = 'sphinx.cmd.quickstart.main'
    globals = globals()


class SphinxBuild(RootCommand):
    """
    usage: sphinx-build [OPTIONS] SOURCEDIR OUTPUTDIR [FILENAMES...]
    """
    __name__ = 'sphinx-build'
    __main__ = 'sphinx.cmd.build.main'
    globals = globals()

    @parameter(long="-W")
    def W(self):
        """将警告信息转为错误，即遇到警告信息时退出程序"""

    def make_html(self):
        self("source",
             "build")


sphinx_quickstart = SphinxQuickstart()
sphinx_build = SphinxBuild()
