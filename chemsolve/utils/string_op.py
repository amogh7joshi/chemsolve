import re
import sys

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

# Specialized Functions

def oxidation_num(compound):
   '''
   Returns the oxidation number of a compound from the inputted string.
   '''
   if compound[-1] in ["+", "-"]:
      rem = re.findall("[A-Za-z]", compound)
      ind = compound.index(rem[-1])
      if compound[ind + 1].isdigit() and compound[ind + 2].isdigit():
         return compound[-2:]
      else: return compound[-1:]





