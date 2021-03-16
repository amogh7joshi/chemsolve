#!/usr/bin/env python3
# -*- coding = utf-8 -*-
import os
from setuptools import setup
from setuptools import find_packages

# Get the long README description.
with open(os.path.join(
         os.path.dirname(__file__), 'README.md'), encoding = 'utf-8') as f:
   long_description = f.read()

# Get the version from the module.
def configure_chemsolve_version():
   """Configures the module version directly from the package."""
   # Import the version.
   # noinspection PyProtectedMember
   from chemsolve._release import __version__

   # Check for certain cases.
   if len(__version__) == 4:
      end_tag = __version__[3]
      return ".".join(str(item) for item in __version__[:3]) + f"-{end_tag}"
   return ".".join(str(item) for item in __version__)

setup(
   name = 'chemsolve',
   version = configure_chemsolve_version(),
   author = "Amogh Joshi",
   packages = find_packages(),
   author_email = "joshi.amoghn@gmail.com",
   url = "https://github.com/amogh7joshi/chemsolve",
   license = 'MIT',
   description = "A low-level chemistry library for solving and practicing chemistry problems.",
   long_description = long_description,
   long_description_content_type = "text/markdown",
   classifiers = [
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent"
   ],
   include_package_data = True
)
