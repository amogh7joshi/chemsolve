import operator
import re
import sys

from chempy import Substance
from chempy import balance_stoichiometry
from chempy import Equilibrium

from math import isclose
from math import floor, ceil

from chemsolve.element import Element
from chemsolve.element import SpecialElement
from chemsolve.utils.string_op import split

try:
   import periodictable as pt
except ModuleNotFoundError:
   print("The module periodictable has not been installed.")
except ImportError:
   print("The module periodictable could not be found (may have not been installed).")


class Compound:
   def __init__(self, compound, *args, **kwargs):
      self.compound = pt.formula(compound)
      self.mass = self.get_mass()
      self.compound_elements_list = self.__get_elements_in_compound_ions(compound)
      self.compound_elements = {}
      self.compound.elements = self.get_elements_in_compound()
      self.print_compound = Substance.from_formula(compound)

      '''
      The class can calculate quantities of moles and grams, depending on the specific keywords 'moles' and 'grams'.
      '''
      if "moles" in kwargs:
         self.mole_amount = kwargs["moles"]
         self.gram_amount = round(operator.mul(self.mole_amount, self.mass), 4)

      if "grams" in kwargs:
         self.gram_amount = kwargs["grams"]
         self.mole_amount = round(operator.truediv(self.gram_amount, self.mass), 4)

      if "volume" in kwargs:
         #TODO: Moles from molarity.
         self.volume = kwargs["volume"]

      if "moles" in kwargs and "grams" in kwargs:
         raise ValueError("You cannot provide both the number of moles and grams of the element at a single time.")
      if "grams" in kwargs and "volume" in kwargs:
         raise ValueError("You cannot provide both the volume and the gram value at the same time.")

   def __str__(self):
      return str(self.print_compound.unicode_name)

   def __repr__(self):
      return str(self.compound)

   def __getattr__(self, item):
      if not item in ["mole_amount", "gram_amount", "volume"]:
         print("The attribute " + str(item) + " does not exist within this class or has not been defined yet.")

   def __call__(self, **kwargs):
      if "moles" in kwargs:
         self.mole_amount = kwargs["moles"]
         self.gram_amount = round(operator.mul(self.mole_amount, self.mass), 4)

      if "grams" in kwargs:
         self.gram_amount = kwargs["grams"]
         self.mole_amount = round(operator.truediv(self.gram_amount, self.mass), 4)

      if "volume" in kwargs:
         #TODO: Moles from molarity.
         self.volume = kwargs["volume"]

      if "moles" in kwargs and "grams" in kwargs:
         raise Exception("You cannot provide both the number of moles and grams of the element at a single time.")
      if "grams" in kwargs and "volume" in kwargs:
         raise ValueError("You cannot provide both the volume and the gram value at the same time.")

   '''
   Functions which gather attributes.
   '''
   def get_mass(self):
      '''
      Returns the atomic (and therefore molar) mass of the compound.
      '''
      return self.compound.mass

   def __get_elements_in_compound_ions(self, compound):
      '''
      Returns each of the individual polyatomic ions in the element (both element symbol and number).
      '''
      t = compound
      if "(" in t:
         if ")" not in t:
            raise TypeError("That is not a valid format for a compound.")
         left = t.index("(")
         right = t.index(")")
         charge = int(t[right + 1])
         f = re.findall('[A-Z][^A-Z]*', t[(left + 1):right])
         replacer = ""
         for val in f:
            val = str(val)
            if val[-1].isdigit():
               z = val[-1]
               val = val[:-1]
               q = str(int(z) * int(charge))
               val += q
            else:
               val += str(charge)
            replacer += val

         t = t[:left] + str(replacer)

      return re.findall('[A-Z][^A-Z]*', str(t))

   def get_elements_in_compound(self):
      '''
      Returns a dictionary containing the elements in the compound and the quantity of each element.
      '''
      for item in self.compound_elements_list:
         item_val = split(item)
         if item_val[-1].isdigit():
            if item_val[-2].isdigit():
               pass
               self.compound_elements.update({''.join(item_val[:-2]): int(''.join(item_val[-2:]))})
            else:
               self.compound_elements.update({''.join(item_val[:-1]): int(item_val[-1])})
         else:
            self.compound_elements.update({item: 1})

   '''
   Functions which perform calculations.
   '''
   def moles_in_compound(self, element):
      '''
      Returns the number of moles of a certain element within one mole of the compound.
      '''
      try:
         return(self.compound_elements[element])
      except KeyError:
         print("That is not an element in this compound.")
      except AttributeError:
         print("That is not an element.")

   def percent_in_compound(self, element):
      '''
      Returns the percentage of a certain element within the compound.
      '''
      try:
         return round(operator.truediv((Element(element.title()).mass * self.compound_elements[element]), self.mass), 4)
      except KeyError:
         print("That is not an element in this compound.")
      except AttributeError:
         print("That is not an element.")

class FormulaCompound(Compound):
   '''
   Finds empirical, molecular, and other formulas of a compound.

   Has mostly similar attributes to the Compound class, but different inputs.
   Takes in gram/mole values of different elements within a theoretical compound
   and determines the empirical & molecular formulas.
   If the parameter molecular is true, then the class must have a molar mass attribute.
   It will then return the stored formula of the compound as the molecular formula instead of the empirical formula.

   **Use the SpecialElement class to define elements which are going to be used to determine the compound.
   '''
   def __init__(self, *args, molecular = False, **kwargs):
      self.__compound_elements = []

      if len(args) < 2:
         raise ValueError("You may be using the wrong class. The FormulaCompound class is used to determine compound formulas.")
      for element in args:
         if not isinstance(element, SpecialElement):
            raise TypeError("The arguments of this class should only be SpecialElement classes.")
         else:
            self.__compound_elements.append(element)

      if "mass" in kwargs:
         self.molar_mass = kwargs["mass"]

      self.__empirical_coef = self.__determine_empirical_coef()
      self.empirical = Compound(self.determine_empirical())
      self.__empirical_mass = Compound(self.empirical.__repr__()).mass
      if molecular == True:
         self.molecular = self.determine_molecular(self.molar_mass, molecular = True)
         super().__init__(compound = self.molecular)
      else:
         super().__init__(compound = self.empirical.__repr__())

   def __call__(self, *args, molecular = False, **kwargs):
      if "mass" in kwargs:
         self.molar_mass = kwargs["mass"]

   def __determine_empirical_coef(self):
      '''
      Private method. Returns the coefficients of the empirical formula of the element.
      '''
      coef_list = []
      for element in self.__compound_elements:
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
         if not isclose(t, floor(t), abs_tol = 10 ** -1) and not isclose(t, ceil(t), abs_tol= 10 ** -1):
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

   def determine_empirical(self):
      '''
      Returns the empirical formula of the compound.
      '''
      form = ""
      next = False
      for index, (element, coef) in enumerate(zip(self.__compound_elements, self.__empirical_coef)):
         if next == False:
            if index != len([a for a in zip(self.__compound_elements, self.__empirical_coef)]) - 1:
               if int(self.__empirical_coef[index] == self.__empirical_coef[index + 1]) \
                     and int(self.__empirical_coef[index]) != 1:
                  form += "(" + str(element.__repr__()) \
                           + str(self.__compound_elements[index + 1].__repr__()) \
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
         else:
            pass

      return form

   def determine_molecular(self, mol_mass, molecular = False):
      '''
      Returns the molecular formula of the element, if the molar mass is provided.
      '''
      form = ""
      if molecular == True:
         d = round(operator.truediv(mol_mass, self.__empirical_mass), 1)
         if not d.is_integer():
            raise ValueError("Enter a molar mass that is an integer multiple of the empirical mass.")
         for element in zip(self.__compound_elements, self.__empirical_coef):
            form += str(element[0].__repr__())
            if int(element[1] * d) != 1:
               form += str(int(element[1] * d))

      return form

class CarbonDioxide(Compound):
   '''
   An extension of the Compound class for Carbon Dioxide, to be used in the CombustionTrain class.
   '''
   def __init__(self, **kwargs):
      super().__init__(compound = "CO2", **kwargs)

class Water(Compound):
   '''
   An extension of the Compound class for Water, to be used in the CombustionTrain class/
   '''
   def __init__(self, **kwargs):
      super().__init__(compound = "H2O", **kwargs)

