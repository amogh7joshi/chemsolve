#!/usr/bin/env python3
# -*- coding = utf-8 -*-
from __future__ import division

from chemsolve.utils.constants import *

def convert_pressure_units(value, input_unit = 'mm Hg', out_unit = 'atm'):
   """Convert units of pressure from an initial to a final value.

   This method enables the conversion of units of pressure between
   the commonly used units such as atm, mm Hg, Pa, bar, and more.

   Examples
   --------
   Convert from atm to Pa.

   >>> val = 2.0
   >>> print(convert_pressure_units(val, input_unit = 'atm', out_unit = 'Pa'))

   Parameters
   ----------
   value: int or float
      The input value that you want to convert.
   input_unit: str
      The unit of the initial provided value.
   out_unit: str
      The output unit that you want to convert to.
   """
   # Convert and validate the provided input and output units.
   input_unit = input_unit.replace(" ", "").lower()
   out_unit = out_unit.replace(" ", "").lower()
   for pressure_unit in [input_unit, out_unit]:
      if pressure_unit.replace(" ", "").lower() not in PRESSURE_UNITS:
         raise ValueError(f"The unit \'{pressure_unit}\' not "
                          f"a valid unit of pressure.")

   # Convert the input pressure value to atm (as an intermediate).
   value = to_atm(value, input_unit)

   # Return values for all the different cases.
   if out_unit == "pa":
      return value * 101325
   if out_unit == "kpa":
      return value * 101.325
   if out_unit == "bar":
      return value * 1.01325
   if out_unit == "mmhg" or out_unit == "torr":
      return value * 760
   if input_unit == "psi":
      return value * 14.69595

   # Otherwise, the output value is atm, so return that.
   return value

def convert_temperature_units(value, input_unit = 'c', out_unit = 'k'):
   """Convert units of temperature from an initial to a final value.

   This method enables the conversion of units of temperature
   between the units of Celsius, Farenheit, and Kelvin.

   Examples
   --------
   Convert from Farenheit to Celsius

   >>> val = 46.4
   >>> print(convert_pressure_units(val, input_unit = 'f', out_unit = 'c'))

   Parameters
   ----------
   value: int or float
      The input value that you want to convert.
   input_unit: str
      The unit of the initial provided value.
   out_unit: str
      The output unit that you want to convert to.
   """
   # Convert and validate the provided input and output units.
   input_unit = input_unit.replace(" ", "").lower()
   out_unit = out_unit.replace(" ", "").lower()
   for pressure_unit in [input_unit, out_unit]:
      if pressure_unit.replace(" ", "").lower() not in TEMP_UNITS:
         raise ValueError(f"The unit \'{pressure_unit}\' is not "
                          f"a valid unit of temperature.")

   # Convert the input pressure value to atm (as an intermediate).
   value = to_kelvin(value, input_unit)

   # Return values for all the different cases.
   if out_unit == "c":
      return value - 273
   if out_unit == "f":
      return (value - 273.15) * (9 / 5) + 32

   # Otherwise, the output value is K, so return that.
   return value

# Internal intermediate unit conversion formulas.

def to_atm(value, initial_unit = "mm Hg"):
   """Convert pressure units to standard atmospheres.

   This is an internal intermediate method to convert all
   provided values to the same intermediate unit, which
   greatly simplifies exposed calculation methods.

   Internally, this is also mainly used to simplify
   ideal gas calculations in the gas module.
   """
   # Validate that the provided unit is a usable one.
   initial_unit = initial_unit.replace(" ", "").lower()
   if initial_unit.replace(" ", "").lower() not in PRESSURE_UNITS:
      raise ValueError("That is not a valid unit of pressure.")

   # Return values for the different cases.
   if initial_unit == "pa":
      return value / 101325
   if initial_unit == "kpa":
      return value / 101.325
   if initial_unit == "bar":
      return value / 1.01325
   if initial_unit == "mmhg" or initial_unit == "torr":
      return value / 760
   if initial_unit == "psi":
      return value / 14.69595

   # Otherwise, the input value is simply atm, so return the input.
   return value

def to_kelvin(value, initial_unit = "c"):
   """Convert temperature units to Kelvin.

   This is an internal intermediate method to convert all
   provided values to the same intermediate unit, which
   greatly simplifies exposed calculation methods.

   Internally, this is also mainly used to simplify
   ideal gas calculations in the gas module.
   """
   # Validate that the provided unit is a usable one.
   initial_unit = initial_unit.replace(" ", "").lower()
   if initial_unit.replace(" ", "").lower() not in TEMP_UNITS:
      raise ValueError("That is not a valid unit of temperature.")

   # Return values for the different cases.
   if initial_unit == "c":
      return value + 273.15
   if initial_unit == "f":
      return (value - 32) * (5 / 9) + 273.15

   # Otherwise, the input value is simply K, so return the input.
   return value



