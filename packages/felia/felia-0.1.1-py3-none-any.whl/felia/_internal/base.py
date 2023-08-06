import sys
import logging
import subprocess
from importlib import import_module
import win32api

from .configuration import ConfMixin

logger = logging.getLogger(__name__)
h = logging.StreamHandler()
h.setFormatter(logging.Formatter("%(levelname)s $ %(message)s"))
logger.addHandler(h)
logger.setLevel(logging.INFO)


class BaseCommand:
    """
    cli.para1().para2()(run=False) # 只输出命令，不执行
    等价于
    cli --para1 --para2
    """

    use_shell = False

    def __init__(self):
        self._params = []
        self.pre = []
        self.args = []
        self.cmd = [self.__name__]
        self.run = subprocess.run
        self.setup()

    def setup(self):
        if sys.platform == "win32":
            self.pre.append('powershell.exe')
            self.pre.append('wsl')

    def __call__(self, *args, **kwargs):
        pass

    def show_commands(self):
        self(run=False)

    def print_help(self):
        print(f"Usage:  {self.cmd[0]}")
        print()
        for obj in self._params:
            obj.print_help()

    def clear_args(self):
        self.args.clear()

    def execute(self, *args, use_shell=False):
        _args = self.args + list(args)
        self(*_args, use_shell=use_shell)

    from felia._internal import parameter

    @parameter()
    def help(self):
        """帮助信息"""


class RootCommand(BaseCommand, ConfMixin):
    subcommands: list
    globals: dict

    def setup(self):
        super(RootCommand, self).setup()
        if not hasattr(self, 'subcommands'):
            return

        while self.subcommands:
            CMD = self.subcommands.pop()
            obj = CMD(self)
            setattr(self, CMD.__name__, obj)
            obj_name = f"{self.__name__}_{CMD.__name__}".lower()
            self.globals.setdefault(obj_name,
                                    obj)

            if _all := self.globals.get("__all__"):
                if obj_name not in _all:
                    _all.append(obj_name)

    def __call__(self, *args, run=True, use_shell=False):
        cmd = self.cmd + list(args)
        logger.info(" ".join(cmd))
        if run:
            if hasattr(self, '__main__'):
                module_name, func_name = getattr(self, '__main__').rsplit(".", 1)
                return getattr(import_module(module_name), func_name)(args)
            elif hasattr(self, "use_shell2") and getattr(self, "use_shell2") or use_shell or self.use_shell:
                # use_shell2是临时性的, 在装饰器parameter传入
                delattr(self, "use_shell2") if hasattr(self, "use_shell2") else None
                # Pycharm python console遇到input会卡住不能交互, 用win32api调用powershell窗口处理
                return win32api.ShellExecute(0, "open", "powershell.exe", "wsl " + " ".join(cmd), "", 1)
            else:
                content = " ".join(self.pre + cmd)
                if self.pre:
                    content = content.replace(" | ", " | wsl ")
                return self.run(content)

    @classmethod
    def subcommand(cls, sub_class):
        if not hasattr(cls, 'subcommands'):
            setattr(cls, 'subcommands', [])
        cls.subcommands.append(sub_class)
        del sub_class


class SubCommand(BaseCommand):

    def __init__(self, root):
        super(SubCommand, self).__init__()
        self.root = root

    def __call__(self, *args, run=True, use_shell=False):
        _args = self.args + list(args)
        cmd = self.cmd + _args

        self.root(*cmd, run=run, use_shell=use_shell)
        if run:
            self.clear_args()
            self.root.clear_args()








