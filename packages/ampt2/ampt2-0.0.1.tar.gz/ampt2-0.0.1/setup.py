#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='ampt2',
    version='0.0.1',
    author='Andy Meng',
    author_email='andy_m129@163.com',
    url='https://juejin.cn/user/2875978147966855',
    description="Andy Meng's Python Test",
    packages=['ampt2'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'ampt2=ampt2:ampt2'
        ]
    }
)
