#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: wangyongpeng
# Mail: 1690992651@qq.com
# Created Time:  2022-03-15
#############################################

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name="ZHUANZHUANBktUtil",      #这里是pip项目发布的名称
    version="2.1.2",  #版本号，数值大的会优先被pip
    keywords=("pip", "wangyongpeng","tree"),
    description="toad包来进行分桶。",
    long_description="toad包来进行分桶",
    license="BSD Licence",

    url="https://github.com/HeiBoWang/DecisionTreeBktUtil",     # 项目相关文件地址，一般是github
    author="wangyongpeng",
    author_email="wangyongpeng@zhuanzhuan.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any"
)


