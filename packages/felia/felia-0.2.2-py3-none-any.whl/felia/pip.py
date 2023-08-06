from ._internal import SubCommand, RootCommand, parameter

__all__ = ["pip",
           "pip_list",
           "pip_install"]


class Pip(RootCommand):
    globals = globals()
    __main__ = "pip._internal.cli.main.main"

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
        from twine.commands import upload
        return upload.main(["--repository", repository, "dist/*"])

    @staticmethod
    def upgrade():
        """升级pip"""
        pip_install.upgrade()("pip")


@Pip.subcommand
class Config(SubCommand):
    ...


@Pip.subcommand
class Show(SubCommand):
    ...


@Pip.subcommand
class List(SubCommand):
    ...


@Pip.subcommand
class Install(SubCommand):
    @parameter(short="-i", long="--index-url")
    def index_url(self):
        """下载源"""

    @parameter(short="-U")
    def upgrade(self):
        """更新版本"""


pip = Pip()
pip_list = globals().get("pip_list")
pip_install = globals().get("pip_install")