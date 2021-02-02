#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="schoolstat",
    version="1.0",
    author="Barbara Jurzysta",
    author_email="b.jurzysta@student.uw.edu.pl",
    description="Package for analysis of Polish schools and population",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.uw.edu.pl/bj394093/schoolstat',
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6.0',
    install_requires=['pandas', 'openpyxl', 'xlrd'],
)
