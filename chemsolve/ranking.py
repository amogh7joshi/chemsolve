#!/usr/bin/env python3
# -*- coding = utf-8 -*-
from chemsolve.element import Element
from chemsolve.utils.validation import maybe_elements
from chemsolve.utils.errors import InvalidElementError

def rank_electronegativity(*elements):
   """Ranks provided elements by their electronegativity.

   Examples
   --------
   >>> print(rank_electronegativity(
   ...   Element("Ca"), Element("K"), Element("Br"), Element("O"))))

   Parameters
   ----------
   elements: chemsolve.Element
      A list of `chemsolve.Element` objects.

   Returns
   -------
   The elements ranked from least to greatest electronegativity.
   """
   # First, validate the provided elements.
   elements = maybe_elements(*elements)

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

   Examples
   --------
   >>> print(rank_atomic_radius(
   ...   Element("Ca"), Element("K"), Element("Br"), Element("O"))))

   Parameters
   ----------
   elements: chemsolve.Element
      A list of `chemsolve.Element` objects.

   Returns
   -------
   The elements ranked from least to greatest atomic radius.
   """
   # First, validate the provided elements.
   elements = maybe_elements(*elements)

   # Then, get the atomic radii of each element.
   atomic_radii = []
   for element in elements:
      atomic_radii.append(element.electronegativity)

   # Sort the atomic radii.
   _, sorted_elements = zip(*sorted(zip(atomic_radii, elements)))

   # Return the sorted list.
   return sorted_elements

def rank_first_ionization_energy(*elements):
   """Ranks provided elements by their first ionization energy.

   Examples
   --------
   >>> print(rank_first_ionization_energy(
   ...   Element("Ca"), Element("K"), Element("Br"), Element("O")))

   Parameters
   ----------
   elements: chemsolve.Element or str
      A list of `chemsolve.Element` objects.

   Returns
   -------
   The elements ranked from least to greatest first ionization energy.
   """
   # First, validate the provided elements.
   elements = maybe_elements(*elements)

   # Then, get the first ionization energy of each element.
   ionization_energies = []
   for element in elements:
      ionization_energies.append(element.ionization)

   # Sort the atomic radii.
   _, sorted_elements = zip(*sorted(zip(ionization_energies, elements)))

   # Return the sorted list.
   return sorted_elements

def rank_electron_affinity(*elements):
   """Ranks provided elements by their electron_affinity.

   Examples
   --------
   >>> print(rank_electron_affinity(
   ...   Element("Ca"), Element("K"), Element("Br"), Element("O")))

   Parameters
   ----------
   elements: chemsolve.Element
      A list of `chemsolve.Element` objects.

   Returns
   -------
   The elements ranked from least to greatest electron affinity.
   """
   # First, validate the provided elements.
   elements = maybe_elements(*elements)

   # Then, get the first ionization energy of each element.
   electron_affinities = []
   for element in elements:
      electron_affinities.append(element.electron_affinity)

   # Sort the atomic radii.
   _, sorted_elements = zip(*sorted(zip(electron_affinities, elements)))

   # Return the sorted list.
   return sorted_elements
