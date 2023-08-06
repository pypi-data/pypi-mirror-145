from ._internal import SubCommand, RootCommand, parameter

__all__ = ["pip",
           "pip_install"]


class Pip(RootCommand):
    __name__ = "pip"
    globals = globals()

    @staticmethod
    def generating_distribution_archives():
        """打包软件

        https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives
        """
        from .python import python
        python.m("build").execute()

    @staticmethod
    def uploading_the_distribution_archives(repository="pypi"):
        """上传打包文件

        https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives
        测试环境: https://test.pypi.org/simple/ repository=testpypi
        生产环境: https://pypi.org/simple repository=pypi
        """
        from .python import python
        python.m("twine").execute(f"upload --repository {repository} dist/*", use_shell=True)


@Pip.subcommand
class Config(SubCommand):
    __name__ = "config"


@Pip.subcommand
class Show(SubCommand):
    __name__ = "show"


@Pip.subcommand
class List(SubCommand):
    __name__ = "list"


@Pip.subcommand
class Install(SubCommand):
    __name__ = "install"

    @parameter(short="-i", long="--index-url")
    def index_url(self):
        """下载源"""

    @parameter(short="-U")
    def upgrade(self):
        """更新版本"""


pip = Pip()
pip_install = globals().get("pip_install")