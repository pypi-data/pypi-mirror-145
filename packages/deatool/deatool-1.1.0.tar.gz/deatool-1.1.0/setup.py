#!/usr/bin/env python
# coding: utf-8

from setuptools import setup,find_packages

setup(
    name='deatool',
    version='1.1.0',
    author='WANGY',
    author_email='wangy_prince@126.com',
    url='https://github.com/DEATien',
    description=u'Data envelopment analysis efficiency calculator',
    packages=find_packages(),
    python_requires="<3.10" ,
    install_requires=['pandas','PyQt5','numpy','PyQt5-tools','openpyxl','pyomo'],
)