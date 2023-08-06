# !/usr/bin/env python
# -*- coding:utf-8 -*- setuptools
import setuptools

setuptools.setup(
    name='fuckzk',
    version='0.0.4',
    author='WildboarG',
    author_email='959586@outlook.com',
    url='https://wildboarg.github.io/',
    description=u'A small function to obtain the health reporting and submission information of Zhengzhou Institute of science and technology.',
    long_description_content_type="text/markdown",
    long_description = "test Module",
    packages=setuptools.find_packages(),
    install_requires=['requests>=2.27.1'],
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
        ]
)
