Chemsolve
=========

|PyPI version| |Downloads| |License: MIT| |Travis (.com)|

Chemsolve is a library for solving and practicing chemistry problems.
It's made to have easy usability while still retaining a powerful engine
with functionality allowing it to tackle more complicated problems. It
was designed as a tool for lower-level chemistry and problem solving as
opposed to a materials science or higher-level chemistry library.

Installation
------------

Chemsolve currently runs on Python 3.6 or higher. You can install it
from PyPi via pip:

.. code:: shell

    pip install chemsolve

if you want to install it directly from this repository:

.. code:: shell

    git clone https://github.com/amogh7joshi/chemsolve.git
    cd chemsolve
    python setup.py install

Then execute:

.. code:: shell

    # Install system requirements.
    python3 -m pip install -r requirements.txt

    # Try it out
    cd tests
    python3 elementtest.py

Chemsolve uses the chempy and periodictable libraries.

Using Chemsolve
~~~~~~~~~~~~~~~

Chemsolve relies heavily on class framework with classes representing
chemical objects: elements, compounds, reactions.

.. figure:: images/objects.png
   :alt: Classes

   Classes

Examples
~~~~~~~~

Examples for all of the implemented structures can be found in
``/examples``. In this example, we will use the Reaction class.

Import the required module(s):

.. code:: python

    from chemsolve import Compound, Reaction

Create the Necessary Object and its Object parameters:

.. code:: python

    # Compounds which will be reacted.
    r1 = Compound("NH3", grams = 5.00)
    r2 = Compound("O2", grams = 3.46)
    p1 = Compound("NO2")
    p2 = Compound("H2O")
    reaction = Reaction(r1, r2, "-->", p1, p2)

From here, you can access the object's attributes.

.. code:: python

    print(reaction.balanced_reaction)
    print(reaction.limiting_reactant)

*For further reference, please visit ``/examples``.*

License
-------

All code in this library is avaliable under the `MIT
License <../blob/master/LICENSE>`__.

Contributions
-------------

Contributions are always welcome, and feel free to contribute to the
library. Please make sure to follow the pull request guidelines.

.. |PyPI version| image:: https://badge.fury.io/py/chemsolve.svg
   :target: https://badge.fury.io/py/chemsolve
.. |Downloads| image:: https://pepy.tech/badge/chemsolve
   :target: https://pepy.tech/project/chemsolve
.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
.. |Travis (.com)| image:: https://img.shields.io/travis/com/amogh7joshi/chemsolve
