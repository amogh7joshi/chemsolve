from chemsolve import Element

oxygen = Element("O")
print(oxygen.mass)
print(oxygen.number)
print(oxygen.element_name)
print(oxygen.element_symbol)

boron = Element('B', moles = 2.50)
print(boron.mole_amount)
print(boron.gram_amount)

boron(grams = 30.00)
print(boron.mole_amount)
print(boron.gram_amount)

magnesium = Element.from_electron_configuration('[Ne]3s2')
assert magnesium.__str__() == "Magnesium"
