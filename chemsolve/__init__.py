#!/usr/bin/env python3
# -*- coding = utf-8 -*-
import warnings
# warnings.filterwarnings("ignore")
import logging
logging.basicConfig(format = '%(levelname)s - %(name)s: %(message)s')

# Update logging configuration.
class DuplicateLog(object):
   def __init__(self):
      self.messages = set()

   def filter(self, record):
      rv = record.msg not in self.messages
      self.messages.add(record.msg)
      return rv

# Import general Chemsolve functionalities.
from .element import *
from .compound import *
from .reaction import *

from .solutions.molar import molarity

from .utils.constants import *

# TO BE ADDED IN THE NEAR FUTURE
# from .quantum.photoelectric import energy_change, level_transition

# High-level methods.
def list_valid_elements():
   """Creates a list of valid elements."""
   elements = []

   from .utils.periodictable import PeriodicTable as _PeriodicTable
   _table = _PeriodicTable()

   for _element in _table['Name']:
      elements.append(_element)

   print(elements)
