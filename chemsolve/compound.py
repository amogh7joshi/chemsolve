#!/usr/bin/env python3
# -*- coding = utf-8 -*-
import re
import sys
import math
import operator
import pyparsing

import periodictable as pt
from chempy import Substance

from chemsolve.element import Element
from chemsolve.element import SpecialElement
from chemsolve.utils.from_formula import determine_empirical_coef
from chemsolve.utils.from_formula import determine_empirical, determine_molecular
from chemsolve.utils.constants import *
from chemsolve.utils.warnings import ChemsolveDeprecationWarning
from chemsolve.utils.errors import InvalidCompoundError

__all__ = ['Compound', 'FormulaCompound', 'CarbonDioxide', 'Water']

# Since the `chemsolve.utils.string_op` file contains an import
# of this actual `chemsolve.compound` file, we cannot directly
# import the method from there due to circular imports. Instead,
# the function is redefined here to enable its usage in this module.
def split(string): return [char for char in string]

class Compound(object):
   """The core compound object class.

   This class contains a single compound, with its attributes being
   different properties of the compound, including the simple ones like
   mass and formula but also the more complex ones like dictionaries of
   each of the elements which are part of the compound. Furthermore, the
   class can calculate various values such as the number of moles or the
   percentage of a certain element in the compound.

   The compound should be instantiated traditionally, from its formula,
   but it can also be created from its name (at least for the majority of
   the main understandable compounds) if necessary.

   Furthermore, with provided amounts of grams, moles, or molecules, the
   compound class can automatically calculate the second and third unknown
   quantities, such as molecules and moles from grams.
   
   Methods
   ----------
   `Compound.from_formula`:
      A special method that allows the instantiation of the Compound class
      from quantities of the elements which are part of it, and allows
      for either the traditional empirical formula calculates or the 
      providing of a molecular mass to calculate the molecular formula.
                        
   Examples
   --------
   Create a Ethane element.

   >>> ethane = Compound('C2H6')
   >>> # Access the element's attributes.
   >>> print(ethane.mass)
   >>> print(ethane.compound_elements)

   Create a Sodium Hydroxide element and calculate the number of moles.

   >>> naoh = Compound('NaOH', grams = 2.0)
   >>> # Get the number of molecules and moles.
   >>> print(naoh.mole_amount)
   >>> print(naoh.molecules)

   Parameters
   ----------
   compound: str
      The chemical formula of the compound that you want to use.
   """
   def __init__(self, compound, **kwargs):
      # The Compound class will either be instantiated as a regular
      # compound, or from the `Compound.from_formula` method, and 
      # may potentially have a keyword to calculate the molecular 
      # formula, so that needs to be searched for first.
      if 'mol_comp' in kwargs and compound is None:
         # Extract the option from the kwarg dictionary.
         mol_comp = kwargs['mol_comp']
         
         # Initialize the formula object for later parameter parsing.
         compound = mol_comp[0].replace("'", '')

         # Set the original empirical calculation as well as the new
         # molecular calculation to the class (for accessibility).
         self.compound = pt.formula(compound)
         self.empirical = mol_comp[1]
      else:
         try: # Check if a valid element has been passed.
            self.compound = pt.formula(compound)
         except pyparsing.ParseException:
            # Pass a chemistry-related error rather than a parsing error.
            raise InvalidCompoundError(compound)
         except Exception as e:
            # An unknown exception.
            raise e

      # Set the different class values.
      self.mass = self.get_mass()
      self.compound_elements_list = self._get_compound_ions(compound)
      self.compound_elements = {}
      self.compound.elements = self.get_elements_in_compound()
      self.print_compound = Substance.from_formula(compound) # Deprecated attribute.
      self.store_comp = compound

      if 'bypass' not in kwargs:
         # If a subclass is initialized, then don't set default values.
         self._parse_quantities(**kwargs)

   def __str__(self):
      # Return the unicode name of the compound (rendered correctly).
      return str(Substance.from_formula(str(self.compound)).unicode_name)

   def __repr__(self):
      # Return just the regular string representing the class compound.
      return str(self.compound)

   def __int__(self):
      # Return the mass of the compound as an integer.
      return int(self.mass)

   def __float__(self):
      # Return the mass of the compound as a float.
      return self.mass

   def __getattr__(self, item):
      if item not in ["mole_amount", "gram_amount", "volume"]:
         raise AttributeError("The attribute " + str(item) + " does not exist within this class.")

   def __getattribute__(self, item):
      # Check for deprecated methods and warn about their removal.
      if item == 'print_compound':
         ChemsolveDeprecationWarning('The attribute `Compound.print_compound` is deprecated and will '
                                     'be removed in v2.0.0. Use repr(Compound) instead.',
                                     future_version = 'bypass')
      return object.__getattribute__(self, item)

   def __contains__(self, item):
      # Determine whether a element is in the compound.
      if isinstance(item, Element):
         if item.element_symbol in self.compound_elements_list:
            return True
      elif isinstance(item, str):
         if item in self.compound_elements_list:
            return True
      return False

   def __call__(self, **kwargs):
      # Update the class quantities of moles, grams, or molecules.
      self._parse_quantities(**kwargs)

   def _parse_quantities(self, **kwargs):
      # Parse the keyword arguments of the class.
      if "moles" in kwargs:
         self.mole_amount = kwargs["moles"]
         self.gram_amount = round(operator.mul(self.mole_amount, self.mass), 4)
         self.molecules = round(operator.mul(self.mole_amount, AVOGADRO), 4)

      if "grams" in kwargs:
         self.gram_amount = kwargs["grams"]
         self.mole_amount = round(operator.truediv(self.gram_amount, self.mass), 4)
         self.molecules = round(operator.mul(self.mole_amount, AVOGADRO), 4)

      if "molecules" in kwargs:
         self.molecules = kwargs["molecules"]
         self.mole_amount = round(operator.__truediv__(self.molecules, AVOGADRO), 4)
         self.gram_amount = round(operator.mul(self.mass, self.mole_amount))

      if "volume" in kwargs or "molarity" in kwargs:
         raise AttributeError("If you want to use volume or molarity, then you need to use the SolutionCompound class.")

      if "moles" in kwargs and "grams" in kwargs:
         raise ValueError("You cannot provide both the number of moles and grams of the element at a single time.")
      if "grams" in kwargs and "volume" in kwargs:
         raise ValueError("You cannot provide both the volume and the gram value at the same time.")

      if "structure" in kwargs:
         if kwargs["structure"] in STRUCTURES:
            self.structure = kwargs["structure"]
         else:
            raise ValueError("That is not an appropriate compound structure.")

   @classmethod
   def fromFormula(cls, *args, molecular = False, **kwargs):
      """Creates a compound from provided percentages of different elements in the compound."""
      molar_mass = None
      compound_elements = []

      if len(args) < 2:
         raise ValueError("You may be using the wrong method, as fromFormula is used to determine compound formulas.")
      for element in args:
         if not isinstance(element, Element):
            raise TypeError("The arguments of this class should only be Element classes.")
         else:
            compound_elements.append(element)

      if "mass" in kwargs:
         molar_mass = kwargs["mass"]

      # Determine compound coefficients, and create compound from them.
      empirical_coef = determine_empirical_coef(compound_elements)
      empirical = Compound(determine_empirical(compound_elements, empirical_coef))
      empirical_mass = Compound(empirical.__repr__()).mass

      # Create primary Compound class.
      if molecular:
         molecular = determine_molecular(empirical_mass, compound_elements,
                                         empirical_coef, molar_mass, molecular=True)
         return cls(compound = None, mol_comp = [molecular.__repr__(), empirical], grams = molar_mass) # noqa
      else:
         return cls(compound = empirical.__repr__())

   @staticmethod
   def from_formula(*args, molecular = False, **kwargs):
      """A transitional method for v2.0.0, will eventually replace fromFormula."""
      return Compound.fromFormula(*args, molecular = molecular, **kwargs)

   def get_mass(self):
      '''
      Returns the atomic (and therefore molar) mass of the compound.
      '''
      return self.compound.mass # noqa

   @staticmethod
   def _get_compound_ions(compound):
      """Returns each of the individual polyatomic ions in
      the element (both element symbol and number)."""
      # Start by checking whether there is a parenthesis in the compound.
      if "(" in compound:
         # Ensure that there is an end parenthesis or else the parser will break.
         if ")" not in compound:
            raise TypeError("That is not a valid format for a compound.")

         # Parse all of the information inside of the actual parenthesis.
         left = compound.index("(")
         right = compound.index(")")
         charge = int(compound[right + 1])
         f = re.findall('[A-Z][^A-Z]*', compound[(left + 1):right])
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

         # Re-create the compound with the parenthesis information resolved.
         compound = compound[:left] + str(replacer)

      # Return the parsed compound.
      return re.findall('[A-Z][^A-Z]*', str(compound))

   def get_elements_in_compound(self):
      """Returns a dictionary containing the elements in the compound and the quantity of each element."""
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
      return self.compound_elements

   def moles_in_compound(self, element):
      """Returns the number of moles of a certain element
      inside of the compound.

      Finds the number of moles of a certain element per one mole of the
      compound, and returns that value.

      Examples
      --------
      Find the number of moles of hydrogen in water.

      >>> water = Compound('H2O')
      >>> print(water.moles_in_compound('H'))

      Parameters
      ----------
      element: str or Element
         The element that you want to find the quantity of.
      """
      try:
         return self.compound_elements[element]
      except KeyError:
         print("That is not an element in this compound.")
      except AttributeError:
         print("That is not an element.")

   def percent_in_compound(self, element):
      """Returns the percentage of a certain element inside of the compound.

      Finds the percentage of the compound's mass that is made up of
      a certain provided element and returns that value.

      Examples
      --------
      Find the quantity of hydrogen in water.

      >>> water = Compound('H2O')
      >>> print(water.percent_in_compound('H'))

      Parameters
      ----------
      element: str or Element
         The element that you want to find the quantity of.
      """
      try:
         return round((Element(str(element).title()).mass *
                       self.compound_elements[element]) / self.mass, 4)
      except KeyError:
         print("That is not an element in this compound.")
      except AttributeError:
         print("That is not an element.")


class SolutionCompound(Compound):
   """
   Used as an implementation of the compound class for compounds in solutions.

   Accepts either molarity and volume or mole quantity attributes, in addition to
   charge and state attributes in order to represent a complete solution compound.
   Charge defaults to None and state defaults to 'aq', must be manually set otherwise.
   """
   def __init__(self, compound, charge = None, state = "aq", **kwargs):
      super().__init__(compound, bypass = True)
      if charge: # Charge can also not be provided.
         if charge not in range(-5, 6):
            raise ValueError(f"The value for charge as initiated, {charge}, is too high or too low.")
         self.charge = charge
      if state not in ["aq", "s", "l", "g"]:
         raise ValueError("The state of the compound must be either aqueous, solid, liquid, or gaseous.")
      self.state = state

      if 'molarity' in kwargs and 'volume' in kwargs:
         self.molarity = kwargs['molarity']
         self.volume = kwargs['volume']
         self.mole_amount = operator.__mul__(self.molarity, self.volume)

      if 'molarity' in kwargs and 'moles' in kwargs:
         self.molarity = kwargs['molarity']
         self.mole_amount = kwargs['mole_amount']
         self.volume = operator.__truediv__(self.mole_amount, self.molarity)

      if 'moles' in kwargs and 'volume' in kwargs:
         self.mole_amount = kwargs['moles']
         self.volume = kwargs['volume']
         self.molarity = operator.__truediv__(self.mole_amount, self.volume)

   # def split_into_ions(self):
   #    """Splits instance compound into its relevant ions with respect to overall charge."""
   #    element = Element(2)._properties

@ChemsolveDeprecationWarning('FormulaCompound', future_version = "2.0.0")
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
         if not isinstance(element, Element):
            raise TypeError("The arguments of this class should only be Element classes.")
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
         if not math.isclose(t, math.floor(t), abs_tol = 10 ** -1) and not math.isclose(t, math.ceil(t), abs_tol= 10 ** -1):
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
               if not math.isclose(item, math.floor(item), abs_tol=10 ** -1) and not math.isclose(item, math.ceil(item), abs_tol=10 ** -1):
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
               if not math.isclose(t, math.floor(t), abs_tol=10 ** -1) and not math.isclose(t, math.ceil(t), abs_tol=10 ** -1):
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
   """
   An extension of the Compound class for Carbon Dioxide, to be used in the CombustionTrain class.
   """
   def __init__(self, **kwargs):
      super().__init__(compound = "CO2", **kwargs)
      self.geometry = "linear"

class Water(Compound):
   """
   An extension of the Compound class for Water, to be used in the CombustionTrain class/
   """
   def __init__(self, **kwargs):
      super().__init__(compound = "H2O", **kwargs)
      self.geometry = "bent"


