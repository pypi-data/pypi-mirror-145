#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/3/25 14:48
# @Author  : xgy
# @Site    : 
# @File    : setup.py.py
# @Software: PyCharm
# @python version: 3.7.4
"""

from setuptools import setup, find_packages

setup(
    name='csptools',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['Click', 'requests'],
    entry_points='''
        [console_scripts]
        CSP=command.cli:csptools
    ''',
    classifiers=[
        # 发展时期,常见的如下
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # 开发的目标用户
        'Intended Audience :: Developers',

        # 属于什么类型
        'Topic :: Software Development :: Build Tools',

        # 许可证信息
        'License :: OSI Approved :: MIT License',

        # 目标 Python 版本
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ]
)

# CSPTools=command.cli:csptools，从 command 开始
