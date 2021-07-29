#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
import re

package = 'pandas-excel-limitedrows'

with open('README.md', 'rb') as f:
    readme = f.read().decode('utf-8')


setup(
    name='pandas-excel-limitedrows',
    packages=find_packages(),
    version='1.0.0',
    description='Pandas Extension Package used to read Excel files with limit rows',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Ivan Bolorino',
    author_email='ivan.bolorino@gmail.com',
    url='https://github.com/ibolorino/pandas-excel-limitrows',
    install_requires=['pandas', 'openpyxl'],
    license='MIT',
    keywords=['dev', 'web', 'pandas', 'excel', 'data science'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)