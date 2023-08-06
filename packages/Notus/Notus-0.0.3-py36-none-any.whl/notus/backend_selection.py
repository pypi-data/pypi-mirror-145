#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 04-01-2021
           """

import os

from draugr.os_utilities import get_backend_module
from notus import PROJECT_NAME

__all__ = ["Class"]

Class = get_backend_module(
    PROJECT_NAME, os.environ.get("NOTUS_BACKEND", None)
).Class  # Change !Class! to backend class   #TODO: NOT DONE!
del get_backend_module

if __name__ == "__main__":
    print(Class.__doc__)
