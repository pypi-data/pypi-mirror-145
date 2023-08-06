import os

import argparse
import configparser
from pip._vendor.platformdirs.windows import Windows

win = Windows()

DIR_NAME = "felia"


def main():
    """python3 -m felia set --cli sphinx --project django --path /root"""
    parser = argparse.ArgumentParser(prog='HELPER',
                                     description="生活和工作的助手程序")
    parser.add_argument('action', metavar='ACTION', type=str, nargs='?',
                        help='设置项目路径')
    parser.add_argument("--cli", dest="cli", action='store',
                        help="命令行接口")
    parser.add_argument('--project', dest='project', action='store',
                        help='项目')
    parser.add_argument('--path', dest='path', action='store',
                        help='项目路径')
    args = parser.parse_args()

    handle = {"set": set_value,
              "get": get_value}
    handle[args.action](args)


def set_value(args):
    config = configparser.ConfigParser()
    felia_path = win.user_config_path / DIR_NAME
    if not os.path.exists(felia_path):
        os.makedirs(felia_path)

    ini = win.user_config_path / DIR_NAME / 'felia.ini'
    config.read(ini)

    section = args.cli.upper()
    if section not in config.keys():
        config.add_section(section)
    config[args.cli.upper()].setdefault(args.project, args.path)

    with open(ini, 'w') as configfile:
        config.write(configfile)


def get_value(args):
    ...


if __name__ == '__main__':
    main()