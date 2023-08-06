#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/3/25 9:34
# @Author  : xgy
# @Site    : 
# @File    : cli.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import click
import os
import sys

from scripts.model_docker import model_list, model_download, model_start
from scripts.allTools import server_list, server_download

__version__ = "1.1.dev2"
pgk_dir = os.path.join(os.path.dirname(os.path.abspath('__file__')))


# 主组命令 CSPtools
@click.group(context_settings={'help_option_names': ['-h', '--help']}, invoke_without_command=True)
@click.version_option('{0} from {1} (Python {2})'.format(__version__, pgk_dir, sys.version[:3]))
def csptools():
    """
    CSPTools Command line tools
    """


# @csptools.command()
# def cmd1():
#     """Command on cli1"""
#     print("cli1 cmd1")


# 一级命令 CSPtools config
@csptools.group("config")
def config():
    """
    CSPTools config Command line
    """

## todo
"""
token 获取接口，参数，请求方式
数据集下载接口，参数，请求方式
"""


## 二级命令
## 登录验证账号
@config.command()
@click.option("-u", "--username",
              prompt="you can register an account from the platform 'http://192.168.54.151:8181/login.html'",
              help="username of platform")
@click.option("-p", '--password', prompt="your password", hide_input=True, confirmation_prompt=True)
def login(username, password):
    """
    CSPTools config login line
    """


# 一级命令 CSPtools dataset
@csptools.group("dataset")
def dataset():
    """
    CSPTools dataset Command line
    """


## dataset 二级命令
@dataset.command()
def list():
    """
    the info of dataset
    """
    print("list the info of dataset")


@dataset.command()
@click.option("-n", "--name", type=click.STRING, help="dataset name", required=True)
def download(name):
    """
    Command on dataset download
    """
    print("download the dataset: {}".format(name))


# 一级命令 CSPtools model
@csptools.group("model")
def model():
    """
    CSPTools model Command line
    """


# 二级命令 CSPtools model list
@model.command()
def list():
    """
    CSPTools model  list Command line
    """
    image_list = model_list()
    print("repository", "\t", "tag")
    for item in image_list:
        item_l = item.split(":")
        print(item_l[0], "\t", item_l[1], "\n")


# 二级命令 CSPtools model download
@model.command()
@click.option("-n", "--name", prompt="the image name etc. repository:tag", help="the images such as repository:tag",
              required=True)
def download(name):
    """
    CSPTools model download Command line
    """
    model_download(name)


# 二级命令 CSPtools model start
@model.command()
@click.option("-n", "--name", prompt="the image name etc. repository:tag", help="the images such as repository:tag",
              required=True)
@click.option("-c", "--c_name", help="setting the name of container")
@click.option("-p", "--port", help="Port mapping relationship between container and host, such as 5000:5000")
@click.option("-s", "--cmd_s", help="Container initial start command")
@click.option("-l", "--cmd_l", help="Container full start command")
def start(name, c_name, port, cmd_s, cmd_l):
    """
    CSPTools model start Command line
    """
    model_start(name, c_name, port, cmd_s, cmd_l)


# 一级命令 CSPtools server
@csptools.group("resources")
def resources():
    """
    CSPTools resources Command line
    """


@resources.command()
@click.option("-a", "--addr", default=None, help="the url of gitlab")
@click.option("-t", "--private_token", help="the access token", prompt="the access token", required=True,
              hide_input=True, confirmation_prompt=True)
@click.argument("group_name", nargs=-1)
def list(group_name, addr, private_token):
    """
    CSPTools server list line
    """
    server_list(*group_name, url=addr, token=private_token)


@resources.command()
@click.option("-a", "--addr", help="the url of project", required=True)
@click.option("-f", "--folder", type=click.Path(), help="the folder to save project which should not be existed", default=None)
def download(addr, folder):
    """
    CSPTools server download line
    """
    server_download(addr, folder)


# if __name__ == '__main__':
    # csptools()



