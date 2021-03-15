#!/usr/bin/env python3
# -*- coding = utf-8 -*-
from __future__ import division

import operator

from chemsolve.utils.periodictable import PeriodicTable
from chemsolve.utils.warnings import ChemsolveDeprecationWarning
from chemsolve.utils.constants import *

__all__ = ['Element', 'SpecialElement']

class Element(object):
   """The core element object class.

   This class contains a single element and its attributes are all
   different properties of the element, including the simple ones like
   mass and atomic number, but also electron configuration (both full and
   noble gas abbreviation), atomic radius, electronegativity, ionization,
   and electron affinity. These can all be accessed as attributes.

   The element can be instantiated traditionally, from its symbol, but can
   also be created from molar mass or noble gas/complete electron configuration.

   Furthermore, with provided amounts of grams, moles, or molecules, the
   element class can automatically calculate the second and third unknown
   quantities, such as molecules and moles from grams.

   Examples
   --------
   Create a Barium element.

   >>> barium = Element('Ba')
   >>> # Access the element's attributes.
   >>> print(barium.mass)
   >>> print(barium.electronegativity)

   Create a Calcium element and calculate the number of moles.

   >>> calcium = Element('Ca', grams = 2.0)
   >>> # Get the number of molecules and moles.
   >>> print(calcium.mole_amount)
   >>> print(calcium.molecules)

   Parameters
   ----------
   element_symbol: str
      The element symbol representing the element you want to initialize.
   """
   def __init__(self, element_symbol, **kwargs):
      # Initialize class properties from PeriodicTable object.
      self._properties = PeriodicTable().get_properties(element_symbol)

      # Element Symbol/Name.
      self.element_symbol = element_symbol
      self.element_name = self.get_element_name()

      # Atomic Mass and Number.
      self.mass = self._properties['AtomicMass']
      self.number = self._properties['AtomicNumber']

      # Electron Configurations.
      self.electron_configuration = self._properties['ElectronConfiguration']
      self.full_electron_configuration = self._get_full_electron_configuration()

      # Miscellaneous Properties.
      self.radius = self._properties['AtomicRadius']
      self.electronegativity = self._properties['Electronegativity']
      self.ionization = self._properties['IonizationEnergy']
      self.electron_affinity = self._properties['ElectronAffinity']

      # Class Value Calculations.
      if "moles" in kwargs:
         self.mole_amount = kwargs["moles"]
         self.gram_amount = round(
            operator.mul(self.mole_amount, self.mass), 4)
         self.molecules = round(
            operator.mul(self.mole_amount, AVOGADRO), 4)

      if "grams" in kwargs:
         self.gram_amount = kwargs["grams"]
         self.mole_amount = round(
            operator.__truediv__(self.gram_amount, self.mass), 4)
         self.molecules = round(
            operator.mul(self.mole_amount, AVOGADRO), 4)

      if "molecules" in kwargs:
         self.molecules = kwargs["molecules"]
         self.mole_amount = round(
            operator.__truediv__(self.molecules, AVOGADRO), 4)
         self.gram_amount = round(
            operator.mul(self.mass, self.mole_amount))

      if "percent" in kwargs: # Primarily if you are setting up elements for Compound.from_formula.
         if float(kwargs["percent"]) >= 1:
            raise TypeError("That is not a valid input for the percent field. Enter a percent as a decimal.")
         self.percent_of = kwargs["percent"]
         self.mole_amount = False
         self.gram_amount = False

      if all(x in ["moles", "grams", "kwargs"] for x in [kwargs]):
         raise Exception("You cannot provide multiple different quantities "
                         "of the element at a single time.")

   def __str__(self):
      # For __str__, return the entire name of the element.
      return str(self.element_name.title())

   def __repr__(self):
      # For __repr__, we only need the element symbol, since that will be the
      # only thing used in internal methods (the intention of __repr__).
      return str(self.element_symbol.title())

   def __call__(self, **kwargs):
      # Update the class calculation quantities for more calculations.
      if "moles" in kwargs:
         self.mole_amount = kwargs["moles"]
         self.gram_amount = round(
            operator.mul(self.mole_amount, self.mass), 4)
         self.molecules = round(
            operator.mul(self.mole_amount, AVOGADRO), 4)

      if "grams" in kwargs:
         self.gram_amount = kwargs["grams"]
         self.mole_amount = round(
            operator.__truediv__(self.gram_amount, self.mass), 4)
         self.molecules = round(
            operator.mul(self.mole_amount, AVOGADRO), 4)

      if "molecules" in kwargs:
         self.molecules = kwargs["molecules"]
         self.mole_amount = round(
            operator.__truediv__(self.molecules, AVOGADRO), 4)
         self.gram_amount = round(
            operator.mul(self.mass, self.mole_amount))

      if "percent" in kwargs:
         # Primarily if you are setting up elements for Compound.from_formula.
         if float(kwargs["percent"]) >= 1:
            raise TypeError("That is not a valid input for the percent "
                            "field. Enter a decimal percent value.")
         self.percent_of = kwargs["percent"]
         self.mole_amount = False
         self.gram_amount = False

      if all(x in ["moles", "grams", "kwargs"] for x in [kwargs]):
         raise ValueError("You cannot provide multiple quantities "
                          "of the element at a single time.")

   @classmethod
   def from_molar_mass(cls, mass):
      """Instantiates an element from a provided molar mass.

      Given a certain molar mass value, this method checks to see whether there
      is an existing element with a defined molar mass value within 0.05 of the
      provided molar mass value, and instantiates the class from that.

      Examples
      --------
      Create a Boron atom from within 0.02 of its actual molar mass.

      >>> boron = Element.from_molar_mass(10.8)

      Parameters
      ----------
      mass: float
         The molar mass of the element which you want to create.

      Returns
      -------
      An instantiated Element class from the molar mass value.
      """
      table = PeriodicTable()

      for indx, molar_mass in enumerate(table['AtomicMass']):
         if abs(mass - molar_mass) <= 0.05:
            # If the molar mass provided is close to the actual one.
            return cls(table['Symbol'][indx])
      raise ValueError(f"Received invalid molar mass {mass}, not "
                       f"close to any molar masses on the periodic table.")

   @classmethod
   def from_electron_configuration(cls, config):
      """Instantiates an element from a provided electron configuration.

      Given an electron configuration, either the complete one or the noble
      gas abbreviation, this method gets the element associated with that
      electron configuration and instantiates the Element class from it.

      Examples
      --------
      Create a Magnesium atom from its noble gas electron configuration.

      >>> magnesium = Element.from_electron_configuration('[Ne]3s2')

      Parameters
      ---------
      config: str
         The complete or noble gas abbreviated electron configuration.

      Returns
      -------
      An instantiated Element class from the electron configruation.
      """
      table = PeriodicTable()

      for indx, configuration in enumerate(table['ElectronConfiguration']):
         if config == configuration:
            return cls(table['Symbol'][indx])
      for indx, element in enumerate(table['Symbol']):
         if config == Element(table['Symbol'][indx]).full_electron_configuration:
            return cls(table['Symbol'][indx])
      raise ValueError(f"Received invalid electron configuration {config}, not a valid noble gas "
                       f"configuration or complete configuration on the periodic table.")

   def get_element_name(self):
      """Returns the element name from the symbol."""
      try:
         return self._properties['Name']
      except AttributeError as ae:
         if ("+" or "-") in self.element_symbol:
            raise AttributeError("That is not an existing element in the periodic table.")
         else:
            raise ae

   def _get_full_electron_configuration(self):
      """Returns the entire electron configuration of the element."""
      config = ""
      if self.electron_configuration[0] == "[":
         config = Element(self.electron_configuration[1:3]).full_electron_configuration + " "
         config += self.electron_configuration[4:]
         return config
      else:
         return self.electron_configuration

   @ChemsolveDeprecationWarning('Element.calculate_moles', future_version = '2.0.0')
   def calculate_moles(self):
      """Calculates the class mole quantity from grams."""
      return round(operator.__truediv__(self.gram_amount, self.mass), 3)

   @ChemsolveDeprecationWarning('Element.calculate_grams', future_version = '2.0.0')
   def calculate_grams(self):
      """Calculates the class gram quantity from moles."""
      return operator.mul(self.mole_amount, self.mass)

@ChemsolveDeprecationWarning('SpecialElement', future_version = '2.0.0')
class SpecialElement(Element):
   """
   A special variant of the Element class created for the FormulaCompound class.

   Contains the extra parameter of percentage, in order to use percentages to find the formula of the compound.
   If percentage is defined, the percentage parameter overrides the gram and mole parameters in the FormulaCompound class.
   If grams is defined, the grams parameter overrides the mole and percent parameter. Ideally, moles shouldn't be used in the first place.
   If percentage is defined in one SpecialElement, it must be defined in all other elements. Same goes for grams.

   **Should only be used for the FormulaCompound class. If simply defining an element, use the Element class.
   """
   def __init__(self, element_symbol, **kwargs):
      super().__init__(element_symbol = element_symbol, **kwargs)

      if len(kwargs) == 0:
         raise ValueError("If you are not looking to define any values, you should use the Element class instead.")
      if "grams" not in kwargs and "percent" not in kwargs and "moles" not in kwargs:
         raise ValueError("If you are not looking to define any numerical values, you should use the Element class instead.")

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


