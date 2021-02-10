from chemsolve import molarity
from chemsolve.compound import SolutionCompound

print(molarity(SolutionCompound("H2SO4", volume = 2.14, molarity = 2.15), setting = "moles"))