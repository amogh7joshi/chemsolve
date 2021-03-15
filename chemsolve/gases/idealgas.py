#!/usr/bin/env python3
# -*- coding = utf-8 -*-
import operator

from chemsolve.utils.conversion import to_atm, to_kelvin
from chemsolve.utils.string_op import num_in
from chemsolve.utils.constants import *

class Gas(object):
   """A class representing an ideal gas.

   This class is used to solve the ideal gas equation, PV = nRT,
   given three of the different values (which is necessary to solve it).

   The units of P/T (default atm/Kelvin) can be any of the valid units for
   ideal gases, e.g. atm, Pa, kPa, mm Hg, or C, F, K, etc. These should be
   passed as keyword arguments and the equation will adjust as necessary.

   Examples
   --------
   Solving the ideal gas equation for moles:

   >>> Gas(P = 2.0, V = 4.0, T = 200).solve()

   Solving the ideal gas equation for pressure (with temperature in Celsius):

   >>> Gas(V = 2.0, T = 0, n = 4, t_units = "c").solve()

   Parameters
   ----------
   P: float
      The value for pressure.
   V: float
      The value for volume.
   n: float
      The value for moles.
   T: float
      The value for temperature.
   """
   def __init__(self, P: float = None, V: float = None,
                n: float = None, T: float = None, **kwargs):
      # Ensure that enough arguments have been passed.
      if not num_in(3, [P, V, n, T]):
         raise ValueError("You need to define three of the attributes of the gas.")
      else:
         # Otherwise, set the pre-determined class values to the class.
         for attr in [P, V, n, T]:
            if attr:
               # If the attribute is pre-determined.
               m = list(k for k, v in locals().items() if v is attr and k != "attr")[0]
               setattr(self, m, attr)
            else:
               # If the attribute is the unknown.
               m = list(k for k, v in locals().items() if v is None and k != "attr")[0]
               setattr(self, "unknown", m)
               setattr(self, m, None)

      # Parse keyword arguments and set relevant conversions.
      if kwargs:
         self._parse_kwargs(kwargs)
      if not self.conv_P: # Pressure unit conversions.
         self.conv_P = self.P
      if not self.conv_T: # Temperature unit conversions.
         self.conv_T = self.T

   def _parse_kwargs(self, kwargs):
      """Internal method to parse the class keyword arguments."""
      for item, value in kwargs:
         # Validate the passed keyword arguments.
         if item.lower() not in ["p_units", "t_units"]:
            raise ValueError("That is not a valid keyword argument. The valid "
                             "keyword arguments are pressure units (P_units) "
                             "and temperature units (T_units).")
         else:
            if item == "p_units": # Set class values for pressure units.
               if item.replace(" ", "").lower() not in PRESSURE_UNITS:
                  raise ValueError("That is not a valid pressure unit.")
               else:
                  self.conv_P = to_atm(self.P, value)
            elif item == "t_units": # Set class values for temperature units.
               if item.replace(" ", "").lower() not in TEMP_UNITS:
                  raise ValueError("That is not a valid temperature unit.")
               else:
                  self.conv_T = to_kelvin(self.T, value)

   def solve(self):
      """Solves the ideal gas equation for the unknown value.

      Returns
      -------
      The value (with the default units) for the corresponding unknown.
      """
      left, right = None, None
      # Solve for the side without any unknowns first.
      if self.P and self.V:
         left = self.conv_P * self.V
      elif self.n and self.T:
         right = self.n * Ratm * self.T

      if right: # Then, solve for the single unknown on the left side.
         if self.unknown == "P": # Pressure calculations.
            setattr(self, 'P', operator.__truediv__(right, self.V))
            return self.P
         if self.unknown == "V": # Volume calculations.
            setattr(self, 'V', operator.__truediv__(right, self.conv_P))
            return self.V
      if left: # Otherwise, solve for the single unknown on the right side.
         if self.unknown == "n": # Moles calculations.
            setattr(self, 'n', operator.__truediv__(left, operator.__mul__(Ratm, self.conv_T)))
            return self.n
         if self.unknown == "T": # Temperature calculations.
            setattr(self, 'T', operator.__truediv__(left, operator.__mul__(Ratm, self.n)))
            return self.T


