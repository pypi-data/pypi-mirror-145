# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 14:42:23 2022

@author: Florian Ellsäßer
"""

import setuptools


setuptools.setup(name='harvest-indices',
      version='0.0.1',
      description='Calculate harvest anomalies from historical harvest data.',
      author='Florian Ellsäßer',
      author_email='info@cropdata.de',
      license='CC BY-NC-SA',
      packages=['harvest_indices'],
      install_requires=[
          'numpy','pandas','statsmodels'
      ]
      )

