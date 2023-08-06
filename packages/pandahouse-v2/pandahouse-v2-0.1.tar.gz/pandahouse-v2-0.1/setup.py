#!/usr/bin/env python

import versioneer
from os.path import exists
from setuptools import setup


setup(name='pandahouse-v2',
      version='0.1',
      description='Pandas interface for Clickhouse HTTP API forked from pandahouse',
      url='https://github.com/ayushdeqode/pandahouse',
      maintainer='Ayush',
      maintainer_email='example@gmail.com',
      license='BSD',
      keywords='',
      packages=['pandahouse'],
      tests_require=['pytest'],
      setup_requires=['pytest-runner'],
      install_requires=['pandas', 'requests', 'toolz'],
      long_description=(open('README.rst').read() if exists('README.rst')
                        else ''),
      zip_safe=False)
