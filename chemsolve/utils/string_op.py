from __future__ import division

import re
import sys

from chemsolve.utils.constants import REDOX, BASEREDOX
from chemsolve.element import Element
from chemsolve.compound import Compound

# A loose collection of functions which perform operations on strings.

# General Functions

def split(string):
   '''
   Takes in a string, returns a list containing each character in the string.
   '''
   return [char for char in string]

def num_in_string(string):
   '''
   Takes in a string, returns each of the numbers within the string.
   '''
   return [char for char in string if (char.is_digit() == True)]

def index_gather(main, choose):
   '''
   Returns certain indices of a string, based on which ones are given.
   '''
   return [n for n in range(len(main)) if main[n] in choose]

# Specialized Functions

def charge(compound):
   """Returns the charge of a compound from the inputted string."""
   if compound[-1] in ["+", "-"]:
      rem = re.findall("[A-Za-z]", compound)
      ind = compound.index(rem[-1])
      if compound[ind + 1].isdigit() and compound[ind + 2].isdigit():
         return [compound[:-2], compound[-2:]]
      try:
         Element(compound[: len(compound) - 1]); return [compound[:-1], compound[-1:]]
      except:
         pass
      try:
         Element(compound[: len(compound) - 2]); return [compound[:-2], compound[-2:]]
      except:
         pass
      return [compound[:-1], compound[-1:]]
   else:
      return [compound, 0]

def compound_index_gather(main, choose): # TODO: May not work for double-digit subscripts.
   """Adds to the initial indices from index_gather the indices of the subscript of an ignored substring."""
   comp = Compound(main)
   indices = []
   for element in comp.compound_elements:
      if Element(element).element_symbol in choose:
         for i in Element(element).element_symbol:
            indices.append(*index_gather(main, i))

   for index in indices:
      if (index + 1) < len(main):
         if main[index + 1].isdigit():
            indices.append(index + 1)

   return indices

def charge_value(input):
   """Returns the numerical value of the charge from the string."""
   charges = {
      0: 0,
      "0": 0,
      "+" or "+1" or "1+": 1,
      "2+" or "+2": 2,
      "3+" or "+3": 3,
      "4+" or "+4": 4,
      "5+" or "+5": 5,
      "-" or "-1" or "1-": -1,
      "2-" or "-2": -2,
      "3-" or "-3": -3,
      "4-" or "-4": -4,
      "5-" or "-5": -5
   }

   return charges[input]

# Master Functions

def ignore(list, param = None, ignore = None, *args):
   """Returns a string without certain substrings as determined by the parameter or arguments."""
   choose = []
   newlist = []
   if param is None:
      choose.append(args)
   if param == REDOX:
      choose = ["H", "O"]
   if param == BASEREDOX:
      choose = ["H", "O", "Na", "K", "Li", "Cl", "F", "Br", "Ca"]
   if ignore is not None:
      choose.append(*ignore)
   for item in list:
      remove = compound_index_gather(item, choose)
      newlist.append(''.join(char for indx, char in enumerate(item) if indx not in remove))
   return newlist

def oxidation_number(comp, charge, param = None):
   """Returns the oxidation number of a main element in a compound."""
   rest_charge = 0
   compound = Compound(comp)
   preset = {
      "O": -2,
      "H": 1,
      "F": -1,
      "Na" or "K" or "Li" or "Rb" or "Cs": 1,
      "Be" or "Mg" or "Ca" or "Sr" or "Ba": 2
   }
   main = ignore([comp], param = REDOX, ignore = param)
   if main[0][-1].isdigit():
      main[0] = main[0][:-1]
   in_compound = compound.compound_elements
   for element in in_compound:
      try:
         rest_charge += preset[element] * in_compound[element]
      except:
         pass
   charge = charge_value(charge)
   num = int((charge - rest_charge) / in_compound[main[0]])
   return num

def num_in(nums, list):
   """Whether the number of items in a list is as it should be."""
   i = 0
   for obj in list:
      if obj:
         i += 1
   return i == nums







