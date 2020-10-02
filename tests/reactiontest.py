from chemsolve import Compound, Reaction

r1 = Compound("HSiCl3")
r2 = Compound("H2O")
p1 = Compound("H10Si10O15")
p2 = Compound("HCl")
reaction = Reaction(r1, r2, "-->", p1, p2)
print(reaction)


print(reaction.balanced_reaction)
print(reaction.coefficient_sum)
print(reaction.reactants)
print(reaction.products)

r1 = Compound("KOH", grams = 36.7)
r2 = Compound("H3PO4", grams = 112.7)
p1 = Compound("K3PO4")
p2 = Compound("H2O")
reaction = Reaction(r1, r2, "-->", p1, p2, lim_calc = True)
print(reaction.balanced_reaction)
print(reaction.limiting_reactant)

from chemsolve import CombustionTrain
carbon_dioxide = Compound("CO2", grams = 38.196)
water = Compound("H2O", grams = 18.752)
combustion = CombustionTrain(carbon_dioxide, water)
print(combustion.main_reactant)
print(combustion)
print(combustion.balanced_reaction)
print(combustion.limiting_reactant)

carbon_dioxide(grams = 3.00)
water(grams = 0.816)
combustion = CombustionTrain(carbon_dioxide, water, hydrocarbon = False, sample_mass = 2.00)
print(combustion.main_reactant)
print(combustion)
print(combustion.balanced_reaction)
print(combustion.limiting_reactant)