#!/usr/bin/env python3
# -*- coding = utf-8 -*-
import math

def ph(concentration):
   """Returns the pH from the hydronium ion concentration."""
   return -math.log(concentration)

def ph_from_hydroxide(concentration):
   """Returns the pH from the hydroxide ion concentration."""
   return 14 + math.log(concentration)

def poh(concentration):
   """Returns the pOH from the hydroxide ion concentration."""
   return -math.log(concentration)

def poh_from_hydronium(concentration):
   """Returns the pOH from the hydronium ion concentration."""
   return 14 + math.log(concentration)
