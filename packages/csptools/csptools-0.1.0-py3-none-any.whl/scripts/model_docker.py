#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/3/29 10:18
# @Author  : xgy
# @Site    : 
# @File    : model_docker.py
# @Software: PyCharm
# @python version: 3.7.4
"""
from dataclasses import dataclass

import requests
import json
from common.url import UrlConfig
from common.utils import RunSys


@dataclass
class DockerConfig(UrlConfig):
    nexus_port: str = "28081"
    repository: str = "opspipe/aip"
    tag: str = None


def model_list():
    """
    从nexus上获取docker镜像列表
    :return:
    """
    docker_url_info = UrlConfig(name="opspipe/aip")
    image_url = docker_url_info.nexus_url + ":" + docker_url_info.nexus_port + "/" + "service/rest/v1/search"
    params = {"repository": docker_url_info.repository, "format": docker_url_info.format, "name": docker_url_info.name}

    res = requests.get(image_url, params=params)
    res_dict = json.loads(res.text)

    images_list = []
    for image in res_dict["items"]:
        image_item = image["name"] + ":" + image["version"]
        images_list.append(image_item)

    return images_list


def model_download(name):
    """
    按镜像名称下载镜像文件
    :param name: 镜像名称（images:tag）
    :return:
    """
    images, tag = name.split(":")
    docker_config = DockerConfig(repository=images, tag=tag)
    cmd_line = "docker pull " + docker_config.nexus_url.replace("http://", "") + ":" + docker_config.nexus_port + "/" + name
    command = RunSys(cmd_line)
    command.run_cli()


def model_start(name, c_name, port, cmd_s=None, cmd_l=None):
    """
    启动模型镜像服务
    :param cmd_s: 容器初始启动命令，默认为 sh run.sh
    :param c_name: 容器名称
    :param port: 容器/宿主机端口映射
    :param cmd_l: 完整镜像启动命令，若有值，则其他参数不起作用
    :param name: 模型镜像名称
    :return:
    """
    docker_config = DockerConfig()
    if cmd_l:
        cmd_line = cmd_l
    else:
        if cmd_s:
            cmd_line = "docker run -d --name " + c_name + " -p " + port + " " + \
                       docker_config.nexus_url.replace("http://", "") + ":" + docker_config.nexus_port + "/" + name + \
                       " " + cmd_s
        else:
            cmd_line = "docker run -d --name " + c_name + " -p " + port + " " + \
                       docker_config.nexus_url.replace("http://", "") + ":" + docker_config.nexus_port + "/" + name + \
                       " " + "sh run.sh"

    command = RunSys(cmd_line)
    command.run_cli()


if __name__ == '__main__':
    print("start")

