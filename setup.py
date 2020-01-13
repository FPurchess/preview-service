#!/usr/bin/env python
import os

from setuptools import setup


README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()

setup(long_description=README)
