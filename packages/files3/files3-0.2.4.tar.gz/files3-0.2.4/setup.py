#!/usr/bin/env python
# coding:utf-8

from setuptools import find_packages, setup

setup(
name='files3',
version='0.2.4',
description='(pickle based) save Python objects in binary to the file system and manage them (more convenient?)',
author="Eagle'sBaby",
author_email='2229066748@qq.com',
maintainer="Eagle'sBaby",
maintainer_email='2229066748@qq.com',
packages=find_packages(),
platforms=["all"],
license='Apache Licence 2.0',
classifiers=[
'Programming Language :: Python',
'Programming Language :: Python :: 3',
],
install_requires = ["pycryptodome"],
keywords = ['pickle', 'files', "object"],
python_requires='>=3', 
)