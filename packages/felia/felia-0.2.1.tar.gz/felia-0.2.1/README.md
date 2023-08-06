# Felia

## 关于

felia是一个方便执行终端命令的工具，配合Pycharm Python console一起使用(其他Jetbrains系列IDE开发工具也可以, 下载python插件)，利用其强大的智能补全特性，提高命令输入效率。

该库被设计成在Windows系统使用, 本地在wsl环境下执行命令, 同时也可以远程至其他主机执行命令。

## 安装

```text
pip install felia
```

## 快速上手

打开Pycharm的Python控制台。

一般情况下Python控制台会默认打开, 也可在菜单栏中调用: <kbd>工具</kbd> -> <kbd>Python或调试控制台</kbd>

执行代码

```ipython
>>> from felia.pip import *
>>> pip_list()
INFO $ pip list
Package                Version             
---------------------- --------------------
.......                ........ 
```

## 已实现的命令行工具

* cobra
* docker
* go
* pip
* protoc
* sphinx
* ssh