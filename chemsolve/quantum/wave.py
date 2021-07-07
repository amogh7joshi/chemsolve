#!/usr/bin/env python3
# -*- coding = utf-8 -*-
from chemsolve.utils.validation import resolve_float_or_constant
from chemsolve.utils.validation import check_empty_values
from chemsolve.utils.constants import *

class Wave(object):
   """Represents a wave object, with frequency/wavelength.

   Examples
   --------
   Calculate the frequency of an electromagnetic wave
   given its wavelength and speed.

   >>> wave = Wave(wavelength = 2e8, speed = 1)

   Parameters
   ----------
   frequency: int or float or str
      - The frequency of the wave, either a float or string.
   wavelength: int or float or str
      - The wavelength of the wave, either a float or string.
   speed: int or float or str
      - The speed of the wave, either a float or string.
   """
   @check_empty_values('frequency', 'wavelength', 'speed', allow = 2)
   def __init__(self, frequency = None, wavelength = None, speed = None):
      # Resolve the input parameters.
      self._frequency = resolve_float_or_constant(frequency)
      self._wavelength = resolve_float_or_constant(wavelength)
      self._speed = resolve_float_or_constant(speed)

      # Set any other attributes which will be calculated.
      self._energy = None

      # Calculate all of the class quantities.
      self._calculate_quantities()

   def _calculate_quantities(self):
      """Calculates quantities pertinent to the wave."""
      if self._frequency is None:
         self._frequency = self._speed / self._wavelength
      elif self._speed is None:
         self._speed = self._frequency * self._wavelength
      elif self._wavelength is None:
         self._wavelength = self._speed / self._frequency
      self._energy = h * self._speed / self._wavelength

   @property
   def frequency(self):
      return self._frequency

   @property
   def speed(self):
      return self._speed

   @property
   def wavelength(self):
      return self._wavelength

   @property
   def energy(self):
      return self._energy





