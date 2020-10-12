import operator
import re
import sys
import sympy
from pprint import pprint

from chempy import Substance
from chempy import balance_stoichiometry
from chempy import Equilibrium

from chemsolve.compound import Compound
from chemsolve.compound import FormulaCompound
from chemsolve.element import Element
from chemsolve.element import SpecialElement

try:
   import periodictable as pt
except ModuleNotFoundError:
   print("The module periodictable has not been installed.")
except ImportError:
   print("The module periodictable could not be found (may have not been installed).")

class Reaction:
   '''
   Stores a balanced/unbalanced chemical reaction.

   INPUTS:
   Takes in Compound objects, either predefined or defined for the purposes of the reaction.
   Reactants/Products are split by "-->".
   CALCULATIONS:
   Define the quantity of each compound (either moles or grams) directly in the Compound class of each object.
   The class will directly use these for its calculations.

   If you want to use the calculation methods, you have to set the calculation booleans to True.
   Otherwise, it will force you to enter values for the moles/grams of each compound even if you don't have them.
   '''
   def __init__(self, *args, lim_calc = False, **kwargs):
      self.lim_calc = lim_calc
      self.reactants = []
      self.products = []
      self.original_reaction = ""
      self.__reactant_store = []
      self.__product_store = []

      tempvar = self.reactants
      tempvar2 = self.__reactant_store
      for compound in args:
         if isinstance(compound, str):
            self.original_reaction += str("--> ")
            tempvar = self.products
            tempvar2 = self.__product_store
         else:
            tempvar2.append(compound)
            self.original_reaction += str(compound.__str__() + " ")
            if compound != args[-1] and not isinstance(args[args.index(compound) + 1], str):
               self.original_reaction += str("+ ")
            if not isinstance(compound, Compound) and not isinstance(compound, FormulaCompound):
               raise TypeError("The object " + str(compound) + " is not of type Compound or related subclasses, please redefine it.")
            else: tempvar.append(compound.__repr__())

      self.__balanced = self.__balance()
      self.balanced_reaction = self.balanced_display()
      self.limiting_reactant = self.get_limiting_reactant(self.lim_calc)
      self.coefficient_sum = self.get_coefficient_sum()

   def __str__(self):
      return self.original_reaction

   def __call__(self, *args, **kwargs):
      pass
      #TODO: Add to this call function.

   def __getattr__(self, item):
      return "The attribute " + str(item) + " does not exist within this class."

   '''
   Functions which gather attributes.
   '''
   @property
   def get_reactants(self):
      '''
      Returns the reactants of the reaction.
      '''
      return self.reactants

   @property
   def get_products(self):
      '''
      Returns the products of the reaction.
      '''
      return self.products

   def __balance(self):
      '''
      Private method. Returns ordered dictionaries containing the balanced reaction's reactants and products.
      '''
      #FIXME: Remove.

      # print(self.reactants)
      # print(self.products)
      return balance_stoichiometry({f for f in self.reactants}, {f for f in self.products})

   def balanced_display(self):
      '''
      Returns a displayable version of the balanced reaction.
      '''
      tempstr = ""
      e1 = list(self.__balanced[0].items())
      count = 0
      for reactant in self.reactants:
         count += 1
         for item in self.__balanced[0]:
            if str(item) == str(reactant):
               self.__balanced[0][item] = int(self.__balanced[0][item])
               if not self.__balanced[0][item] == 1:
                  tempstr += str(self.__balanced[0][item])
               tempstr += str(Compound(str(item)).__str__()) + str(" ")
               if count < len(e1):
                  tempstr += str("+ ")
      tempstr += str("--> ")
      #----
      e2 = list(self.__balanced[1].items())
      count = 0
      for product in self.products:
         count += 1
         for item in self.__balanced[1]:
            if str(item) == str(product):
               self.__balanced[1][item] = int(self.__balanced[1][item])
               if not self.__balanced[1][item] == 1:
                  tempstr += str(self.__balanced[1][item])
               tempstr += str(Compound(str(item)).__str__()) + str(" ")
               if count < len(e2):
                  tempstr += str("+ ")

      # Original Code --> utils/past_code

      return tempstr

   def get_coefficient_sum(self):
      '''
      Returns the sum of the coefficients of the reactants and products in the reaction.
      '''
      self.coefficient_sum = 0
      for item in self.__balanced[0]:
         self.coefficient_sum += int(self.__balanced[0][item])
      for item in self.__balanced[1]:
         self.coefficient_sum += int(self.__balanced[1][item])

      return self.coefficient_sum

   def get_limiting_reactant(self, lim_calc = False):
      '''
      Returns the limiting reactant of the chemical reaction. Uses the moles/grams values from the Compound objects.
      '''
      if lim_calc == True:
         lim_reac = Compound
         quant = sys.maxsize
         product = (next(iter((self.__balanced[1]).items())))[1]
         moles = 0
         org_moles = 0

         for item in list((self.__balanced[0]).items()):
            for com in self.__reactant_store:
               if Compound(item[0]).__str__() == com.__str__():
                  moles = com.mole_amount
                  org_moles = moles
            moles *= operator.truediv(product, item[1])
            if moles < quant:
               lim_reac = item[0]

         return Compound(lim_reac, moles = org_moles)
      else:
         return False

class CombustionTrain(Reaction):
   '''
   Determines an unknown compound in a combustion reaction.

   Used in a combustion reaction, when knowing the mass of the initial compound(made up of C, H, and O),
   when knowing the masses of the CO2 and H2O collected (or moles, in each case).
   Once the unknown compound is determined, it will have the attributes of the regular reaction class.

   INPUTS:
   Takes in only two compounds: CO2 and H2O (and their masses), the products of the reaction.
   Oxygen is automatically added and once calculated, the additional compound is also added.
   If the main compound is made up of O atoms in addition to C and H, then the parameter hydrocarbon
   must be set to False and the mass of oxygen added as a parameter.
   ADDITIONAL INPUTS:
   If the main compound is made up of another element as well, this class can be modified.
   If there is another element as a product, then add an element class. If a compound, then a compound.
   **You must enter the products in the order: CO2, H2O, <other element/compound>.

   The limiting reactant will always be assumed to be the non-oxygen reactant, as with most calculated
   combustion reaction.

   **This class only determines the reacting compound, so DO NOT use this class for a regular reaction.
   '''
   def __init__(self, *args, hydrocarbon = True, othercompound = False, sample_mass = 0.0, **kwargs):
      # A lot of errors may arise, all need to be prevented.
      if hydrocarbon == False:
         if sample_mass == 0.0:
            raise AttributeError("You must provide the total mass of the product in order to determine the quantity of oxygen.")
         else:
            sample_mass = round(float(sample_mass), 4)
      if len(kwargs) > 3:
         raise ValueError("The CombustionTrain class currently doesn't support more than one additional compound.")

      self.__product_store = []
      self.products = []
      for compound in args:
         try:
            compound.mass
         except AttributeError as exception:
            print("You must provide the masses of the compounds as acquired in the Compound definition.")
            raise exception
         else:
            self.__product_store.append(compound)
            self.products.append(compound.__repr__())

      if hydrocarbon == True:
         if othercompound == True:
            self.main_reactant = Compound(self.determine_main_compound(
               sample_mass, hydrocarbon = hydrocarbon, othercompound = True))
         else:
            self.main_reactant = Compound(self.determine_main_compound(sample_mass, hydrocarbon = hydrocarbon))
      if hydrocarbon == False:
         self.main_reactant = Compound(self.determine_main_compound(sample_mass, hydrocarbon = hydrocarbon), grams = sample_mass)

      #TODO: Fix this again!
      #---------------------
      # Make sure the products in the reaction goes in the order CO2, H2O.
      # if args[0].__repr__() == "H2O":
         # args[0], args[1] = args[1], args[0]

      if len(args) == 2:
         super().__init__(self.main_reactant, Compound('O2'), "-->", args[0], args[1])
      elif len(args) == 3:
         super().__init__(self.main_reactant, Compound('O2'), "-->", args[0], args[1], Compound(args[2].__repr__()))
      self.limiting_reactant = self.main_reactant

   def determine_main_compound(self, sample_mass, hydrocarbon = True, othercompound = False):
      '''
      Determines the main compound in the combustion reaction.
      '''
      mole_val = []
      __hold = []
      other = None

      #TODO: Add functionality for giving the other compound but not its mass, and having to calculate that.
      #-------------------
      # other_calc = False

      if hydrocarbon == False and othercompound == True:
            raise ValueError("You cannot have a hydrocarbon that also contains another element.")
      for index, compound in enumerate(self.__product_store):
         if 'O' not in compound.__repr__() and not isinstance(compound, (Element, SpecialElement)):
            raise TypeError("The CombustionTrain class only takes in oxide compounds or elements.")
         total = operator.__truediv__(compound.gram_amount, compound.mass)
         if compound.__repr__() == 'CO2':
            mole_val.append(total * compound.moles_in_compound('C'))
            __hold.append('C')
         elif compound.__repr__() == 'H2O':
            mole_val.append(total * compound.moles_in_compound('H'))
            __hold.append('H')
         else:
            if 'O' in compound.__repr__():
               other = str(compound.__repr__()[0])
               mole_val.append(total * compound.moles_in_compound(other))
            else:
               other = str(compound.__repr__())
               mole_val.append(compound.mole_amount)
            __hold.append(other)

      if hydrocarbon == True:
         if other == None:
            reactant = FormulaCompound(SpecialElement('C', moles = mole_val[0]), SpecialElement('H', moles = mole_val[1]))\
                       .empirical.__repr__()
            self.main_reactant = reactant
         else:
            reactant = FormulaCompound(SpecialElement('C', moles = mole_val[0]), SpecialElement('H', moles = mole_val[1]),
                                       SpecialElement(other, moles = mole_val[2])).empirical.__repr__()
            self.main_reactant = reactant

      if hydrocarbon == False:
         e1 = mole_val[0] * Element('C').mass
         e2 = mole_val[1] * Element('H').mass
         reactant = None
         if other == None:
            e3 = sample_mass - e1 - e2
            mole_val.append(operator.truediv(e3, Element('O').mass))

            reactant = FormulaCompound(SpecialElement('C', moles = mole_val[0]), SpecialElement('H', moles = mole_val[1]),
                                       SpecialElement('O', moles = mole_val[2])).empirical.__repr__()
         else:
            e3 = mole_val[2] * Element(other).mass
            e4 = sample_mass - e1 - e2 - e3
            mole_val.append(operator.truediv(e4, Element('O').mass))

            reactant = FormulaCompound(SpecialElement('C', moles = mole_val[0]), SpecialElement('H', moles = mole_val[1]),
                                       SpecialElement(other, moles = mole_val[2]), SpecialElement('O', moles = mole_val[3])).empirical.__repr__()
         self.main_reactant = reactant

      return self.main_reactant





