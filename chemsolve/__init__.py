import warnings
warnings.filterwarnings("ignore")
import logging
logging.basicConfig(format = '%(levelname)s - %(name)s: %(message)s')

from .element import *
from .compound import *
from .compound import *
from .reaction import *

# Removed Quantum for the time being.
# from .quantum.photoelectric import energy_change, level_transition

from .solutions.molar import molarity

from .utils.constants import *
