import operator

from chemsolve.utils.constants import *

def energy_change(initial, final):
   '''
   Returns the energy required to move between different energy states.
   '''
   return -round(rH * (1 / (operator.__pow__(final, 2)) - 1 / (operator.__pow__(initial, 2))), 4)

def level_transition(initial, final, wavelength = None, frequency = None):
   '''
   Returns the wavelength or frequency of moving between different energy states, based on the parameter
   '''
   if frequency and wavelength:
      raise ValueError("You cannot provide both the frequency and the wavelength. ")
   if wavelength: return h * C / energy_change(initial, final)
   if frequency: return energy_change(initial, final) / h
   return 0


