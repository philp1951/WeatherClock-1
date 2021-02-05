#! /usr/bin/env python3

from distutils.core import setup
from setuptools import setup
setup(name='WeatherClock',
      version='1.0',
      description='Raspberry Pi Radio Studio Clock with Weather',
      author='Phil Pugh',
      author_email='philpugh51@outlook.com',
      url='http://github.com/philpugh1951/WeatherClock',
      scripts=['weatherclock.py'],
      requires=['pygame'],
      install_requires=['pygame'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: Console :: Framebuffer',
          'Intended Audience :: System Administrators',
          'Intended Audience :: Customer Service',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Operating System :: POSIX :: Linux',
          'Topic :: Utilities',
          ],
      )
