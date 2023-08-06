#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/3/29 10:20
# @Author  : xgy
# @Site    : 
# @File    : url.py
# @Software: PyCharm
# @python version: 3.7.4
"""
from dataclasses import dataclass


@dataclass
class UrlConfig:
    nexus_url: str = "http://192.168.54.151"
    nexus_port: str = "18081"
    repository: str = "docker"
    format: str = "docker"
    name: str = None


@dataclass
class GitConfig:
    git_url: str = None
    name: str = None





if __name__ == '__main__':
    print("start")
