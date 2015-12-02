# -*- coding: utf-8 -*-
"""
setup file for creating python package usfEP
"""
from setuptools import setup
from setuptools import find_packages

setup(name='usfEP',
      version='0.1',
      description='Invert GPS data for Euler Vector for plate motion',
      url='https://github.com/USFgeodesy/usfEP.git',
      author='Nick Voss',
      author_email= 'nvoss@mail.usf.edu',
      license='MIT',
      packages=find_packages(),
      zip_safe=False)
