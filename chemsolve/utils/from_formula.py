import sys
import operator

from math import isclose
from math import floor, ceil

# Methods used by the former FormulaCompound class.
# Returns the empirical/molecular formula of a compound based on the elements in it.

def determine_empirical_coef(compound_elements):
   '''
   Returns the coefficients of the empirical formula of the element.
   '''
   coef_list = []
   for element in compound_elements:
      if element.percent_of != False:
         coef_list.append(operator.truediv(operator.mul(element.percent_of, 100), element.mass))
      if element.gram_amount != False:
         coef_list.append(operator.truediv(element.gram_amount, element.mass))
      if element.mole_amount != False:
         coef_list.append(element.mole_amount)

   least = sys.maxsize
   for item in coef_list:
      if item < least:
         least = item
   coef_list_2 = []
   solved = True
   for item in coef_list:
      t = round(operator.truediv(item, least), 2)
      if not isclose(t, floor(t), abs_tol=10 ** -1) and not isclose(t, ceil(t), abs_tol=10 ** -1):
         solved = False
         coef_list_2.append(t)
      else:
         coef_list_2.append(round(t, 1))

   factor = 2
   coef_list_3 = coef_list_2.copy()
   coef_list_4 = []
   overall_solved = True
   while solved == False:
      overall_solved = False
      if solved == False:
         for item in coef_list_3:
            if not isclose(item, floor(item), abs_tol=10 ** -1) and not isclose(item, ceil(item), abs_tol=10 ** -1):
               z = True
               while z == True:
                  if round(operator.mul(item, factor), 1).is_integer():
                     z = False
                  else:
                     factor += 1
         for item in coef_list_3:
            coef_list_4.append(round(operator.mul(item, factor), 1))
         coef_list_3 = coef_list_4.copy()
         coef_list_4 = []
         for t in coef_list_3:
            if not isclose(t, floor(t), abs_tol=10 ** -1) and not isclose(t, ceil(t), abs_tol=10 ** -1):
               solved = False
            else:
               solved = True

   if overall_solved == False:
      return coef_list_3
   return coef_list_2


def determine_empirical(compound_elements, empirical_coef):
   '''
   Returns the empirical formula of the compound.
   '''
   form = ""
   next = False
   for index, (element, coef) in enumerate(zip(compound_elements, empirical_coef)):
      if next == False:
         if index != len([a for a in zip(compound_elements, empirical_coef)]) - 1:
            if int(empirical_coef[index] == empirical_coef[index + 1]) \
                  and int(empirical_coef[index]) != 1:
               form += "(" + str(element.__repr__()) \
                        + str(compound_elements[index + 1].__repr__()) \
                        + ")" + str(int(coef))
               next = True
            else:
               form += str(element.__repr__())
               if int(coef) != 1:
                  form += str(int(coef))
               next = False
         else:
            form += str(element.__repr__())
            if int(coef) != 1:
               form += str(int(coef))
            next = False
      else: pass

   return form

def determine_molecular(empirical_mass, compound_elements, empirical_coef, mol_mass, molecular = False):
   '''
   Returns the molecular formula of the element, if the molar mass is provided.
   '''
   form = ""
   if molecular == True:
      d = round(operator.truediv(mol_mass, empirical_mass), 1)
      if not d.is_integer():
         raise ValueError("Enter a molar mass that is an integer multiple of the empirical mass.")
      for element in zip(compound_elements, empirical_coef):
         form += str(element[0].__repr__())
         if int(element[1] * d) != 1:
            form += str(int(element[1] * d))

   return form







