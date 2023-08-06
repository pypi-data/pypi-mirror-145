#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="genius_lite",
    version="0.1.0",
    keywords=("spider"),
    description="spider frame",
    long_description="spider frame",
    license="MIT Licence",

    url="https://github.com/f840415070/genius-lite",
    author="fanyibin",
    author_email="f84041507@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['requests']
)
