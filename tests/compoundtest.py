from chemsolve import Compound
from chemsolve.compound import FormulaCompound

lead_nitrate = Compound("Pb(NO3)2")
print(lead_nitrate.mass)
print(lead_nitrate.compound_elements)
print(lead_nitrate)
print(lead_nitrate.print_compound)

ammonium = Compound("NH4", moles = 1.50)
print(ammonium.mole_amount)
print(ammonium.gram_amount)
ammonium(grams = 4.50)
print(ammonium.mole_amount)
print(ammonium.gram_amount)

water = Compound("H2O")
print(water.moles_in_compound("H"))
print(water.percent_in_compound("O"))

from chemsolve import SpecialElement
carbon = SpecialElement("C", percent = 0.5714)
hydrogen = SpecialElement("H", percent = 0.0616)
nitrogen = SpecialElement("N", percent = 0.0952)
oxygen = SpecialElement("O", percent = 0.2718)
compound = Compound.from_formula(carbon, hydrogen, nitrogen, oxygen)
print(compound)
print(compound.mass)
print(compound.compound_elements)
print(compound.print_compound)
print(compound.moles_in_compound('C'))
print(compound.percent_in_compound('O'))

carbon = SpecialElement("C", percent = 0.7595)
nitrogen = SpecialElement("N", percent = 0.1772)
hydrogen = SpecialElement("H", percent = 0.0633)
compound = FormulaCompound(carbon, nitrogen, hydrogen, molecular = True, mass = 240)
print(compound)
print(compound.empirical)
