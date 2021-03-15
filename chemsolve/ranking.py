#!/usr/bin/env python3
# -*- coding = utf-8 -*-
from chemsolve.element import Element
from chemsolve.utils.errors import InvalidElementError

def rank_electronegativity(*elements):
   """Ranks provided elements by their electronegativity.

   Parameters
   ----------
   elements: chemsolve.Element
      A list of `chemsolve.Element` objects.

   Returns
   -------
   The elements ranked from least to greatest electronegativity.
   """
   # First, validate the provided elements.
   for element in elements:
      if not isinstance(element, Element):
         raise InvalidElementError(element, property_type = "type")

   # Then, get the electronegativities of each element.
   electronegativities = []
   for element in elements:
      electronegativities.append(element.electronegativity)

   # Sort the electronegativities.
   _, sorted_elements = zip(*sorted(zip(electronegativities, elements)))

   # Return the sorted list.
   return sorted_elements

def rank_atomic_radius(*elements):
   """Ranks provided elements by their atomic radii.

   Parameters
   ----------
   elements: chemsolve.Element
      A list of `chemsolve.Element` objects.

   Returns
   -------
   The elements ranked from least to greatest atomic radius.
   """
   # First, validate the provided elements.
   for element in elements:
      if not isinstance(element, Element):
         raise InvalidElementError(element, property_type = "type")

   # Then, get the atomic radii of each element.
   atomic_radii = []
   for element in elements:
      atomic_radii.append(element.electronegativity)

   # Sort the atomic radii.
   _, sorted_elements = zip(*sorted(zip(atomic_radii, elements)))

   # Return the sorted list.
   return sorted_elements

