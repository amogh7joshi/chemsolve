from __future__ import division

import operator

import numpy as np

from chemsolve.utils.constants import *

__all__ = ['kinetic_energy', 'gravitational_potential_energy']

def kinetic_energy(mass, velocity):
   # Basic Kinetic Energy Calculations.
   return (1 / 2) * mass * (velocity ** 2)

def gravitational_potential_energy(mass, height):
   # Basic Gravitational Potential Energy Calculations.
   return mass * G * height


