from __future__ import annotations

from pint import UnitRegistry

ureg = UnitRegistry(on_redefinition="ignore")
Q_ = ureg.Quantity

ureg.define("Sverdrup = 1e6 * meter **3 / second = Sv = Sverdrups")
ureg.define("Mol = 1 * mol / liter = M")
ureg.define("fraction = [] = frac")
ureg.define("percent = 1e-2 frac = pct")
ureg.define("permil = 1e-3 fraction")
ureg.define("ppm = 1e-6 fraction")

import numpy as np
np.seterr(invalid='ignore')

from .esbmtk import *
from .extended_classes import *
from .connections import ConnectionGroup, Connection, Connect, AirSeaExchange
from .utility_functions import *
from .sealevel import *
from .solver import *
