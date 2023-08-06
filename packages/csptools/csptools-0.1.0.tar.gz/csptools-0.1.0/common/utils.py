#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/3/29 15:22
# @Author  : xgy
# @Site    : 
# @File    : utils.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import subprocess
import shlex
import time
import traceback
import gitlab

import os
import sys


class RunSys:
    """
    执行 shell 命令
    """

    def __init__(self, command: str = None):
        self.command = command
        self.output = None

    def run_cli(self):
        cmd = shlex.split(self.command)
        try:
            # output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            subprocess.check_call(cmd, stderr=subprocess.STDOUT)
            # self.output = output.decode()
        except subprocess.CalledProcessError as e:
            print(traceback.print_exc())


# __test_private_token__ = 'uuMT9AkxLNpeYVDYAQEv'
__test_private_token__ = 'rDYfmk1ZkEQ4phz8RxUa'
__gitlab_url__ = 'http://192.168.55.37:12001/'


class GitlabAPI(object):
    """
    获取工具集 gitlab 工程列表
    """

    def __init__(self, url=__gitlab_url__, private_token=__test_private_token__):
        # self.gl = gitlab.Gitlab()
        self.private_token = private_token
        self.url = url
        self.gl = gitlab.Gitlab(url=self.url, private_token=self.private_token)
        self.groups = []
        self.projects = []

    def get_all_projects(self):
        projects = self.gl.projects.list(all=True)
        result_list = []
        for project in projects:
            result_list.append(project.http_url_to_repo)
            self.projects.append(project)
        return result_list

    def get_group(self):
        group_list = []
        items = self.gl.groups.list(as_list=False)
        for item in items:
            group_list.append(item.attributes)
            self.groups.append(item)
        return group_list

    def get_group_projects(self, *args):
        group_projects = []
        _ = self.get_group()
        for item in self.groups:
            if args:
                if item.name in args:
                    projects = item.projects.list()
                    for project in projects:
                        # group_projects.append(project.http_url_to_repo)
                        # group_projects.append(project.attributes)
                        group_projects.append([project.http_url_to_repo, project.namespace["name"], project.description])
            else:
                projects = item.projects.list()
                for project in projects:
                    # group_projects.append(project.attributes)
                    group_projects.append([project.http_url_to_repo, project.namespace["name"], project.description])
        return group_projects

    # def get_group_projects(self, *args):
    #     group_projects = []
    #     _ = self.get_group()
    #     for item in self.groups:
    #         len_group = len(item.projects.list())
    #         if args:
    #             if item.name in args:
    #                 for i in range(0, len_group):
    #                     group_project = item.projects.list()[i]
    #                     manageable_project = self.gl.projects.get(group_project.id, lazy=True)
    #                     group_projects.append(manageable_project)
    #         else:
    #             for i in range(0, len_group):
    #                 group_project = item.projects.list()[i]
    #                 manageable_project = self.gl.projects.get(group_project.id, lazy=True, include_subgroups=True)
    #                 group_projects.append(manageable_project)
    #     return group_projects

    def __export_project(self, name):
        """
        导出工程，gitlab工程对象，非工程源码
        :param name:
        :return:
        """
        _ = self.get_all_projects()
        for project in self.projects:
            if name == project.name:
                # Create the export
                id = project.id
                p = self.gl.projects.get(project.id)
                export = p.exports.create()

                # Wait for the 'finished' status
                export.refresh()
                while export.export_status != 'finished':
                    time.sleep(1)
                    export.refresh()

                # Download the result
                with open('../test/export.tgz', 'wb') as f:
                    export.download(streamed=True, action=f.write)


if __name__ == '__main__':
    print("start")

    # user_name ='xgy'
    groupname = ["人工智能", "safetyctrl"]
    # groupname = ["人工智能", "safetyctrl"]

    git = GitlabAPI()
    # pro_all = git.get_all_projects()
    # group_list = git.get_group()
    group_pro_l = git.get_group_projects()
    # git.export_project("pdf_check")
