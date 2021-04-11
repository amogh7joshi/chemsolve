#!/usr/bin/env python3
# -*- coding = utf-8 -*-
from chemsolve.utils._unicode_constants import SUBSCRIPT_CONVERSION

def convert_string_no_charge(formula):
   """Converts a chemical formula (that doesn't contain
   a charge) to a displayable format."""
   return ''.join([SUBSCRIPT_CONVERSION[o] for o in formula])
