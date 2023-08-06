#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages            #这个包没有的可以pip一下

try:
    import torch
except:
    print("Pyorch is required, but its version depends on your device conditions, so it is not included in the dependencies of this package. If you see this warning message, please install Pytorch for your device yourself")

setup(
    name = "SongUtils",      #这里是pip项目发布的名称
    version = "0.0.8",  #版本号，数值大的会优先被pip
    keywords = ["pip", "SongUtils"],
    description = "Junjie's private utils.",
    long_description = "Junjie's private utils.",
    license = "MIT Licence",

    url = "https://github.com/Adenialzz/SongUtils",     #项目相关文件地址，一般是github
    author = "Adenialzz",
    author_email = "1160180309@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["numpy", "pillow", "opencv-python", "tensorboardX"]          #这个项目需要的第三方库
)
