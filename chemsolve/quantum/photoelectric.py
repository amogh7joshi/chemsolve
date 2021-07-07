#!/usr/bin/env python3
# -*- coding = utf-8 -*-
from chemsolve.utils.constants import *
from chemsolve.utils.validation import resolve_float_or_constant

def energy_change(initial, final):
   """Calculates the energy change between two states.

   This method calculates the energy change between two
   photoelectric spectrum states, primarily corresponding
   to hydrogen atoms.

   Examples
   --------
   Calculate the energy change between two different states.

   >>> energy = energy_change(2, 4)

   Parameters
   ----------
   initial: int
      - The initial energy level of the atom.
   final: int
      - The final energy level of the atom.
   """
   # Resolve the input states.
   initial = resolve_float_or_constant(initial)
   final = resolve_float_or_constant(final)

   # Return the value.
   return -round(rH * (1 / (final ** 2) - 1 / (initial ** 2)), 4)

def level_transition(initial, final, mode = 'w'):
   """Calculates the wavelength of frequency required to
   move between two energy states.

   Given an initial energy state and a final energy state,
   this method will calculate the wavelength or frequency
   required to move within the state, based on the `mode`
   parameter.

   Examples
   --------
   Calculate the frequency required to move between states.

   >>> freq = level_transition(2, 4, mode = 'f')

   Or, calculate the wavelength required.

   >>> wav = level_transition(4, 2, mode = 'w')

   Parameters
   ----------
   initial: int
      - The initial energy level of the atom.
   final: int
      - The final energy level of the atom.
   mode: str
      - What to calculate, either 'w' for wavelength
      or 'f' for frequency.
   """
   # Resolve the input states.
   initial = resolve_float_or_constant(initial)
   final = resolve_float_or_constant(final)

   # Validate the input mode.
   if mode not in ['w', 'f']:
      raise ValueError(
         "Expected either 'w' (wavelength) or "
         "'f' (frequency) for `mode`.")

   # Return the different cases.
   if mode == 'w':
      return h * C / energy_change(initial, final)
   return energy_change(initial, final) / h

