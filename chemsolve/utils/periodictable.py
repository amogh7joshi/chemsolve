import os

import pandas as pd
import numpy as np

directory, filename = os.path.split(__file__)
PATH = os.path.join(directory, "assets", "PT_complete.csv")

class PeriodicTable(pd.DataFrame):
   def __init__(self):
      super().__init__(pd.read_csv(PATH))
      pd.set_option("display.max_rows", None, "display.max_columns", None)

   def get_properties(self, symbol):
      properties = np.array(self.iloc[[self.index[self['Symbol'] == symbol].tolist()[0]]]).ravel()
      elements = list(self)
      return dict(zip(elements, properties))


