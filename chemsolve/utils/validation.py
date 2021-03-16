#!/usr/bin/env python3
# -*- coding = utf-8 -*-
from chemsolve.element import Element
from chemsolve.compound import Compound
from chemsolve.utils.periodictable import PeriodicTable
from chemsolve.utils.errors import InvalidElementError

def is_valid_element(element):
   """Checks whether a provided object is a valid element."""
   # If the object is already an Element, return True.
   if isinstance(element, Element):
      return True

   # Otherwise, check whether it is in the periodic table.
   return element in [item for item in PeriodicTable()['Symbol']]


def maybe_elements(*elements):
   """Validation method to check whether provided arguments are
   either elements or strings which represent valid elements."""
   # Create a holder list for return purposes.
   converted_elements = []

   # Iterate over the provided elements.
   for element in elements:
      if isinstance(element, Element):
         # It is already an element object.
         converted_elements.append(element)
      elif isinstance(element, str):
         # Check whether it is a valid element.
         if is_valid_element(element):
            converted_elements.append(Element(element))
         else:
            raise InvalidElementError(element)
      else:
         raise InvalidElementError(
            element, property_type = "type")

   # Return the converted elements.
   return converted_elements
