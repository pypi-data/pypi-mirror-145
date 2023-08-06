#!/usr/bin/python3
# -*- coding: utf-8 -*-
import setuptools
with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()
setuptools.setup(
    name="xyzrequest",  # 模块名称
    version="2022.1",  # 当前版本
    author="SunnyLi",  # 作者
    author_email="5327136@qq.com",  # 作者邮箱
    description="Modules that make the API easy to get\n 简单API爬虫获取",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        "requests",
        "requests_toolbelt",
        "urllib3",
        "removebg",
        "ISS-info",
        "pillow",
    ],
    python_requires='>=3',
)