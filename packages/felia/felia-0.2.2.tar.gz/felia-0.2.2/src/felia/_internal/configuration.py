import configparser
import os
import logging
from pip._vendor.platformdirs.windows import Windows


logger = logging.getLogger(__name__)
win = Windows()
DIR_NAME = "felia"
config = configparser.ConfigParser()
ini = win.user_config_path / DIR_NAME / 'felia.ini'
config.read(ini, encoding='utf-8')


class ConfMixin:
    def change_workdir(self):
        key = self.__class__.__name__.upper()
        if config.has_section(key) is False:
            return

        section = config[key]
        projects = list(section.items())

        if len(projects) == 1:
            path = projects[0][1]
        else:
            for index, value in enumerate(projects):
                print(index + 1, value[0])

            i = int(input("请选择一个项目")) - 1
            path = projects[i][1]

        print("切换路径:", path)
        os.chdir(path)

    def change_conn(self):
        """切换本地或者连接远程机器

        :return:
        """
        key = self.__class__.__name__.upper()
        if config.has_section(key) is False:
            return

        section = config[key]
        projects = list(section.items())
        if len(projects) == 0:
            return

        print(1, "Local")
        for index, value in enumerate(projects, start=2):
            print(index, value[0])
        i = int(input("请选择一个项目"))

        if i == 1:
            import subprocess
            self.run = subprocess.run
            return

        from fabric import Connection
        import json
        logger.debug(f"projects: {projects}")
        conf = json.loads(projects[i - 2][1])
        conn = Connection(conf["host"],
                          user=conf["user"],
                          port=conf["port"],
                          connect_kwargs={"key_filename": conf["key_filename"]})
        self.run = conn.sudo