#!/usr/bin/env python

from distutils.core import setup
from cablestats import __version__ as version

setup(
    name = 'cablestats',
    version = version,
    description = 'Hacky hack to get cable stats.  Includes munin plugins',
    author = 'Brandon Bennett',
    author_email = 'bennetb@gmail.com',
    packages = ['cablestats'],
)