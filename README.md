# Chemsolve

[![PyPI version](https://img.shields.io/pypi/v/chemsolve)](https://img.shields.io/pypi/v/chemsolve)
[![Downloads](https://pepy.tech/badge/chemsolve)](https://pepy.tech/project/chemsolve)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Travis (.com)](https://img.shields.io/travis/com/amogh7joshi/chemsolve)](https://travis-ci.org/github/amogh7joshi/chemsolve)
[![Latest Commit](https://img.shields.io/github/last-commit/amogh7joshi/chemsolve)](https://img.shields.io/github/last-commit/amogh7joshi/chemsolve)

Chemsolve is a library for solving and practicing chemistry problems.
It's made to have easy usability while still retaining a powerful engine
with functionality allowing it to tackle more complicated problems. It was 
designed as a tool for lower-level chemistry and problem solving as opposed 
to a materials science or higher-level chemistry library. 

## Installation

Chemsolve currently runs on Python 3.6 or higher. You can install it from PyPi via pip:

```shell script
pip install chemsolve
```

if you want to install it directly from this repository:
```shell script
git clone https://github.com/amogh7joshi/chemsolve.git
cd chemsolve
python setup.py install
```

Then execute:
```shell script
# Install system requirements.
python3 -m pip install -r requirements.txt 

# Try it out
cd tests
python3 elementtest.py
```

Chemsolve makes use of the [chempy](https://github.com/bjodah/chempy) library for backend stoichiometry calculations.

## Using Chemsolve

Chemsolve relies heavily on an object-based framework with classes representing important objects in chemistry: elements, compounds, reactions. 
The structure of Chemsolve is similar to the following:

![Classes](https://raw.githubusercontent.com/amogh7joshi/chemsolve/master/images/objects.png)

In addition, Chemsolve includes numerous features to ease chemistry calculations, available in the associated modules within 
Chemsolve, such as molarity and molality calculations in `chemsolve.solutions` and the ideal gas formula within 
`chemsolve.gases`. 

### Examples

Examples for all of the primary implemented structures can be found in `/examples`:
1. The [Element Class](https://github.com/amogh7joshi/chemsolve/blob/master/examples/element_example.ipynb) and usage.
2. The [Compound Class](https://github.com/amogh7joshi/chemsolve/blob/master/examples/compound_example.ipynb) and usage.
3. The [Reaction Class](https://github.com/amogh7joshi/chemsolve/blob/master/examples/reaction_example.ipynb) and usage. 

In this example, we will use the Reaction class.

Import the required module(s):

```python
from chemsolve import Compound, Reaction
```
Create the Necessary Object and its Object parameters:

```python
# Compounds which will be reacted.
r1 = Compound("NH3", grams = 5.00)
r2 = Compound("O2", grams = 3.46)
p1 = Compound("NO2")
p2 = Compound("H2O")
reaction = Reaction(r1, r2, "-->", p1, p2)
```

From here, you can access the object's attributes.

```python
print(reaction.balanced_reaction)
print(reaction.limiting_reactant)
```

*For further reference, please visit `/examples`.* 

## License

All code in this library is available under the [MIT License](../blob/master/LICENSE). You are welcome
to download the repository on your own and work with it, however. 

## Issues

If you notice an issues or bugs with the library, please feel free to create an issue. 
Make sure to follow the issue guidelines.

## Contributions

Contributions are always welcome, and feel free to contribute to the library. 
Please make sure to follow the pull request guidelines.




