#!/usr/bin/env python3
# -*- coding = utf-8 -*-
import os

import numpy as np
import pandas as pd

from chemsolve.utils.errors import InvalidElementError

# Create the path to the periodic table.
pt_path = os.path.join(os.path.dirname(__file__), "assets", "PT_complete.csv")

class PeriodicTable(pd.DataFrame):
   """A DataFrame containing the periodic table, and information about elements."""
   def __init__(self):
      super().__init__(pd.read_csv(pt_path))
      pd.set_option("display.max_rows", None, "display.max_columns", None)

   def get_properties(self, symbol):
      """Get the different properties of a specific element."""
      try:
         properties = np.array(
            self.iloc[[self.index[self['Symbol'] == symbol].tolist()[0]]]).ravel()
      except IndexError:
         raise InvalidElementError(symbol)
      elements = list(self)
      return dict(zip(elements, properties))


