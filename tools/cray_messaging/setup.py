#!/usr/bin/env python

from distutils.core import setup

setup(name='cray_messaging',
      version='1.0',
      description='Functions for generating and parsing Cray ALPS messages.',
      author='Paul M. Rich',
      py_modules=['cray_messaging'],
      package_dir={'':'lib'})
