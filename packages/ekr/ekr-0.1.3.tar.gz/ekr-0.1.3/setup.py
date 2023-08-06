#!/usr/bin/env python
# coding:utf-8

from setuptools import find_packages, setup

setup(
name='ekr',
version='0.1.3',
description='MicroKernel based on eventframework as it\'s inner core. Use python project as plugin.',
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
install_requires = ["mkr>=0.1.0", 'efr>=0.1.9'],
keywords = ["microkernel", "event-driven"],
python_requires='>=3', 
)