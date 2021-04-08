#!/usr/bin/env python3
# -*- coding = utf-8 -*-
import unittest

from chemsolve import Element

class ElementTest(unittest.TestCase):
   """Various assorted tests for the element class."""
   def test_element_initialization_properties(self):
      """Test that the element initializes its properties correctly."""
      # Construct the element.
      oxygen = Element("O")
      # Check that the properties are correct.
      self.assertAlmostEqual(oxygen.mass, 15.999, places = 2)
      self.assertEqual(oxygen.number, 8)
      self.assertEqual(oxygen.element_name, 'Oxygen')
      self.assertEqual(oxygen.element_symbol, 'O')

   def test_mole_gram_initialization(self):
      """Ensure that the mole/gram calculations on initialization are correct."""
      # Construct the element.
      boron = Element('B', moles = 2.50)
      # Ensure that the calculated values are correct.
      self.assertEqual(boron.mole_amount, 2.5)
      self.assertAlmostEqual(boron.gram_amount, 27.025, places = 2)
      # Update the parameters.
      boron(grams = 30.00)
      # Ensure that the calculated values are correct.
      self.assertAlmostEqual(boron.mole_amount, 2.7752, places = 2)
      self.assertEqual(boron.gram_amount, 30.0)

   def test_electron_configuration(self):
      """Test the initialization of an Element from its electron configuration."""
      # Construct the element.
      magnesium = Element.from_electron_configuration('[Ne]3s2')
      # Ensure that it is correct.
      self.assertEqual(str(magnesium), "Magnesium")

