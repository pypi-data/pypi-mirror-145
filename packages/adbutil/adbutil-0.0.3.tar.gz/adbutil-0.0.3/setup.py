# -*- coding: utf-8 -*-
# @Time   : 2022/4/6 10:31
# @Author : w


from setuptools import setup, find_packages

setup(
    name='adbutil',
    version='0.0.3',
    author='jayden',
    author_email='282669595@qq.com',
    url='https://blog.csdn.net/Jonder_wu?type=blog',
    description=u'android flash update da',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'flash=flash:pp_flash',
            'jujube=flash:jujube',
        ]
    }
)
