import operator

from chemsolve.utils.periodictable import PeriodicTable
from chemsolve.utils.constants import *

__all__ = ['Element', 'SpecialElement']

class Element(object):
   '''
   A class which contains an element.

   Has little functions of its own aside from elemental attributes such as number, mass, and the ion it forms.
   A framework for extended element classes.
   '''
   def __init__(self, element_symbol, **kwargs):
      self.__properties = PeriodicTable().get_properties(element_symbol)
      self.element_symbol = element_symbol
      self.element_name = self.get_element_name()
      self.mass = self.__properties['AtomicMass']
      self.number = self.__properties['AtomicNumber']
      self.electron_configuration = self.__properties['ElectronConfiguration']
      self.full_electron_configuration = self.get_full_electron_configuration()
      self.radius = self.__properties['AtomicRadius']
      self.electronegativity = self.__properties['Electronegativity']
      self.ionization = self.__properties['IonizationEnergy']
      self.electron_affinity = self.__properties['ElectronAffinity']

      '''
      The class can calculate quantities of moles and grams, depending on the specific keywords 'moles' and 'grams'.
      '''
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

      if all(x in ["moles", "grams", "kwargs"] for x in [kwargs]):
         raise Exception("You cannot provide multiple quantities of the element at a single time.")

   def __str__(self):
      return str(self.element_name.title())

   def __repr__(self):
      return str(self.element_symbol.title())

   def __getattr__(self, item):
      if item == "percent_of":
         raise AttributeError("If you want to use percentages, you must use the SpecialElement class.")

   def __call__(self, **kwargs):
      if "moles" in kwargs:
         self.mole_amount = kwargs["moles"]
         self.gram_amount = round(operator.mul(self.mole_amount, self.mass), 4)
         self.molecules = round(operator.mul(self.mole_amount, AVOGADRO), 4)

      if "grams" in kwargs:
         self.gram_amount = kwargs["grams"]
         self.mole_amount = round(operator.__truediv__(self.gram_amount, self.mass), 4)
         self.molecules = round(operator.mul(self.mole_amount, AVOGADRO), 4)

      if "molecules" in kwargs:
         self.molecules = kwargs["molecules"]
         self.mole_amount = round(operator.__truediv__(self.molecules, AVOGADRO), 4)
         self.gram_amount = round(operator.mul(self.mass, self.mole_amount))

      if all(x in ["moles", "grams", "kwargs"] for x in [kwargs]):
         raise ValueError("You cannot provide multiple quantities of the element at a single time.")

   '''
   Functions which gather attributes.
   '''
   def get_element_name(self):
      '''
      Returns the element name from the symbol.
      '''
      try:
         return self.__properties['Name']
      except AttributeError:
         if ("+" or "-") in self.element_symbol:
            print("That is not an existing element in the periodic table.")

   def get_full_electron_configuration(self):
      '''
      Returns the entire electron configuration of the element, ignoring the noble gas abbreviation.
      '''
      config = ""
      if self.electron_configuration[0] == "[":
         config = Element(self.electron_configuration[1:3]).full_electron_configuration + " "
         config += self.electron_configuration[4:]
         return config
      else: return self.electron_configuration

   '''
   Functions which perform calculations.
   '''
   def calculate_moles(self):
      return round(operator.truediv(self.gram_amount, self.mass), 3)

   def calculate_grams(self):
      return operator.mul(self.mole_amount, self.mass)


class SpecialElement(Element):
   '''
   A special variant of the Element class created for the FormulaCompound class.

   Contains the extra parameter of percentage, in order to use percentages to find the formula of the compound.
   If percentage is defined, the percentage parameter overrides the gram and mole parameters in the FormulaCompound class.
   If grams is defined, the grams parameter overrides the mole and percent parameter. Ideally, moles shouldn't be used in the first place.
   If percentage is defined in one SpecialElement, it must be defined in all other elements. Same goes for grams.

   **Should only be used for the FormulaCompound class. If simply defining an element, use the Element class.
   '''
   def __init__(self, element_symbol, **kwargs):
      super().__init__(element_symbol = element_symbol, **kwargs)

      if len(kwargs) == 0:
         raise Warning("If you are not looking to define any values, you should use the Element class instead.")
      if "grams" not in kwargs and "percent" not in kwargs and "moles" not in kwargs:
         raise Warning("If you are not looking to define any numerical values, you should use the Element class instead.")

      if "grams" in kwargs:
         self.gram_amount = kwargs["grams"]; self.mole_amount = False; self.percent_of = False
      else: self.gram_amount = False
      if "percent" in kwargs:
         if float(kwargs["percent"]) >= 1:
            raise TypeError("That is not a valid input for the percent field. Enter a percent as a decimal.")
         self.percent_of = kwargs["percent"]; self.mole_amount = False; self.gram_amount = False
      else: self.percent_of = False
      if "moles" in kwargs:
         self.mole_amount = kwargs["moles"]; self.gram_amount = False; self.percent_of = False


