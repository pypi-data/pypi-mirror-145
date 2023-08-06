#!/usr/bin/env python

import os
from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, 'google_ime_skk_py', '__version__.py'),
          mode='r', encoding='utf-8') as f:
    exec(f.read(), about)

with open('README.md', mode='r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name=about['__title__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    url=about['__url__'],
    version=about['__version__'],
    author=about['__author__'],
    license=about['__license__'],
    python_requires='>=3.6',
    packages=find_packages(),
    entry_points={
        "console_scripts":
        ["google-ime-skk-py=google_ime_skk_py.google_ime_skk:main"]
    }
)
