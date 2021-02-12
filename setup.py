from os import path
from setuptools import setup
from setuptools import find_packages

directory = path.abspath(path.dirname(__file__))
with open(path.join(directory, 'README.md'), encoding = 'utf-8') as f:
   long_description = f.read()


setup(
   name = 'chemsolve',
   version = '1.7.0',
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
