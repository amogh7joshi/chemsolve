#!/usr/bin/env python3
# -*- coding = utf-8 -*-
from chemsolve.element import Element

class ChemsolveError(Exception):
   """Base class for all Chemsolve errors."""
   pass

class InvalidElementError(ChemsolveError, ValueError):
   """Primarily invalid element error.

   Raised when an invalid element or element property is received.
   """
   def __init__(self, element_or_property, property_type = None):
      # Determine whether an element or property was passed.
      self.element_or_property = element_or_property
      self.property_type = property_type

   def __str__(self):
      # Format the output as necessary.
      raised_str = "Received an invalid "
      if self.property_type == "type":
         raised_str += "object of type {0}, expected an element.".format(
            type(self.element_or_property))
      elif isinstance(self.element_or_property, Element):
         raised_str += "element name: {0}.".format(self.element_or_property)
      else:
         raised_str += "element property for {0}: {1}.".format(
            self.element_or_property, self.property_type)
      return raised_str

   def __reduce__(self):
      return self.__class__, self.element_or_property, self.property_type
