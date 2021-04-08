#!/usr/bin/env python3
# -*- coding = utf-8 -*-
import unittest
import logging

from chemsolve import Element
from chemsolve import Compound, Water

class CompoundTest(unittest.TestCase):
   """Various assorted tests for the compound class."""
   def test_compound_initialization_properties(self):
      """Test that the compound initializes its properties correctly."""
      # Construct the compound.
      lead_nitrate = Compound("Pb(NO3)2")
      # Check that the properties are correct.
      self.assertAlmostEqual(lead_nitrate.mass, 331.2098, places = 2)
      self.assertEqual(lead_nitrate.compound_elements, {'Pb': 1, 'N': 2, 'O': 6})
      self.assertEqual(str(lead_nitrate), 'Pb(NO₃)₂')
      # Deprecated attribute.
      self.assertEqual(str(lead_nitrate.print_compound), 'Pb(NO3)2')

   def test_mole_gram_initialization(self):
      """Ensure that the mole/gram calculations on initialization are correct."""
      # Construct the compound.
      ammonium = Compound("NH4", moles = 1.50)
      # Check that the values are correct.
      self.assertEqual(ammonium.mole_amount, 1.5)
      self.assertAlmostEqual(ammonium.gram_amount, 27.0577, places = 3)
      # Update the compound and check that things are still correct.
      ammonium(grams = 4.50)
      self.assertAlmostEqual(ammonium.mole_amount, 0.2495, places = 3)
      self.assertEqual(ammonium.gram_amount, 4.5)

   def test_compound_amounts(self):
      """Test that the amounts of the compound are as expected."""
      # Construct the compound.
      water = Compound("H2O")
      # Check that the values are correct.
      self.assertEqual(water.moles_in_compound('H'), 2)
      self.assertEqual(water.moles_in_compound('O'), 1)
   
   def test_compound_from_formula_empirical(self):
      """Check that the empirical version of Compound.from_formula is working."""
      # Create the elements.
      carbon = Element("C", percent = 0.5714)
      hydrogen = Element("H", percent = 0.0616)
      nitrogen = Element("N", percent = 0.0952)
      oxygen = Element("O", percent = 0.2718)
      # Construct the compound.
      compound = Compound.from_formula(carbon, hydrogen, nitrogen, oxygen)
      # Check the compound properties.
      self.assertEqual(repr(compound), 'C14H18N2O5')
      self.assertEqual(str(compound), 'C₁₄H₁₈N₂O₅')
      self.assertAlmostEqual(compound.mass, 294.30312, places = 3)
      self.assertAlmostEqual(compound.percent_in_compound('O'), 0.2718, places = 2)
      self.assertEqual(compound.compound_elements, {'C': 14, 'H': 18, 'N': 2, 'O': 5})

   def test_compound_from_formula_molecular(self):
      """Check that the molecular version of Compound.from_formula is working."""
      # Create the elements.
      carbon = Element("C", percent = 0.7595)
      nitrogen = Element("N", percent = 0.1772)
      hydrogen = Element("H", percent = 0.0633)
      # Construct the compound.
      compound = Compound.from_formula(carbon, nitrogen, hydrogen, molecular = True, mass = 240)
      self.assertEqual(str(compound), 'C₁₅N₃H₁₅')
      self.assertEqual(str(compound.empirical), 'C₅NH₅')
      self.assertAlmostEqual(compound.mass, 240, places = -1)

   def test_special_compounds(self):
      """Test the special pre-built compounds."""
      # Construct the water compound.
      water = Water()
      self.assertEqual(repr(water), 'H2O')
      self.assertAlmostEqual(water.mass, 18.01, places = 1)

if __name__ == '__main__':
   unittest.main()
