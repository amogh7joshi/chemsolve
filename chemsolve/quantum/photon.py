import operator

from chemsolve.quantum.photoelectric import energy_change
from chemsolve.utils.constants import *

class Photon(object):
   '''
   A class which represents a photon. Contains the frequency, energy, and wavelength of the photon.
   '''
   def __init__(self, **kwargs):
      if "frequency" in kwargs:
         self.frequency = kwargs["frequency"]
         self.wavelength = C / self.frequency
         self.energy = h * self.frequency

      if "wavelength" in kwargs:
         self.wavelength = kwargs["wavelength"]
         self.frequency = C / self.wavelength
         self.energy = h * self.frequency

      if all(x in ["frequency", "wavelength", "energy"] for x in [kwargs]):
         raise ValueError("You cannot provide multiple quantities of the photon at a single time.")


