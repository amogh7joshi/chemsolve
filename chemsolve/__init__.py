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

# Import package version and set it up.
from ._release import __version__
__version__ = '.'.join(str(item) for item in __version__)

# Import general Chemsolve functionalities.
from .element import *
from .compound import *
from .reaction import *

from .solutions.molar import molarity

from .utils.constants import *

# Import all of the different errors to the top-level API.
from .utils.errors import (
   ChemsolveError, InvalidChemistryArgumentError,
   InvalidElementError, InvalidCompoundError, InvalidReactionError
)

# TO BE ADDED IN THE NEAR FUTURE
# from .quantum.photoelectric import energy_change, level_transition

# TOP-LEVEL METHODS FOR BASIC CHEMICAL INTERACTIONS (a lot of lists, essentially).

def list_valid_elements():
   """Creates a list of valid elements.

   Returns
   -------
   A list of every valid element from the Periodic Table.
   """
   elements = []

   from .utils.periodictable import PeriodicTable as _PeriodicTable
   _table = _PeriodicTable()

   for _element in _table['Name']:
      elements.append(_element)

   print(elements)

def list_strong_acids(return_compounds = False):
   """Creates a list of strong acids.

   Parameters
   ----------
   return_compounds: bool
      If set to true, then this method will return a list of
      `chemsolve.Compound` objects containing the strong acids.

   Returns
   -------
   A list of each of the valid strong acids.
   """
   from .utils.constants import STRONG_ACIDS as _STRONG_ACIDS
   if return_compounds:
      return [Compound(strong_acid) for strong_acid in _STRONG_ACIDS]
   else:
      return _STRONG_ACIDS

def list_strong_bases(return_compounds = False):
   """Creates a list of strong bases.

   Parameters
   ----------
   return_compounds: bool
      If set to true, then this method will return a list of
      `chemsolve.Compound` objects containing the strong bases.

   Returns
   -------
   A list of each of the valid strong bases.
   """
   from .utils.constants import STRONG_BASES as _STRONG_BASES
   if return_compounds:
      return [Compound(strong_base) for strong_base in _STRONG_BASES]
   else:
      return _STRONG_BASES


