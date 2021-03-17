#!/usr/bin/env python3
# -*- coding = utf-8 -*-
"""
This file contains a collection of unicode conversion constants.
"""

# Create a method to initialize subscript mappings.
def _create_subscript_mapping():
   """Convert unicode digit characters to subscripts."""
   # Create the normal and subscript digits list.
   normal_digits = [i for i in range(10)]
   subscript_digits = [chr(0x2080 + i) for i in range(10)]

   # Create a dict mapping the two.
   return dict(zip(normal_digits, subscript_digits))

# Initialize the subscript mapping.
SUBSCRIPT_CONVERSION = _create_subscript_mapping()

# Create a method to initialize superscript mappings.
def _create_superscript_mapping():
   """Convert unicode digit characters to superscripts."""
   # 2 & 3 have different unicode superscript translations, so
   # we need to manually create different cases for them.
   # Also, 1 needs to be manually added with a different case.
   two_and_three = [2, 3]
   all_other_normal_nums = [0, *[i for i in range(4, 10)]]

   # Create the unicode superscripts for each of them.
   unicode_superscripts = [
      chr(0x2070 + i) for i in all_other_normal_nums]
   unicode_superscripts.extend(
      [chr(0x00B0 + i) for i in two_and_three])
   unicode_superscripts.append(chr(0x00B9))

   # Sort the list.
   normal, unicode = zip(*sorted(zip(
      [*all_other_normal_nums, *two_and_three, 1],
      unicode_superscripts)))

   # Create a dict mapping the two.
   return dict(zip(normal, unicode))

# Initialize the superscript mapping.
SUPERSCRIPT_CONVERSION = _create_superscript_mapping()

# Create a method exclusively for mapping the plus/minus signs (charges).
def _create_symbol_mapping():
   """Convert unicode symbols to their superscript format."""
   normal_items = ["+", "-"]
   unicode_items = [chr(0x2070 + i) for i in range(10, 12)]

   # Create a dict mapping the two.
   return dict(zip(normal_items, unicode_items))

# Initialize the symbol mapping.
SYMBOL_CONVERSION = _create_symbol_mapping()
