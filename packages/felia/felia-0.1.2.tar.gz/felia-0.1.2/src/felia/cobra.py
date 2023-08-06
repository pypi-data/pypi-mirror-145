import logging
from pathlib import Path

from felia._internal import RootCommand, SubCommand, change_workdir, config

logger = logging.getLogger('Docker')
h = logging.StreamHandler()
h.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - | %(message)s"))
logger.addHandler(h)
logger.setLevel(logging.INFO)


class Add(SubCommand):
    """增加一个Cobra命令

    cobra-cli add serve
    cobra-cli add config
    cobra-cli add create -p 'configCmd'
    """
    subcmd = "add"


class CobraCli(RootCommand):
    """生成cobra代码

    https://github.com/spf13/cobra-cli/blob/main/README.md"""
    __name__ = 'cobra-cli'
    globals = globals()
    subcommands = [Add, ]


cobra_cli = CobraCli()
cobra_add = getattr(cobra_cli, 'add')

change_workdir(config["COBRA"])