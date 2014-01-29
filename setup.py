#!/usr/bin/env python
from distutils.core import setup

setup(
    name='cablestats',
    version="0.1.1",
    description='Hacky hack to get cable stats.  Includes munin plugins.',
    author='Brandon Bennett',
    author_email='bennetb@gmail.com',
    packages=['cablestats'],
    data_files=[
        ('share/cablestats/munin_plugins',
            ['munin_plugins/cablemodem_ds_power',
             'munin_plugins/cablemodem_ds_snr',
             'munin_plugins/cablemodem_us_power']),
    ]
)
