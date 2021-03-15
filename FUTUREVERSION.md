# Future Changes

This file contains a list of changes which are intended to be implemented in the future, 
primarily non-backwards compatible changes which will be implemented in Chemsolve v2.0.0.

Before that, a list of changes which are to arrive in v1.8.0 and v1.9.0:

### Changes for v1.8.0:

- Adding a ranking system for element properties, where you can add a list of element or element 
names and the methods will rank them based on a certain attribute, such as electronegativity or atomic radius.
- Updates to the `chemsolve.solutions` module, including pH, pOH, and further operations involving concentrations.

### Changes for v1.9.0:
- Introducing the `chemsolve.quantum` module, with methods for basic modern physics and quantum chemistry.

Many of the changes which are to be implemented in v2.0.0 will be heavily non-backwards compatible, 
so here is a list of those changes to keep in mind for the future, somewhat organized by least destructive to most destructive.

## Changes for v2.0.0:
- **Removal of the FormulaCompound and CombustionTrain classes.** These were deprecated in v1.5.0, 
and they will be entirely removed in v2.0.0 in favor of `Compound.from_formula` and `Reaction.from_combustion`.
- Renaming of `Compound.fromFormula` and `Reaction.fromCombustion` to `Compound.from_formula` and `Reaction.from_combustion`.
- Changing the input method of the `Reaction` class, instead of a list of string arguments separated with a `'-->'`, the inputs
will be two individual dictionaries where reactants and products can be inputted. 
- Renaming the `Reaction.get_reactants` and `Reaction.get_products` properties directly to `Reaction.reactants` and `Reaction.products`.
- Removing the `SpecialElement` class, and replacing any of its prior instances with `Element` instead.
- Design a base OOP framework for the library, such that all classes including `Compound`, `Element`, and `Reaction` will inherit from a base class
with a `__new__` method to dispatch to a relevant class. Purposes:
    - Have the instantiation of a `Compound` class automatically return a `StrongAcid` or `StrongBase` class with the same features
    of the original `Compound` class, but allowing for easier method development for chemical methods involving acids/bases.
- Move all of the actual library source code to a `chemsolve.source` directory with the main library code being exposed through an API, preventing
runaway imports or access to internal methods which disrupt the library usage.

*Note: This is not a complete list of changes, additional changes will be added as seen fit. Furthermore, changes may be removed from 
this list if they are determined to be not worth or not feasible to add.* 