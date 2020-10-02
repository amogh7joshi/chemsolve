import operator
import re
import sys
import sympy
from pprint import pprint
from collections import OrderedDict

from math import isclose
from math import floor, ceil

try:
   import tkinter as tk
except ImportError:
   import Tkinter as tk

from chempy import Substance
from chempy import balance_stoichiometry
from chempy import Equilibrium

try:
   import periodictable as pt
except ModuleNotFoundError:
   print("The module periodictable has not been installed.")
except ImportError:
   print("The module periodictable could not be found (may have not been installed).")

def split(item):
   return [char for char in item]

class Element:
   def __init__(self, element_symbol, **kwargs):
      self.element_symbol = element_symbol
      self.element_name = self.get_element_name()
      self.mass = self.get_mass()
      self.number = self.get_atomic_number()

      '''
      The class can calculate quantities of moles and grams, depending on the specific keywords 'moles' and 'grams'.
      '''
      if "moles" in kwargs:
         self.mole_amount = kwargs["moles"]
         self.gram_amount = round(operator.mul(self.mole_amount, self.mass), 4)

      if "grams" in kwargs:
         self.gram_amount = kwargs["grams"]
         self.mole_amount = round(operator.truediv(self.gram_amount, self.mass), 4)

      if "moles" in kwargs and "grams" in kwargs:
         raise Exception("You cannot provide both the number of moles and grams of the element at a single time.")

   def __str__(self):
      return str(self.element_name.title())

   def __repr__(self):
      return str(self.element_symbol.title())

   def __getattr__(self, item):
      if item == "percent_of":
         raise AttributeError("If you want to use percentages, you must use the SpecialElement class.")
      print("The attribute " + str(item) + " does not exist within this class.")

   def __call__(self, **kwargs):
      if "moles" in kwargs:
         self.mole_amount = kwargs["moles"]
         self.gram_amount = round(operator.mul(self.mole_amount, self.mass), 4)

      if "grams" in kwargs:
         self.gram_amount = kwargs["grams"]
         self.mole_amount = round(operator.truediv(self.gram_amount, self.mass), 4)

      if "moles" in kwargs and "grams" in kwargs:
         raise TypeError("You cannot provide both the number of moles and grams of the element at a single time.")

   '''
   Functions which gather attributes.
   '''
   def get_element_name(self):
      '''
      Returns the element name from the symbol.
      '''
      try:
         return getattr(pt, self.element_symbol.title()).name
      except AttributeError:
         print("That is not an existing element in the periodic table.")

   def get_mass(self):
      '''
      Returns the atomic (and therefore molar) mass of the element.
      '''
      return getattr(pt, self.element_symbol.title()).mass

   def get_atomic_number(self):
      '''
      Returns the atomic number of the element.
      '''
      return getattr(pt, self.element_symbol.title()).number

   '''
   Functions which perform calculations.
   '''
   def calculate_moles(self):
      return round(operator.truediv(self.gram_amount, self.mass), 3)

   def calculate_grams(self):
      return operator.mul(self.mole_amount, self.mass)

class SpecialElement(Element):
   '''
   A special variant of the Element class created for the FormulaCompound class.

   Contains the extra parameter of percentage, in order to use percentages to find the formula of the compound.
   If percentage is defined, the percentage parameter overrides the gram and mole parameters in the FormulaCompound class.
   If grams is defined, the grams parameter overrides the mole and percent parameter. Ideally, moles shouldn't be used in the first place.
   If percentage is defined in one SpecialElement, it must be defined in all other elements. Same goes for grams.

   **Should only be used for the FormulaCompound class. If simply defining an element, use the Element class.
   '''
   def __init__(self, element_symbol, **kwargs):
      super().__init__(element_symbol = element_symbol, **kwargs)

      if len(kwargs) == 0:
         raise Warning("If you are not looking to define any values, you should use the Element class instead.")
      if "grams" not in kwargs and "percent" not in kwargs and "moles" not in kwargs:
         raise Warning("If you are not looking to define any numerical values, you should use the Element class instead.")

      if "grams" in kwargs:
         self.gram_amount = kwargs["grams"]; self.mole_amount = False; self.percent_of = False
      else: self.gram_amount = False
      if "percent" in kwargs:
         if float(kwargs["percent"]) >= 1:
            raise TypeError("That is not a valid input for the percent field. Enter a percent as a decimal.")
         self.percent_of = kwargs["percent"]; self.mole_amount = False; self.gram_amount = False
      else: self.percent_of = False
      if "moles" in kwargs:
         self.mole_amount = kwargs["moles"]; self.gram_amount = False; self.percent_of = False


class Compound:
   def __init__(self, compound, *args, **kwargs):
      self.compound = pt.formula(compound)
      self.mass = self.get_mass()
      self.compound_elements_list = self.get_elements_in_compound_ions(compound)
      self.compound_elements = {}
      self.compound.elements = self.get_elements_in_compound()
      self.print_compound = Substance.from_formula(compound)

      '''
      The class can calculate quantities of moles and grams, depending on the specific keywords 'moles' and 'grams'.
      '''
      if "moles" in kwargs:
         self.mole_amount = kwargs["moles"]
         self.gram_amount = round(operator.mul(self.mole_amount, self.mass), 4)

      if "grams" in kwargs:
         self.gram_amount = kwargs["grams"]
         self.mole_amount = round(operator.truediv(self.gram_amount, self.mass), 4)

      if "moles" in kwargs and "grams" in kwargs:
         raise Exception("You cannot provide both the number of moles and grams of the element at a single time.")

   def __str__(self):
      return str(self.print_compound.unicode_name)

   def __repr__(self):
      return str(self.compound)

   def __getattr__(self, item):
      print("The attribute " + str(item) + " does not exist within this class.")

   def __call__(self, **kwargs):
      if "moles" in kwargs:
         self.mole_amount = kwargs["moles"]
         self.gram_amount = round(operator.mul(self.mole_amount, self.mass), 4)

      if "grams" in kwargs:
         self.gram_amount = kwargs["grams"]
         self.mole_amount = round(operator.truediv(self.gram_amount, self.mass), 4)

      if "moles" in kwargs and "grams" in kwargs:
         raise Exception("You cannot provide both the number of moles and grams of the element at a single time.")

   '''
   Functions which gather attributes.
   '''
   def get_mass(self):
      '''
      Returns the atomic (and therefore molar) mass of the compound.
      '''
      return self.compound.mass

   def get_elements_in_compound_ions(self, compound):
      '''
      Returns each of the individual polyatomic ions in the element (both element symbol and number).
      '''
      t = compound
      if "(" in t:
         if ")" not in t:
            raise TypeError("That is not a valid format for a compound.")
         left = t.index("(")
         right = t.index(")")
         charge = int(t[right + 1])
         f = re.findall('[A-Z][^A-Z]*', t[(left + 1):right])
         replacer = ""
         for val in f:
            val = str(val)
            if val[-1].isdigit():
               z = val[-1]
               val = val[:-1]
               q = str(int(z) * int(charge))
               val += q
            else:
               val += str(charge)
            replacer += val

         t = t[:left] + str(replacer)

      return re.findall('[A-Z][^A-Z]*', str(t))

   def get_elements_in_compound(self):
      '''
      Returns a dictionary containing the elements in the compound and the quantity of each element.
      '''
      for item in self.compound_elements_list:
         item_val = split(item)
         if item_val[-1].isdigit():
            self.compound_elements.update({''.join(item_val[:-1]): int(item_val[-1])})
         else:
            self.compound_elements.update({item: 1})

   '''
   Functions which perform calculations.
   '''
   def moles_in_compound(self, element):
      '''
      Returns the number of moles of a certain element within one mole of the compound.
      '''
      try:
         return(self.compound_elements[element])
      except KeyError:
         print("That is not an element in this compound.")
      except AttributeError:
         print("That is not an element.")

   def percent_in_compound(self, element):
      '''
      Returns the percentage of a certain element within the compound.
      '''
      try:
         return round(operator.truediv((Element(element.title()).mass * self.compound_elements[element]), self.mass), 4)
      except KeyError:
         print("That is not an element in this compound.")
      except AttributeError:
         print("That is not an element.")

class FormulaCompound(Compound):
   '''
   Finds empirical, molecular, and other formulas of a compound.

   Has mostly similar attributes to the Compound class, but different inputs.
   Takes in gram/mole values of different elements within a theoretical compound
   and determines the empirical & molecular formulas.
   If the parameter molecular is true, then the class must have a molar mass attribute.
   It will then return the stored formula of the compound as the molecular formula instead of the empirical formula.

   **Use the SpecialElement class to define elements which are going to be used to determine the compound.
   '''
   def __init__(self, *args, molecular = False, **kwargs):
      self.__compound_elements = []

      if len(args) < 2:
         raise ValueError("You may be using the wrong class. The FormulaCompound class is used to determine compound formulas.")
      for element in args:
         if not isinstance(element, SpecialElement):
            raise TypeError("The arguments of this class should only be SpecialElement classes.")
         else:
            self.__compound_elements.append(element)

      if "mass" in kwargs:
         self.molar_mass = kwargs["mass"]

      self.__empirical_coef = self.__determine_empirical_coef()
      self.empirical = Compound(self.determine_empirical())
      self.__empirical_mass = Compound(self.empirical.__repr__()).mass
      if molecular == True:
         self.molecular = self.determine_molecular(self.molar_mass, molecular = True)
         super().__init__(compound = self.molecular.__repr__())
      else:
         super().__init__(compound = self.empirical.__repr__())

   #TODO: Add a __call__ function to be able to update whether the user wants a molecular formula or not.

   def __determine_empirical_coef(self):
      '''
      Private method. Returns the coefficients of the empirical formula of the element.
      '''
      coef_list = []
      for element in self.__compound_elements:
         if element.percent_of != False:
            coef_list.append(operator.truediv(operator.mul(element.percent_of, 100), element.mass))
         if element.gram_amount != False:
            coef_list.append(operator.truediv(element.gram_amount, element.mass))
         if element.mole_amount != False:
            coef_list.append(element.mole_amount)

      least = sys.maxsize
      for item in coef_list:
         if item < least:
            least = item
      coef_list_2 = []
      solved = True
      for item in coef_list:
         t = round(operator.truediv(item, least), 2)
         if not isclose(t, floor(t), abs_tol = 10 ** -1) and not isclose(t, ceil(t), abs_tol= 10 ** -1):
            solved = False
            coef_list_2.append(t)
         else:
            coef_list_2.append(round(t, 1))

      factor = 2
      coef_list_3 = coef_list_2.copy()
      coef_list_4 = []
      overall_solved = True
      while solved == False:
         overall_solved = False
         if solved == False:
            for item in coef_list_3:
               if not isclose(item, floor(item), abs_tol=10 ** -1) and not isclose(item, ceil(item), abs_tol=10 ** -1):
                  z = True
                  while z == True:
                     if round(operator.mul(item, factor), 1).is_integer():
                        z = False
                     else:
                        factor += 1
            for item in coef_list_3:
               coef_list_4.append(round(operator.mul(item, factor), 1))
            coef_list_3 = coef_list_4.copy()
            coef_list_4 = []
            for t in coef_list_3:
               if not isclose(t, floor(t), abs_tol=10 ** -1) and not isclose(t, ceil(t), abs_tol=10 ** -1):
                  solved = False
               else:
                  solved = True

      if overall_solved == False:
         return coef_list_3
      return coef_list_2

   def determine_empirical(self):
      '''
      Returns the empirical formula of the compound.
      '''
      form = ""
      for element in zip(self.__compound_elements, self.__empirical_coef):
         form += str(element[0].__repr__())
         if int(element[1]) != 1:
            form += str(int(element[1]))

      return form

   def determine_molecular(self, mol_mass, molecular = False):
      '''
      Returns the molecular formula of the element, if the molar mass is provided.
      '''
      form = ""
      if molecular == True:
         d = round(operator.truediv(mol_mass, self.__empirical_mass), 1)
         if not d.is_integer():
            raise ValueError("Enter a molar mass that is an integer multiple of the empirical mass.")
         for element in zip(self.__compound_elements, self.__empirical_coef):
            form += str(element[0].__repr__())
            if int(element[1] * d) != 1:
               form += str(int(element[1] * d))

      return form


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
            if not isinstance(compound, Compound):
               raise TypeError("The object " + str(compound) + " is not of type Compound, please redefine it.")
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

      # Original code. Shorter, but printed them out in a different order.
      ''' 
      for dict in self.__balanced:
         for item in dict:
            e = list(dict.items())
            dict[item] = int(dict[item])
            if not dict[item] == 1:
               tempstr += str(dict[item])
            tempstr += str(Compound(str(item)).__str__()) + str(" ")
            if item != e[-1][0]:
               tempstr += str("+ ")
         if count == 0:
            tempstr += str("--> ")
         count += 1
      '''

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

   The limiting reactant will always be assumed to be the non-oxygen reactant, as with most calculated
   combustion reaction.

   **This class only determines the reacting compound, so DO NOT use this class for a regular reaction.
   '''
   def __init__(self, *args, hydrocarbon = True, sample_mass = 0.0, **kwargs):
      # A lot of errors may arise, all need to be prevented.
      if hydrocarbon == False:
         if sample_mass == 0.0:
            raise AttributeError("You must provide the total mass of the product in order to determine the quantity of oxygen.")
         else:
            sample_mass = round(float(sample_mass), 4)
      if len(args) > 2:
         raise AttributeError("You only need to provide the CO2 and H2O compound classes.")

      self.__product_store = []
      self.products = []
      for compound in args:
         try:
            compound.mass
         except AttributeError:
            print("You must provide the masses of CO2 and H2O acquired in the Compound definition.")
         else:
            self.__product_store.append(compound)
            self.products.append(compound.__repr__())

      if hydrocarbon == True:
         self.main_reactant = Compound(self.determine_main_compound(sample_mass, hydrocarbon = hydrocarbon))
      if hydrocarbon == False:
         self.main_reactant = Compound(self.determine_main_compound(sample_mass, hydrocarbon = hydrocarbon), grams = sample_mass)

      # Make sure the products in the reaction goes in the order CO2, H2O.
      if args[0].__repr__() == "H2O":
         args[0], args[1] = args[1], args[0]

      super().__init__(self.main_reactant, Compound('O2'), "-->", args[0], args[1])
      self.limiting_reactant = self.main_reactant


   def determine_main_compound(self, sample_mass, hydrocarbon = True):
      '''
      Determines the main compound in the combustion reaction.
      '''
      mole_val = []
      __hold = []
      for index, compound in enumerate(self.__product_store):
         if compound.__repr__() != 'CO2' and compound.__repr__() != 'H2O':
            raise TypeError("The CombustionTrain class only takes in CO2 and H2O as products.")
         total = operator.truediv(compound.gram_amount, compound.mass)
         if compound.__repr__() == 'CO2':
            mole_val.append(total * compound.moles_in_compound('C'))
            __hold.append('C')
         if compound.__repr__() == 'H2O':
            mole_val.append(total * compound.moles_in_compound('H'))
            __hold.append('H')

      if __hold[0] == 'H':
         mole_val[0], mole_val[1] = mole_val[1], mole_val[0]

      if hydrocarbon == True:
         reactant = FormulaCompound(SpecialElement('C', moles = mole_val[0]), SpecialElement('H', moles = mole_val[1]))\
                    .empirical.__repr__()
         self.main_reactant = reactant

      if hydrocarbon == False:
         e1 = mole_val[0] * Element('C').mass
         e2 = mole_val[1] * Element('H').mass
         e3 = sample_mass - e1 - e2
         mole_val.append(operator.truediv(e3, Element('O').mass))

         reactant = FormulaCompound(SpecialElement('C', moles = mole_val[0]), SpecialElement('H', moles = mole_val[1]),
                                    SpecialElement('O', moles = mole_val[2]))\
                    .empirical.__repr__()
         self.main_reactant = reactant

      return self.main_reactant





'''
elementA = SpecialElement("H", moles = 3.03)
elementB = Element("C", moles = 3)
print(elementA)
print(elementA.mass)
print(elementA.number)
print(elementA.calculate_moles())
print()
elementA.update(grams = 3.03)
print(elementA.calculate_moles())



reaction = "SO2 + O2 --> SO3"

compoundA = Compound("H2SO4")
print(compoundA)
print(compoundA.compound_elements)
print(compoundA.percent_in_compound("O"))
print(compoundA.moles_in_compound("O"))



compound1 = Compound("HNO3", grams = 3.47)
compound2 = Compound("Ca(OH)2", grams = 2.12)
compound3 = Compound("Ca(NO3)2")
compound5 = Compound("H2O")

reactionA = Reaction(compound1, compound2, "--> ", compound3, compound5, lim_calc = True)
print(reactionA.balanced_reaction)
print(reactionA.limiting_reactant)
print(reactionA.coefficient_sum)
print(reactionA.reactants)

'''

specialA = SpecialElement("C", percent = 0.7402)
specialB = SpecialElement("H", percent = 0.08710)
specialC = SpecialElement("N", percent = 0.1727)

formulacompoundA = FormulaCompound(specialA, specialB, specialC)
print(formulacompoundA.mass)
print(formulacompoundA)
print(formulacompoundA.empirical)
formulacompoundA(molecular = True, mass = 162)
print(formulacompoundA)

'''

combustioncomp1 = Compound('CO2', grams = 38.196)
combustioncomp2 = Compound('H2O', grams = 18.752)
train = CombustionTrain(combustioncomp1, combustioncomp2, hydrocarbon = True)
print(train.balanced_reaction)
print(train.limiting_reactant)
print(Compound('C2H4').print_compound)

'''





