#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/3/30 17:06
# @Author  : xgy
# @Site    : 
# @File    : allTools.py
# @Software: PyCharm
# @python version: 3.7.4
"""


import yaml
import os
from common.utils import GitlabAPI, RunSys

path_before = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
path_config = os.path.join(path_before, "common/config", "gitlab.yaml")


def server_list(*args, url, token):
    with open(path_config, "r", encoding="utf-8") as fr:
        data = yaml.load(fr, Loader=yaml.FullLoader)
    if not url:
        url = data["url"]
    git = GitlabAPI(url=url, private_token=token)
    group_pro_l = git.get_group_projects(*args)
    print("repo_url", "\t", "group", "\t", "description")
    for pro in group_pro_l:
        print(pro[0], "\t", pro[1], "\t", pro[2])
        print("\n")
    # return data


def server_download(url, folder):
    if folder:
        cmd_line = "git clone " + url + " " + folder
    else:
        cmd_line = "git clone " + url

    command = RunSys(cmd_line)
    command.run_cli()


if __name__ == '__main__':
    print("start")
    # data = server_list(url=None, token="uuMT9AkxLNpeYVDYAQEv")
    # server_list("人工智能", "safetyctrl", url=None, token="uuMT9AkxLNpeYVDYAQEv")

