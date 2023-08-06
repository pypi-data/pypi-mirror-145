# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 14:17:56 2022

@author: Florian Ellsäßer
"""

# this is a statement that is printed to check weather the package has been imported correctly
print(f'Invoking __init__.py for {__name__}')


# this will import all modules of the package with *
__all__ = [
        'indices',
        'utils'
        ]