#!/usr/bin/env python3
# -*- coding = utf-8 -*-
from chemsolve.utils.constants import *

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
      - The final energy level of the atm.
   """
   return -round(rH * (1 / (final ** 2) - 1 / (initial ** 2)), 4)