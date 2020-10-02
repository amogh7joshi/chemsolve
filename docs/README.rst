# Chemsolve

[![PyPI version](https://badge.fury.io/py/chemsolve.svg)](https://badge.fury.io/py/chemsolve)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
cd ml
python setup.py install
```

Then execute:
```python
# Install system requirements.
python3 -m pip install -r requirements.txt
```

Chemsolve uses the chempy and periodictable libraries.
## Using Chemsolve

Chemsolve relies heavily on class framework with classes representing chemical objects: elements, compounds, reactions.

![Classes | 50%](images/objects.png)

### Examples

Examples for all of the implemented structures can be found in `/examples`.
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

All code in this library is avaliable under the [MIT License](../blob/master/LICENSE).

## Contributions

Contributions are always welcome, and feel free to contribute to the library.
Please make sure to follow the pull request guidelines.




