# -*- coding: utf-8 -*-
import codecs
import os
import re
import setuptools


def local_file(file):
    return codecs.open(
        os.path.join(os.path.dirname(__file__), file), 'r', 'utf-8'
    )

setuptools.setup(
    name="people_also_ask_it",
    version="0.2",
    author="intelligenzaartificialeitalia.net",
    author_email="",
    packages=setuptools.find_packages(),
    long_description=local_file('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
	"Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
    ],
    install_requires=[
        "beautifulsoup4",
        "requests",
    ],
    python_requires=">=3.6"
)
