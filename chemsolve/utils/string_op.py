import re
import sys

from .constants import REDOX
from ..element import Element

'''
A loose collection of functions which perform operations on strings.
'''

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
   '''
   Returns the charge of a compound from the inputted string.
   '''
   if compound[-1] in ["+", "-"]:
      rem = re.findall("[A-Za-z]", compound)
      ind = compound.index(rem[-1])
      if compound[ind + 1].isdigit() and compound[ind + 2].isdigit():
         return [compound[:-2], compound[-2:]]
      try:
         Element(compound[: len(compound) - 1]); return [compound[:-1], compound[-1:]]
      except: pass
      try:
         Element(compound[: len(compound) - 2]); return [compound[:-2], compound[-2:]]
      except: pass
      return [compound[:-1], compound[-1:]]
   else: return [compound, 0]

def compound_index_gather(main, choose): #TODO: May not work for double-digit subscripts.
   indices = index_gather(main, choose)
   for index in indices:
      if (index + 1) < len(main):
         if main[index + 1].isdigit():
            indices.append(index + 1)
   return indices

# Master Functions

def ignore(list, param = None, *args):
   global choose, newlist
   newlist = []
   if param == None:
      choose.append(args)
   if param == REDOX:
      choose = ["H", "O"]
   for item in list:
      remove = compound_index_gather(item, choose)
      newlist.append(''.join(char for indx, char in enumerate(item) if indx not in remove))
   return newlist







