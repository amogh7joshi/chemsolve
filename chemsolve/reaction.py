import operator
import re
import sys
import sympy

import pyparsing

from chempy import Substance
from chempy import balance_stoichiometry

from chemsolve.element import Element
from chemsolve.element import SpecialElement
from chemsolve.compound import Compound
from chemsolve.compound import FormulaCompound
from chemsolve.utils.combustion import determine_main_compound
from chemsolve.utils.warnings import assert_presence
from chemsolve.utils.warnings import ChemsolveDeprecationWarning
from chemsolve.utils.errors import (
   InvalidElementError, InvalidCompoundError, InvalidReactionError
)

__all__ = ['Reaction', 'CombustionTrain']

try:
   import periodictable as pt
except ModuleNotFoundError:
   print("The module periodictable has not been installed.")
except ImportError:
   print("The module periodictable could not be found (may have not been installed).")

class Reaction(object):
   """
   Stores a balanced/unbalanced chemical reaction.

   INPUTS:
   Takes in Compound objects, either predefined or defined for the purposes of the reaction.
   Reactants/Products are split by "-->".
   CALCULATIONS:
   Define the quantity of each compound (either moles or grams) directly in the Compound class of each object.
   The class will directly use these for its calculations.

   If you want to use the calculation methods, you have to set the calculation booleans to True.
   Otherwise, it will force you to enter values for the moles/grams of each compound even if you don't have them.
   """
   def __init__(self, *args, reactants = (), products = (), lim_calc = False, main_reactant = None, **kwargs):
      self.lim_calc = lim_calc
      self.reactants = []
      self.products = []
      self.original_reaction = ""
      self._reactant_store = []
      self._product_store = []
      assert_presence(self._reactant_store, self._product_store)

      temp = self.reactants
      temp2 = self._reactant_store

      if args: # Adding reactants/products through *args is deprecated, to be removed in v2.0.0.
         # Warn of future deprecation.
         ChemsolveDeprecationWarning("Adding compounds to a Reaction using *args is deprecated and will be "
                                     "removed in v2.0.0. Start using the `reactants` and `products` arguments.",
                                     future_version = 'bypass')
         for compound in args:
            if isinstance(compound, str):
               self.original_reaction += str("--> ")
               temp = self.products
               temp2 = self._product_store
            else:
               temp2.append(compound)
               self.original_reaction += str(compound.__str__() + " ")
               if compound != args[-1] and not isinstance(args[args.index(compound) + 1], str):
                  self.original_reaction += str("+ ")
               if not isinstance(compound, (Element, Compound)):
                  raise TypeError("The object " + str(compound) + " is not of type "
                                  "Compound or related subclasses, please redefine it.")
               else:
                  temp.append(compound.__repr__())
      else:
         self._initialize_reaction(reactants, products)

      self._balanced = self._balance()
      self.balanced_reaction = self.balanced_display()
      self.limiting_reactant = self.get_limiting_reactant(self.lim_calc)
      self.coefficient_sum = self.get_coefficient_sum()

      if main_reactant:
         self.main_reactant = main_reactant

   def __str__(self):
      return self.original_reaction

   def __getattr__(self, item):
      raise AttributeError("The attribute " + str(item) + " does not exist within the Reaction class.")

   def __contains__(self, item):
      # Determine if a compound is in the reaction.
      if isinstance(item, Compound):
         if repr(item) in self.reactants or repr(item) in self.products:
            return True
      elif isinstance(item, str):
         if item in self.reactants or item in self.products:
            return True
      return False

   def _initialize_reaction(self, reactants, products):
      """Internal method to initialize the class reaction from inputs."""
      # Add reactants to list of reactants and original reaction string.
      for reactant in reactants:
         self.original_reaction += str(str(reactant) + " ")
         if reactant != reactants[-1]:
            self.original_reaction += str("+ ")
         self._reactant_store.append(reactant)
         self.reactants.append(repr(reactant))

      # Add the arrow differentiating reactants and products (to the printed reaction).
      self.original_reaction += "--> "

      # Add products to list of products and original reaction string.
      for product in products:
         self.original_reaction += str(str(product) + " ")
         if product != products[-1]:
            self.original_reaction += str("+ ")
         self._product_store.append(product)
         self.products.append(repr(product))

   @classmethod
   def fromCombustion(cls, *args, hydrocarbon = True, othercompound = False, sample_mass = 0.0, **kwargs):
      """
      An implementation of a class method representing a combustion reaction.
      """
      if not hydrocarbon:
         if sample_mass == 0.0:
            raise AttributeError("You must provide the total mass of the product in order "
                                 "to determine the quantity of oxygen.")
         else:
            sample_mass = round(float(sample_mass), 4)
      if len(kwargs) > 3:
         raise ValueError("The Compound.fromCombustion method currently doesn't support more "
                          "than one additional compound.")

      product_store = []
      products = []
      for compound in args:
         try:
            compound.mass
         except AttributeError as exception:
            print("You must provide the masses of the compounds as acquired in the Compound definition.")
            raise exception
         else:
            product_store.append(compound)
            products.append(repr(compound))

      # Calculate main reactant.
      main_reactant = None

      if hydrocarbon:
         if othercompound:
            main_reactant = Compound(determine_main_compound(product_store, sample_mass, hydrocarbon = hydrocarbon,
                                                             othercompound = True))
         else:
            main_reactant = Compound(determine_main_compound(product_store, sample_mass,
                                                             hydrocarbon = hydrocarbon))
      if not hydrocarbon:
         main_reactant = Compound(determine_main_compound(product_store, sample_mass, hydrocarbon = hydrocarbon),
                                  grams = sample_mass)

      return cls(main_reactant, Compound("O2"), "-->", *product_store, main_reactant = main_reactant)

   @staticmethod
   def from_combustion(*args, hydrocarbon = True, othercompound = False, sample_mass = 0.0, **kwargs):
      """A transitional method for v2.0.0, will eventually replace fromCombustion."""
      return Reaction.fromCombustion(*args, hydrocarbon = hydrocarbon, othercompound = othercompound,
                                     sample_mass = sample_mass, **kwargs)

   @classmethod
   def from_string(cls, reaction_string, lim_calc = False, **kwargs):
      """Instantiates a reaction from a string containing the reaction.

      Given a reaction string, e.g. 2H2 + O2 = 2H2O, this class method will
      split the reaction into its relevant compounds and instantiate the
      reaction as necessary.

      This is merely a convenience method if it is easier to simply write a
      string containing the reaction instead of using the traditional method.

      Examples
      --------
      Instantiate the reaction between hydrogen and iodine.

      >>> reaction = Reaction.from_string("H + I = HI")

      Parameters
      ----------
      reaction_string: str
         The string containing the reaction. Note that the reactant/product
         delimiter should be one of: '->', '-->', or '=', and the individual
         compound error should be one of: '+', '&'.
      lim_calc: bool
         The same as the regular instantiation of a reaction class, if True then
         the class will calculate the reaction's limiting reactant.

      Returns
      -------
      An instantiated reaction class.
      """
      # Create holder lists for reactants and products.
      reactants = []
      products = []
      holder = reactants

      # Get each of the compounds/delimiters and parse the reaction.
      values = reaction_string.split(" ")
      try: # Wrap all of the errors in a try/except block to raise custom errors.
         for value in values:
            try:
               holder.append(Compound(value))
            except InvalidCompoundError:
               if value not in ['+', '&', '->', '-->', '=']:
                  # Check for general errors and raise them.
                  raise ValueError(f"Received an invalid delimiter: '{value}'.")
               else: # Otherwise, check for specific cases.
                  if value in ['+', '&']:
                     # We have received a compound delimiter, just continue.
                     continue
                  else:
                     # We have received a reactant/product delimiter, so
                     # switch the list from reactants to products.
                     holder = products
      except ValueError:
         raise InvalidReactionError("Received an invalid reaction, see traceback "
                                    "for the specific cause of the issue.")

      # Instantiate the class.
      return cls(reactants = reactants, products = products,
                 lim_calc = lim_calc, **kwargs)

   @property
   def get_reactants(self):
      """Returns the reactants of the reaction."""
      return self.reactants

   @property
   def get_products(self):
      """Returns the products of the reaction."""
      return self.products

   @property
   def balanced(self):
      """Returns the balanced reaction."""
      return self._balanced

   def _balance(self):
      """Internal method, returns ordered dictionaries containing
      the balanced reaction's reactants and products."""
      try:
         return balance_stoichiometry({f for f in self.reactants}, {f for f in self.products})
      except pyparsing.ParseException:
         raise InvalidReactionError("Received an invalid reaction, there is a reactant "
                                    "which does not appear on the products side, or a product"
                                    "which does not appear on the reactants side.",
                                    property_type = "bypass")

   def balanced_display(self):
      """Returns a displayable version of the balanced reaction."""
      tempstr = ""
      e1 = list(self._balanced[0].items())
      count = 0
      for reactant in self.reactants:
         count += 1
         for item in self._balanced[0]:
            if str(item) == str(reactant):
               self._balanced[0][item] = int(self._balanced[0][item])
               if not self._balanced[0][item] == 1:
                  tempstr += str(self._balanced[0][item])
               tempstr += str(Compound(str(item)).__str__()) + str(" ")
               if count < len(e1):
                  tempstr += str("+ ")
      tempstr += str("--> ")
      #----
      e2 = list(self._balanced[1].items())
      count = 0
      for product in self.products:
         count += 1
         for item in self._balanced[1]:
            if str(item) == str(product):
               self._balanced[1][item] = int(self._balanced[1][item])
               if not self._balanced[1][item] == 1:
                  tempstr += str(self._balanced[1][item])
               tempstr += str(Compound(str(item)).__str__()) + str(" ")
               if count < len(e2):
                  tempstr += str("+ ")

      return tempstr

   def get_coefficient_sum(self):
      """Returns the sum of the coefficients of the reactants and products in the reaction."""
      self.coefficient_sum = 0
      for item in self._balanced[0]:
         self.coefficient_sum += int(self._balanced[0][item])
      for item in self._balanced[1]:
         self.coefficient_sum += int(self._balanced[1][item])
      return self.coefficient_sum

   def get_limiting_reactant(self, lim_calc = False):
      """Returns the limiting reactant of the chemical reaction.
      Uses the moles/grams values from the Compound objects."""
      if not lim_calc: # If we do not want to calculate the limiting reactant.
         return False

      # Create the initial holder objects.
      lim_reac = None
      moles = 0
      org_moles = 0

      # Choose a product to test with.
      product = (next(iter((self._balanced[1]).items())))[1]

      # Iterate over the different reactants.
      for item in list((self._balanced[0]).items()):
         for com in self._reactant_store:
            if str(Compound(item[0])) == str(com):
               # Calculate the mole values.
               moles = com.mole_amount
               org_moles = moles

         # Use stoichiometry to determine the mole values.
         moles *= operator.truediv(product, item[1])
         if moles < sys.maxsize:
            lim_reac = item[0]

      # Return a compound object made from the limiting reactant.
      return Compound(lim_reac, moles = org_moles)

@ChemsolveDeprecationWarning('CombustionTrain', future_version ='2.0.0')
class CombustionTrain(Reaction):
   """
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
   combustion reactions.

   **This class only determines the reacting compound, so DO NOT use this class for a regular reaction.
   """
   def __init__(self, *args, hydrocarbon = True, othercompound = False, sample_mass = 0.0, **kwargs):
      # A lot of errors may arise, all need to be prevented.
      if not hydrocarbon:
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
         except AttributeError:
            raise AttributeError("You must provide the masses of the compounds as acquired in the Compound definition.")
         except Exception as e:
            raise e
         else:
            self.__product_store.append(compound)
            self.products.append(compound.__repr__())

      if hydrocarbon:
         if othercompound:
            self.main_reactant = Compound(self.determine_main_compound(
               sample_mass, hydrocarbon = hydrocarbon, othercompound = True))
         else:
            self.main_reactant = Compound(self.determine_main_compound(sample_mass, hydrocarbon = hydrocarbon))
      if not hydrocarbon:
         self.main_reactant = Compound(self.determine_main_compound(sample_mass, hydrocarbon = hydrocarbon), grams = sample_mass)

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

      # POTENTIAL: Add functionality for giving the other compound but not its mass, and having to calculate that.
      # other_calc = False

      if not hydrocarbon and othercompound:
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

      if hydrocarbon:
         if other is None:
            reactant = FormulaCompound(SpecialElement('C', moles = mole_val[0]), SpecialElement('H', moles = mole_val[1]))\
                       .empirical.__repr__()
            self.main_reactant = reactant
         else:
            reactant = FormulaCompound(SpecialElement('C', moles = mole_val[0]), SpecialElement('H', moles = mole_val[1]),
                                       SpecialElement(other, moles = mole_val[2])).empirical.__repr__()
            self.main_reactant = reactant

      if not hydrocarbon:
         e1 = mole_val[0] * Element('C').mass
         e2 = mole_val[1] * Element('H').mass
         reactant = None
         if other is None:
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





