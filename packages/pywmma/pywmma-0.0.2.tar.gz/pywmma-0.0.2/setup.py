#! /usr/bin/env python
# -*- coding: utf-8 -*_
# Author: ***<***gmail.com>
from distutils.core import setup
import setuptools

setup(
    name='pywmma', # 包的名字
    version='0.0.2',  # 版本号
    description='Python Wrapper On mma',  # 描述
    author='xjq', # 作者
    author_email='xjq701229@outlook.com',  # 你的邮箱**
    url='',  # 可以写github上的地址，或者其他地址
    packages=setuptools.find_packages(exclude=[]),  # 包内不需要引用的文件夹
    
    # 依赖包
    install_requires=[
        "wolframclient",
    ],
    classifiers=[
        # 'Development Status :: 4 - Beta',
        # 'Operating System :: Microsoft'  # 你的操作系统
        # 'Intended Audience :: Developers',
        # 'License :: OSI Approved :: BSD License', # BSD认证
        # 'Programming Language :: Python',   # 支持的语言
        'Programming Language :: Python :: 3',  # python版本 。。。
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
        # 'Programming Language :: Python :: 3.6',
        # 'Topic :: Software Development :: Libraries'
    ],
    zip_safe=True,
)
