import operator

from chemsolve.utils.conversion import to_atm, to_kelvin
from chemsolve.utils.string_op import num_in
from chemsolve.utils.constants import *

class Gas(object):
   def __init__(self, P: float = None, V: float = None, n: float = None, T: float = None, **kwargs):
      if not num_in(3, [P, V, n, T]):
         raise ValueError("You need to define three of the attributes of the gas.")
      else:
         for attr in [P, V, n, T]:
            if attr:
               m = list(k for k, v in locals().items() if v is attr and k != "attr")[0]
               setattr(self, m, attr)
            else:
               m = list(k for k, v in locals().items() if v is None and k != "attr")[0]
               setattr(self, "unknown", m)
               setattr(self, m, None)

      if kwargs: self._parse_kwargs(kwargs)
      if not self.conv_P: self.conv_P = self.P
      if not self.conv_T: self.conv_T = self.T

   def _parse_kwargs(self, kwargs):
      for item, value in kwargs:
         if item.lower() not in ["p_units", "t_units"]:
            raise ValueError("That is not a valid keyword argument. The valid keyword arguments are pressure units (P_units) and temperature units (T_units).")
         else:
            if item == "p_units":
               if item.replace(" ", "").lower() not in PRESSURE_UNITS:
                  raise ValueError("That is not a valid pressure unit.")
               else: self.conv_P = to_atm(self.P, value)
            elif item == "t_units":
               if item.replace(" ", "").lower() not in TEMP_UNITS:
                  raise ValueError("That is not a valid temperature unit.")
               else: self.conv_T = to_kelvin(self.T, value)

   def solve(self):
      '''
      Solve the ideal gas equation for the unknown value.
      '''
      left, right = None, None
      if self.P and self.V:
         left = self.conv_P * self.V
      elif self.n and self.T:
         right = self.n * Ratm * self.T

      if right:
         if self.unknown == "P": return operator.__truediv__(right, self.V)
         if self.unknown == "V": return operator.__truediv__(right, self.conv_P)
      if left:
         if self.unknown == "n": return operator.__truediv__(left, operator.__mul__(Ratm, self.conv_T))
         if self.unknown == "T": return operator.__truediv__(left, operator.__mul__(Ratm, self.n))


