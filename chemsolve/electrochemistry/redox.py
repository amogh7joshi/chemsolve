import re
import sys

from chempy import Equilibrium
from chempy.chemistry import Species

from chemsolve.compound import Compound
from chemsolve.reaction import Reaction
from chemsolve.utils.string_op import charge, charge_value
from chemsolve.utils.string_op import ignore
from chemsolve.utils.string_op import oxidation_number
from chemsolve.utils.warnings import assert_presence
from chemsolve.utils.constants import *

class RedoxReaction(object):
   def __init__(self, reactants = (), products = (), *args, **kwargs):
      self.reactants = {}
      self.products = {}
      self.__main_reac = []
      self.__main_prod = []

      for reac in reactants:
         self.reactants.update({charge(reac)[0]: str(charge(reac)[1])})
         self.__main_reac.append(charge(reac)[0])
      for prod in products:
         self.products.update({charge(prod)[0]: str(charge(prod)[1])})
         self.__main_prod.append(charge(prod)[0])

      self.__main_reac = ignore(self.__main_reac, param = BASEREDOX)
      self.__main_prod = ignore(self.__main_prod, param = BASEREDOX)
      assert_presence(self.__main_reac, self.__main_prod)
      self.oxidized, self.reduced = self.electron_shift()

   def electron_shift(self):
      for key in self.reactants:
         initial = oxidation_number(key, self.reactants[key])
         final = oxidation_number(key, self.products[key])
         print(initial, final)
         if final > initial: self.oxidized = key
         if initial > final: self.reduced = key

      return self.oxidized, self.reduced

   def half_reactions(self):
      for index, reactant in enumerate(self.reactants):
         pass



c = RedoxReaction(reactants = ("Al", "Cu2+"), products = ("Al3+", "Cu"))
