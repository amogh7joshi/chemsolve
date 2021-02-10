import operator

from ..compound import Compound

__all__ = ['molarity']

def molarity(compound, setting = None, moles = None, volume = None):
   """
   Calculations involving the molarity of a compound. Returns a value based on the setting.
   The compound must be the Compound class. The moles/volume setting will be gathered from the compound itself if defined.
   **Volume is assumed to be in milliliters.

   Setting --> Molarity: Returns the molarity of the compound from moles and volume.
   Setting --> Moles: Returns the moles of the compound from molarity and volume.
   Setting --> Volume: Returns the volume of the compound from moles and volume.
   """
   # Initialize settings:
   if setting not in ["molarity", "moles", "volume"]:
      raise ValueError("You must choose a setting: molarity, moles volume.")

   if not isinstance(compound, Compound):
      raise AttributeError("You must include a Compound class as the main argument")

   if compound.volume and not volume:
      volume = compound.volume
   if not compound.volume and not volume and setting in ["molarity", "moles"]:
      raise AttributeError("You must define volume either through the Compound class or through the method.")

   if compound.mole_amount and not moles:
      moles = compound.mole_amount
   if not compound.mole_amount and not moles and setting in ["molarity", "volume"]:
      raise AttributeError("You must define the mole amount either through the Compound class or through the method.")

   if not compound.molarity and setting in ["moles", "volume"]:
      raise AttributeError("You must define the molarity of the solution if you want to calculate molarity.")

   # Calculations
   if setting == "molarity":
      return operator.__truediv__(moles, volume)
   if setting == "moles":
      return operator.__mul__(volume, compound.molarity)
   if setting == "volume":
      return operator.__truediv__(moles, compound.molarity)
   else:
      return None

def base_molality(solute, solvent):
   """
   For the most basic calculations involving molality --> takes in just the moles of solute and mass of solvent.
   """
   return operator.__truediv__(solute, solvent)



