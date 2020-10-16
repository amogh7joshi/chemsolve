import operator

from chemsolve.element import Element
from chemsolve.element import SpecialElement
from chemsolve.compound import Compound

# Methods used by the former CombustionTrain class.
# Returns the primary element in a combustion reaction..

def determine_main_compound(product_store, sample_mass, hydrocarbon = True, othercompound = False):
   '''
   Determines the main compound in the combustion reaction.
   '''
   global main_reactant
   mole_val = []
   __hold = []
   other = None

   if hydrocarbon == False and othercompound == True:
      raise ValueError("You cannot have a hydrocarbon that also contains another element.")
   for index, compound in enumerate(product_store):
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
         reactant = Compound.fromFormula(SpecialElement('C', moles=mole_val[0]), SpecialElement('H', moles=mole_val[1])) \
            .empirical.__repr__()
         main_reactant = reactant
      else:
         reactant = Compound.fromFormula(SpecialElement('C', moles=mole_val[0]), SpecialElement('H', moles=mole_val[1]),
                                    SpecialElement(other, moles=mole_val[2])).empirical.__repr__()
         main_reactant = reactant

   if hydrocarbon == False:
      e1 = mole_val[0] * Element('C').mass
      e2 = mole_val[1] * Element('H').mass

      if other == None:
         e3 = sample_mass - e1 - e2
         mole_val.append(operator.truediv(e3, Element('O').mass))

         reactant = Compound.fromFormula(SpecialElement('C', moles=mole_val[0]), SpecialElement('H', moles=mole_val[1]),
                                    SpecialElement('O', moles=mole_val[2])).empirical.__repr__()
      else:
         e3 = mole_val[2] * Element(other).mass
         e4 = sample_mass - e1 - e2 - e3
         mole_val.append(operator.truediv(e4, Element('O').mass))

         reactant = Compound.fromFormula(SpecialElement('C', moles=mole_val[0]), SpecialElement('H', moles=mole_val[1]),
                                    SpecialElement(other, moles=mole_val[2]),
                                    SpecialElement('O', moles=mole_val[3])).empirical.__repr__()
      main_reactant = reactant

   return main_reactant






