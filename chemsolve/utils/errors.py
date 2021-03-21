#!/usr/bin/env python3
# -*- coding = utf-8 -*-

class ChemsolveError(Exception):
   """Base class for all Chemsolve errors."""
   pass


class InvalidChemistryArgumentError(ChemsolveError, ValueError):
   """Base class for all invalid argument errors."""
   def __init__(self, object_or_property,
                property_type = None, chemical_type = None):
      # Determine whether an object or property was passed.
      self.object_or_property = object_or_property
      self.property_type = property_type

      # Set the chemical type for the displayed output.
      self.chemical_type = chemical_type
      self.plurals = "s" if self.chemical_type in ['Element'] else ""

   def __str__(self):
      # Format the output as necessary.
      raised_str = "Received an invalid "
      if self.property_type == "type":
         raised_str += "object of type {0}, expected a{1} {2}.".format(
            type(self.object_or_property), self.plurals, self.chemical_type)
      elif self.property_type == "bypass":
         raised_str = self.object_or_property
      elif self.property_type is None:
         raised_str += "{0} name: {1}.".format(
            self.chemical_type, self.object_or_property)
      else:
         raised_str += "{0} property for {1}: {2}.".format(
            self.chemical_type, self.object_or_property, self.property_type)
      return raised_str

   def __reduce__(self):
      return self.__class__, self.object_or_property, self.property_type


class InvalidElementError(InvalidChemistryArgumentError, ValueError):
   """Primary invalid element error.

   Raised when an invalid element or element property is received.
   """
   def __init__(self, object_or_property, property_type = None):
      super(InvalidElementError, self).__init__(
         object_or_property, property_type, "element")


class InvalidCompoundError(InvalidChemistryArgumentError):
   """Primary invalid compound error.

   Raised when an invalid compound or compound property is received.
   """
   def __init__(self, object_or_property, property_type = None):
      super(InvalidCompoundError, self).__init__(
         object_or_property, property_type, "compound")


class InvalidReactionError(InvalidChemistryArgumentError):
   """Primary invalid reaction error.

   Raised when an invalid reaction or reaction property is received.
   """
   def __init__(self, object_or_property, property_type = None):
      super(InvalidReactionError, self).__init__(
         object_or_property, property_type, "reaction")

