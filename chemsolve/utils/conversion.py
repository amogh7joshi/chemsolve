import os
import operator

import numpy as np

# Contains unit conversion formulas.

def to_atm(value, initial_unit = "mm Hg"):
   '''
   Convert pressure units to standard atmospheres.
   Mainly used to simplify ideal gas calculations in the gas module.
   '''
   initial_unit = initial_unit.replace(" ", "").lower()
   if initial_unit.replace(" ", "").lower() not in ["atm", "mmhg", "torr", "pa", "kpa", "psi", "bar"]:
      raise ValueError("That is not a valid unit of pressure.")
   if initial_unit == "pa":
      return operator.__truediv__(value, 101325)
   if initial_unit == "kpa":
      return operator.__truediv__(value, 101.325)
   if initial_unit == "bar":
      return operator.__truediv__(value, 1.01325)
   if initial_unit == "mmhg" or initial_unit == "torr":
      return operator.__truediv__(value, 760)
   if initial_unit == "psi":
      return operator.__truediv__(value, 14.69595)


