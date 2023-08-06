"""
     esbmtk: A general purpose Earth Science box model toolkit
     Copyright (C), 2020 Ulrich G. Wortmann

     This program is free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.

     This program is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.

     You should have received a copy of the GNU General Public License
     along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from numbers import Number
from nptyping import NDArray, Float64
from typing import *
from numpy import array, set_printoptions, arange, zeros, interp, mean
from pandas import DataFrame
from copy import deepcopy, copy
import time
from time import process_time
from numba.typed import List
import numba
from numba.core import types as nbt

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import logging

import builtins
import os, psutil

from .utility_functions import (
    plot_object_data,
    show_data,
    plot_geometry,
    show_dict,
    gen_dict_entries,
    get_string_between_brackets,
    get_plot_layout,
    build_ct_dict,
)
from .solver import (
    get_imass,
    get_delta,
    get_l_mass,
    execute,
    execute_e,
)


class esbmtkBase(object):
    """The esbmtk base class template. This class handles keyword
    arguments, name registration and other common tasks

    Useful methods in this class:

    define required keywords in lrk dict:
       self.lrk: list = ["name"]

    define allowed type per keyword in lkk dict:
       self.lkk: Dict[str, any] = {
                                  "name": str,
                                  "model": Model,
                                  "salinity": (int, float), # int or float
                                  }

    define default values if none provided in lod dict
       self.lod: Dict[str, any] = {"salinity": 35.0}

    validate keyword input:
        self.__validateinput__(kwargs)

    add global defaults each esbmtk object should have, even if they are not set or used
        self.__global_defaults__()

    register all key/value pairs as instance variables
        self.__registerkeys__()

    register name in global name space. This is only necessary if you want to reference
    the instance by name from the console, otherwise use the normal python way (i.e.
    instance = class(keywords)
        self.__register_name__ ()

    """

    __slots__ = "__dict__"

    # from typing import Dict

    def __init__(self) -> None:
        raise NotImplementedError

    def __global_defaults__(self) -> None:
        """Initial variables which should be present in every object
        Note that this is executed before we register the kwargs as instance
        variables

        """

        self.lmo: list = []
        self.lmo2: list = []
        self.ldo: list = ["full_name", "register", "groupname", "ctype"]

        for n in self.ldo:
            if n not in self.kwargs:
                self.kwargs[n] = "None"
                # logging.debug(
                #    f"set {self.kwargs['name']} self.kwargs[{n}] to {self.kwargs[n]}"
                # )

    def __validateandregister__(self, kwargs: dict) -> None:
        """Validate the user provided input key-value pairs. For this we need
        kwargs = dictionary with the user provided key-value pairs
        self.lkk = dictionary with allowed keys and type
        self.lrk = list of mandatory keywords
        self.lod = dictionary of default values for keys

        and register the instance variables and the instance in the global name space

        """

        # validate input
        self.__validateinput__(kwargs)

        # add global key-value pairs which should be present in each object
        self.__global_defaults__()

        # register all key/value pairs as instance variables
        self.__registerkeys__()

    def __register_name__(self) -> None:
        """
        Register object name in global name space, and test if
        name is unique

        There are two possible cases: This is a regular object, which will be registered
        in the global namespace (self.register is not set).

        Case B) This object should be registered in the local namespace of a group. In which case
        self.register should be set to the group object.

        """

        # we use this to suppress the echo during object creation
        self.reg_time = time.monotonic()

        # if self register is set, it points to the group object which contains
        # this sub object.

        logging.debug(f"self.register = {self.register}")

        # models are either in the global namespace, or do not get registered at all
        if isinstance(self, Model):
            if self.register == "None":
                setattr(builtins, self.name, self)
            else:
                pass

        # all other objects can be either part of another esbmtk object
        # register=object reference
        # or be registered globally
        else:
            # get model registry
            if isinstance(self.register, Model):
                reg = self.register
            elif isinstance(self.register, str):
                reg = self.mo
            else:
                reg = self.register.mo

            # checl model default
            if self.register == "None":  # global registration
                setattr(builtins, self.name, self)
                self.full_name = self.name

                # check for naming conflicts
                if self.full_name in reg.lmo:
                    raise NameError(f"{self.full_name} is a duplicate name. Please fix")
                else:
                    # register with model
                    reg.lmo.append(self.full_name)
                    reg.lmo2.append(self)
                    reg.dmo.update({self.full_name: self})

            else:  # local registration
                # get full_name of parent object
                if self.register.full_name != "None":
                    fn: str = f"{self.register.full_name}.{self.name}"
                else:
                    fn: str = f"{self.register.name}.{self.name}"

                self.full_name = fn
                setattr(self.register, self.name, self)
                # register with model
                reg.lmo.append(self.full_name)
                reg.dmo.update({self.full_name: self})

        # add fullname to kwargs so it shows up in __repr__
        # its a dirty hack though
        self.provided_kwargs["full_name"] = self.full_name
        logging.info(self.__repr__(1))

    def __validateinput__(self, kwargs: dict) -> None:
        """Validate the user provided input key-value pairs. For this we need
        kwargs = dictionary with the user provided key-value pairs
        self.lkk = dictionary with allowed keys and type
        self.lrk = list of mandatory keywords
        self.lod = dictionary of default values for keys

        """

        self.kwargs = kwargs  # store the kwargs
        self.provided_kwargs = kwargs.copy()  # preserve a copy

        if not hasattr(self, "lkk"):
            self.lkk: dict = {}
        if not hasattr(self, "lrk"):
            self.lrk: list = []
        if not hasattr(self, "lod"):
            self.lod: dict = []
        if not hasattr(self, "drn"):
            self.drn: dict = []

        # check that mandatory keys are present
        # and that all keys are allowed
        self.__checkkeys__()

        # initialize missing parameters

        self.kwargs = self.__addmissingdefaults__(self.lod, kwargs)

        # check if key values are of correct type
        self.__checktypes__(self.lkk, self.kwargs)

    def __checktypes__(self, av: Dict[any, any], pv: Dict[any, any]) -> None:
        """this method will use the the dict key in the user provided
        key value data (pv) to look up the allowed data type for this key in av

        av = dictinory with the allowed input keys and their type
        pv = dictionary with the user provided key-value data
        """

        k: any
        v: any

        # loop over known keywords in av
        for k, v in av.items():
            if k in pv:  # check type of k
                # check if entry matches required type
                if v != any:
                    # print()
                    if not isinstance(pv[k], v):
                        raise TypeError(
                            f"{type(pv[k])} is the wrong type for '{k}', should be '{av[k]}'"
                        )

        # loop over provided keywords
        # for k, v in pv.items():
        #     # check av if provided value v is of correct type
        #     if av[k] != any:
        #         # print(f"key = {k}, value  = {v}")
        #         if not isinstance(v, av[k]):
        #             # print(f"k={k}, v= {v}, av[k] = {av[k]}")
        #             raise TypeError(
        #                 f"{type(v)} is the wrong type for '{k}', should be '{av[k]}'"
        #             )

    def __initerrormessages__(self):
        """Init the list of known error messages"""
        self.bem: dict = {
            "Number": "a number",
            "Model": "a model handle (i.e. the name without quotation marks)",
            "Element": "an element handle (i.e. the name without quotation marks)",
            "Species": "a species handle (i.e. the name without quotation marks)",
            "Flux": "a flux handle (i.e. the name without quotation marks)",
            "Reservoir": "a reservoir handle (i.e. the name without quotation marks)",
            "Signal": "a signal handle (i.e. the name without quotation marks)",
            "Process": "a process handle (i.e. the name without quotation marks)",
            "Unit": "a string",
            "File": "a filename inb the local directory",
            "Legend": " a string",
            "Source": " a string",
            "Sink": " a string",
            "Ref": " a Flux reference",
            "Alpha": " a Number",
            "Delta": " a Number",
            "Scale": " a Number",
            "Ratio": " a Number",
            "number": "a number",
            "model": "a model handle (i.e. the name without quotation marks)",
            "element": "an element handle (i.e. the name without quotation marks)",
            "species": "a species handle (i.e. the name without quotation marks)",
            "flux": "a flux handle (i.e. the name without quotation marks)",
            "reservoir": "a reservoir handle (i.e. the name without quotation marks)",
            "signal": "a signal handle (i.e. the name without quotation marks)",
            "Process": "a process handle (i.e. the name without quotation marks)",
            "unit": "a string",
            "file": "a filename inb the local directory",
            "legend": " a string",
            "source": " a string",
            "sink": " a string",
            "ref": " a Flux reference",
            "alpha": " a Number",
            "delta": " a Number",
            "scale": "a Number",
            "ratio": "a Number",
            "concentration": "a Number",
            "pl": " a list with one or more process handles",
            "react_with": "a Flux handle",
            "data": "External Data Object",
            "register": "esbmtk object",
            str: "a string with quotation marks",
        }

    def __registerkeys__(self) -> None:
        """register the kwargs key/value pairs as instance variables
        and complain about unknown keywords"""
        k: any  # dict keys
        v: any  # dict values

        # need list of replacement values
        # "alpha" : _alpha

        for k, v in self.kwargs.items():
            # check wheather the variable name needs to be replaced
            if k in self.drn:
                k = self.drn[k]
            setattr(self, k, v)

    def __checkkeys__(self) -> None:
        """check if the mandatory keys are present"""

        k: str
        v: any
        # test if the required keywords are given
        for k in self.lrk:  # loop over required keywords
            if isinstance(k, list):  # If keyword is a list
                s: int = 0  # loop over allowed substitutions
                for e in k:  # test how many matches are in this list
                    if e in self.kwargs:
                        # print(self.kwargs[e])
                        if not isinstance(e, (np.ndarray, np.float64, list)):
                            # print (type(self.kwargs[e]))
                            if self.kwargs[e] != "None":
                                s = s + 1
                if s > 1:  # if more than one match
                    raise ValueError(
                        f"You need to specify exactly one from this list: {k}"
                    )

            else:  # keyword is not a list
                if k not in self.kwargs:
                    raise ValueError(f"You need to specify a value for {k}")

        tl: List[str] = []
        # get a list of all known keywords
        for k, v in self.lkk.items():
            tl.append(k)

        # test if we know all keys
        # for k, v in self.kwargs.items():
        #     if k not in self.lkk:
        #         raise ValueError(f"{k} is not a valid keyword. \n Try any of \n {tl}\n")

    def __addmissingdefaults__(self, lod: dict, kwargs: dict) -> dict:
        """
        test if the keys in lod exist in kwargs, otherwise add them with the default values
        from lod

        """
        new: dict = {}
        if len(self.lod) > 0:
            for k, v in lod.items():
                if k not in kwargs:
                    new.update({k: v})

        kwargs.update(new)
        return kwargs

    def __repr__(self, log=0) -> str:
        """Print the basic parameters for this class when called via the print method"""
        from esbmtk import Q_

        m: str = ""

        # suppress output during object initialization
        tdiff = time.monotonic() - self.reg_time

        # do not echo input unless explicitly requestted

        m = f"{self.__class__.__name__}(\n"
        for k, v in self.provided_kwargs.items():
            if not isinstance({k}, esbmtkBase):
                # check if this is not another esbmtk object
                if "esbmtk" in str(type(v)):
                    m = m + f"    {k} = {v.name},\n"
                # if this is a string
                elif isinstance(v, str):
                    m = m + f"    {k} = '{v}',\n"
                # if this is a quantity
                elif isinstance(v, Q_):
                    m = m + f"    {k} = '{v}',\n"
                # if this is a list
                elif isinstance(v, (list, np.ndarray)):
                    m = m + f"    {k} = '{v[0:3]}',\n"
                # all other cases
                else:
                    m = m + f"    {k} = {v},\n"

        m = m + ")"

        if log == 0 and tdiff < 1:
            m = ""

        return m

    def __str__(self, kwargs={}):
        """Print the basic parameters for this class when called via the print method
        Optional arguments

        indent :int = 0 printing offset

        """
        from esbmtk import Q_

        m: str = ""
        off: str = "  "

        if "indent" in kwargs:
            ind: str = kwargs["indent"] * " "
        else:
            ind: str = ""

        if "index" in kwargs:
            index = int(kwargs["index"])
        else:
            index = -2

        m = f"{ind}{self.name} ({self.__class__.__name__})\n"
        for k, v in self.provided_kwargs.items():
            if not isinstance({k}, esbmtkBase):
                # check if this is not another esbmtk object
                if "esbmtk" in str(type(v)):
                    pass
                elif isinstance(v, str) and not (k == "name"):
                    m = m + f"{ind}{off}{k} = {v}\n"
                elif isinstance(v, Q_):
                    m = m + f"{ind}{off}{k} = {v}\n"
                elif isinstance(v, np.ndarray):
                    m = m + f"{ind}{off}{k}[{index}] = {v[index]:.2e}\n"
                elif k != "name":
                    m = m + f"{ind}{off}{k} = {v}\n"

        return m

    def __lt__(self, other) -> None:
        """This is needed for sorting with sorted()"""

        return self.n < other.n

    def __gt__(self, other) -> None:
        """This is needed for sorting with sorted()"""

        return self.n > other.n

    def info(self, **kwargs) -> None:
        """Show an overview of the object properties.
        Optional arguments are

        indent :int = 0 indentation

        """

        if "indent" not in kwargs:
            indent = 0
            ind = ""
        else:
            indent = kwargs["indent"]
            ind = " " * indent

        # print basic data bout this object
        print(f"{ind}{self.__str__(kwargs)}")

    def __aux_inits__(self) -> None:
        """Aux initialization code. Not normally used"""

        pass


class Model(esbmtkBase):
    """This class is used to specify a new model

    Example:

          esbmtkModel(name   =  "Test_Model",
                      start    = "0 yrs",    # optional: start time
                      stop     = "1000 yrs", # end time
                      timestep = "2 yrs",    # as a string "2 yrs"
                      offset = "0 yrs",    # optional: time offset for plot
                      mass_unit = "mol",   #required
                      volume_unit = "l", #required
                      time_label = optional, defaults to "Time"
                      display_precision = optional, defaults to 0.01,
                      m_type = "mass_only/both"
                      plot_style = 'default', optional defaults to 'default'
                      number_of_datapoints = optional, see below
                      step_limit = optional, see below
                      register = 'local', see below
                      save_flux_data = False, see below
                    )

    ref_time:  will offset the time axis by the specified
                 amount, when plotting the data, .i.e., the model time runs from to
                 100, but you want to plot data as if where from 2000 to 2100, you would
                 specify a value of 2000. This is for display purposes only, and does not affect
                 the model. Care must be taken that any external data references the model
                 time domain, and not the display time.

    display precision: affects the on-screen display of data. It is
                       also cutoff for the graphicak output. I.e., the interval f the y-axis will not be
                       smaller than the display_precision.

    m_type: enables or disables isotope calculation for the entire model.
            The default value  is "Not set" in this case isotopes will only be calculated for
            reservoirs which set the isotope keyword. 'mass_only' 'both' will override
            the reservoir settings

    register = local/None. If set to 'None' all objects are registered
               in the global namespace the default setting is local,
               i.e. all objects are registered in the model namespace.

    save_flux_data: Normally, flux data is not stored. Set this to True
               for debugging puposes. Note, Fluxes with signals are always
               stored. You can also enable this option for inidividual
               connections (fluxes).

    get_delta_values: Compute delta values as postprocessing step.

    All of the above keyword values are available as variables with
    Model_Name.keyword

    The user facing methods of the model class are
       - Model_Name.info()
       - Model_Name.save_data()
       - Model_Name.plot_data()
       - Model_Name.plot_reservoirs() takes an optional filename as argument
       - Model_Name.plot([sb.DIC, sb.TA]) plot any object in the list
       - Model_Name.save_state() Save the model state
       - Model_name.read_state() Initialize with a previous model state
       - Model_Name.run(), there are 2 optional arguments here, solver="hybrid"
         and solver = "numba". Both involve a 3 to 5 second overhead. The hybrid
         solver is compatible with all connection types, and about 3 times faster
         than the  regular solver. The numba solver is about 10 faster, but currently
         only supports a limited set of connection types.
       - Model_Name.list_species()
       - Model_name.flux_summary()
       - Model_Name.connection_summary()


    User facing variable are Model_Name.time which contains the time
    axis.

    Optional, you can provide the element keyword which will setup a
    default set of Species for Carbon and Sulfur. In this case, there
    is no need to define elements or species. The argument to this
    keyword are either "Carbon", or "Sulfur" or both as a list
    ["Carbon", "Sulfur"].


    Dealing with large datasets:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    1) Limiting the size of the data which is being saved with save_data()

         number_of_datapoints = 100 will only write every nth data point to file.
                                where n = timesteps/ number_of_datapoints

         this defaults to 1000 until set explicitly.

    2) Reducing the memory footprint

    Models with a long runtime can easily exceed the available
    computer memory, as much if it is goobled up storing the model
    results. In this case, one can set the optional parameter

       step_limit = 1E6

    The above will limit the total number of iterations to 1E6, then
    save the data up to this point, and then restart the
    model. Subsequent results will be appended to the results.

    Caveat Emptor: If your model uses a signal instance, all signal
    data must fit into a single iteration set. At present, there is no
    support for signals which extend beyond the step_limit.

    In order to prevent the creation of massive datafiles, number_of_datapoints
    defaults to 1000. Modify as needed.

    """

    __slots__ = "lor"

    def __init__(self, **kwargs: Dict[any, any]) -> None:
        """Init Sequence"""

        from . import ureg, Q_

        # provide a dict of all known keywords and their type
        self.lkk: Dict[str, any] = {
            "name": str,
            "start": str,
            "stop": str,
            "timestep": str,
            "offset": str,
            "element": (str, list),
            "mass_unit": str,
            "volume_unit": str,
            "time_label": str,
            "display_precision": float,
            "m_type": str,
            "plot_style": str,
            "number_of_datapoints": int,
            "step_limit": (Number, str),
            "register": str,
            "full_name": str,
            "save_flux_data": bool,
        }

        # provide a list of absolutely required keywords
        self.lrk: list[str] = ["name", "stop", "timestep", "mass_unit", "volume_unit"]

        # list of default values if none provided
        self.lod: Dict[str, any] = {
            "start": "0 years",
            "offset": "0 years",
            "time_label": "Time",
            "display_precision": 0.01,
            "m_type": "Not Set",
            "plot_style": "default",
            "number_of_datapoints": 1000,
            "step_limit": "None",
            "register": "local",
            "full_name": kwargs["name"],
            "save_flux_data": False,
        }

        self.__initerrormessages__()
        self.bem.update(
            {
                "offset": "a string",
                "timesetp": "a string",
                "element": "element name or list of names",
                "mass_unit": "a string",
                "volume_unit": "a string",
                "time_label": "a string",
                "display_precision": "a number",
                "m_type": "a string",
                "plot_style": "a string",
            }
        )

        self.__validateandregister__(kwargs)  # initialize keyword values

        # empty list which will hold all reservoir references
        self.dmo: dict = {}  # dict of all model objects. useful for name lookups
        self.lor: list = []
        # empty list which will hold all connector references
        self.loc: set = set()  # set with connection handles
        self.lel: list = []  # list which will hold all element references
        self.lsp: list = []  # list which will hold all species references
        self.lop: list = []  # set of flux processes
        self.lpc_f: list = []  # list of external functions affecting fluxes
        # list of external functions affecting virtual reservoirs
        self.lpc_r: list = []
        # list of virtual reservoirs
        self.lvr: list = []
        # optional keywords for use in the connector class
        self.olkk: list = []
        # list of objects which require a delayed initialize
        self.lto: list = []
        # list of datafield objects
        self.ldf: list = []
        # list of signals
        self.los: list = []
        self.first_start = True  # keep track of repeated solver calls
        self.lof: list = []  # list of fluxes
        self.debug: bool = False

        # Parse the strings which contain unit information and convert
        # into model base units For this we setup 3 variables which define
        self.l_unit = ureg.meter  # the length unit
        self.t_unit = Q_(self.timestep).units  # the time unit
        self.d_unit = Q_(self.stop).units  # display time units
        self.m_unit = Q_(self.mass_unit).units  # the mass unit
        self.v_unit = Q_(self.volume_unit).units  # the volume unit
        # the concentration unit (mass/volume)
        self.c_unit = self.m_unit / self.v_unit  # concentration
        u1 = Q_("mol/liter").units
        u2 = Q_("mol/kg").units
        if self.c_unit != u1 and self.c_unit != u2:
            raise ValueError(f"units must be {u1} or {u2}, not {self.c_unit}")

        self.f_unit = self.m_unit / self.t_unit  # the flux unit (mass/time)
        self.r_unit = self.v_unit / self.t_unit  # flux as volume/time
        # this is now defined in __init__.py
        # ureg.define('Sverdrup = 1e6 * meter **3 / second = Sv = Sverdrups')

        # legacy variable names
        self.start = Q_(self.start).to(self.t_unit).magnitude
        self.stop = Q_(self.stop).to(self.t_unit).magnitude
        self.offset = Q_(self.offset).to(self.t_unit).magnitude

        self.bu = self.t_unit
        self.base_unit = self.t_unit
        self.dt = Q_(self.timestep).magnitude
        self.tu = str(self.bu)  # needs to be a string
        self.n = self.name
        self.mo = self.name
        self.plot_style: list = [self.plot_style]

        self.xl = f"Time [{self.bu}]"  # time axis label
        self.length = int(abs(self.stop - self.start))
        self.steps = int(abs(round(self.length / self.dt)))

        if self.steps < self.number_of_datapoints:
            self.number_of_datapoints = self.steps

        self.time = (np.arange(self.steps) * self.dt) + self.start
        self.timec = np.empty(0)
        self.state = 0

        # calculate stride
        self.stride = int(self.steps / self.number_of_datapoints)
        self.reset_stride = self.stride

        if self.step_limit == "None":
            self.number_of_solving_iterations: int = 0
        elif self.step_limit > self.steps:
            self.number_of_solving_iterations: int = 0
            self.step_limit = "None"
        else:
            self.step_limit = int(self.step_limit)
            self.number_of_solving_iterations = int(round(self.steps / self.step_limit))
            self.reset_stride = int(round(self.steps / self.number_of_datapoints))
            self.steps = self.step_limit
            self.time = (arange(self.steps) * self.dt) + self.start

        # set_printoptions(precision=self.display_precision)

        if "element" in self.kwargs:
            if isinstance(self.kwargs["element"], list):
                element_list = self.kwargs["element"]
            else:
                element_list = [self.kwargs["element"]]

            for e in element_list:

                if e == "Carbon":
                    carbon(self)
                elif e == "Sulfur":
                    sulfur(self)
                elif e == "Hydrogen":
                    hydrogen(self)
                elif e == "Phosphor":
                    phosphor(self)
                elif e == "Oxygen":
                    oxygen(self)
                elif e == "Nitrogen":
                    nitrogen(self)
                elif e == "Boron":
                    boron(self)
                else:
                    raise ValueError(f"{e} not implemented yet")

        warranty = (
            f"\n"
            f"ESBMTK  Copyright (C) 2020  Ulrich G.Wortmann\n"
            f"This program comes with ABSOLUTELY NO WARRANTY\n"
            f"For details see the LICENSE file\n"
            f"This is free software, and you are welcome to redistribute it\n"
            f"under certain conditions; See the LICENSE file for details.\n"
        )
        print(warranty)

        # start a log file
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        fn: str = f"{kwargs['name']}.log"
        logging.basicConfig(filename=fn, filemode="w", level=logging.WARN)
        self.__register_name__()

        # initialize the hypsometry class
        hypsometry(name="hyp", model=self, register=self)

    def info(self, **kwargs) -> None:
        """Show an overview of the object properties.
        Optional arguments are
        index  :int = 0 this will show data at the given index
        indent :int = 0 indentation

        """
        off: str = "  "
        if "index" not in kwargs:
            index = 0
        else:
            index = kwargs["index"]

        if "indent" not in kwargs:
            indent = 0
            ind = ""
        else:
            indent = kwargs["indent"]
            ind = " " * indent

        # print basic data bout this object
        print(self)

        # list elements
        print("Currently defined elements and their species:")
        for e in self.lel:
            print(f"{ind}{e}")
            print(f"{off} Defined Species:")
            for s in e.lsp:
                print(f"{off}{off}{ind}{s.n}")

    def save_state(self) -> None:
        """Save model state. Similar to save data, but only saves the last 10
        time-steps

        """

        start: int = -10
        stop: int = -1
        stride: int = 1
        prefix: str = "state_"

        for r in self.lor:
            r.__write_data__(prefix, start, stop, stride, False, "state")

        for r in self.lvr:
            r.__write_data__(prefix, start, stop, stride, False, "state")

    def save_data(self, **kwargs) -> None:
        """Save the model results to a CSV file. Each reservoir will have
        their own CSV file

        Optional arguments:
        stride = int  # every nth element
        start = int   # start index
        stop = int    # end index
        append = True/False #

        """

        for k, v in kwargs.items():
            if not isinstance(v, int):
                print(f"{k} must be an integer number")
                raise ValueError(f"{k} must be an integer number")

        if "stride" in kwargs:
            stride = kwargs["stride"]
        else:
            stride = self.stride

        if "start" in kwargs:
            start = kwargs["start"]
        else:
            start = 0

        if "stop" in kwargs:
            stop = kwargs["stop"]
        else:
            stop = self.steps

        if "append" in kwargs:
            append = kwargs["append"]
        else:
            append = False

        prefix = ""
        # Save reservoir and flux data
        ##print("Writing reservoir data")
        print(f"start = {start}, stop = {stop}, stride={stride}, append ={append}")
        for r in self.lor:
            # print(f"R = {r.full_name}")
            # print(f"start = {start}, stop = {stop}, stride={stride}, append ={append}")
            r.__write_data__(prefix, start, stop, stride, append, "data")

        # save data fields
        # for r in self.ldf:
        #     r.__write_data__(prefix, start, stop, stride, append)
        print("Writing virtual reservoir data")
        for r in self.lvr:
            r.__write_data__(prefix, start, stop, stride, append, "data")
        print("done writing")

    def restart(self):
        """Restart the model with result of the last run.
        This is useful for long runs which otherwise would used
        to much memory

        """

        for r in self.lor:
            r.__reset_state__()
            for f in r.lof:
                f.__reset_state__()

        for r in self.lvr:
            r.__reset_state__()

        # print(f"len of time {len(self.time)}, stride = {self.stride}")
        # print(f"len of time with stride {len(self.time[0 : -2 : self.stride])}")
        self.timec = np.append(self.timec, self.time[0 : -2 : self.stride])
        t = int(round((self.stop - self.start) * self.dt))
        self.start = int(round((self.stop * self.dt)))
        self.stop = self.start + t
        self.time = (np.arange(self.steps) * self.dt) + self.start
        print(f"new start = {self.start}, new stop = {self.stop}")
        print(f"time[0] = {self.time[0]} time[-1] = {self.time[-1]}")
        # print(f"len of timec {len(self.timec)}")
        # self.time = (arange(self.steps) * self.dt) + self.start

    def read_state(self):
        """This will initialize the model with the result of a previous model
        run.  For this to work, you will need issue a
        Model.save_state() command at then end of a model run. This
        will create the necessary data files to initialize a
        subsequent model run.

        """
        for r in self.lor:
            if isinstance(r, (Reservoir, GasReservoir)):
                # print(f" reading from {r.full_name}")
                r.__read_state__("state")

        for r in self.lvr:
            # print(f"lvr  reading from {r.full_name}")
            r.__read_state__("state")

    def merge_temp_results(self):
        """Replace the datafields which were used for an individual iteration
        with the data we saved from the previous iterations

        """

        self.time = self.timec
        for r in self.lor:
            r.__merge_temp_results__()
            for f in r.lof:
                f.__merge_temp_results__()

        for r in self.lvr:
            r.__merge_temp_results__()

    def plot_data(self, **kwargs: dict) -> None:
        """
        Loop over all reservoirs and either plot the data into a
        window, or save it to a pdf

        """

        i = 0
        for r in self.lor:
            r.__plot__(i)
            i = i + 1

        fig.tight_layout()
        plt.show()  # create the plot windows

    def plot(self, l: list = [], **kwargs) -> None:
        """Plot all objects specified in list)

        M.plot([sb.PO4, sb.DIC],fn=test.pdf)

        fn is optional
        """
        if "fn" in kwargs:
            filename = kwargs["fn"]
        else:
            filename = f"{self.n}.pdf"

        noo: int = len(l)
        size, geo = plot_geometry(noo)  # adjust layout
        plt.style.use(self.plot_style)
        fig = plt.figure(0)  # Initialize a plot window
        fig.canvas.manager.set_window_title(f"{self.n} Reservoirs")
        fig.set_size_inches(size)

        i: int = 1
        for e in l:
            plot_object_data(geo, i, e)
            i = i + 1

        fig.subplots_adjust(top=0.88)
        fig.tight_layout()
        plt.show()  # create the plot windows
        fig.savefig(filename)

    def plot_reservoirs(self, **kwargs: dict) -> None:
        """Plot only Reservoir data

        you can further specify a different name for the plot
        fn = "foo.pdf"

        """

        # get number of plot objects
        i = 0
        # get number of signals
        for s in self.los:
            if s.plot == "yes":
                i = i + 1

        # get number of reservoirs
        for r in self.lor:
            if r.plot == "yes":
                i = i + 1

        # get number of virtual reservoirs
        for r in self.lvr:
            if r.plot == "yes":
                i = i + 1

        noo: int = len(self.ldf) + i
        size, geo = plot_geometry(noo)  # adjust layout

        if "fn" in kwargs:
            filename = kwargs["fn"]
        else:
            filename = f"{self.n}_Reservoirs.pdf"

        plt.style.use(self.plot_style)

        fig = plt.figure(0)  # Initialize a plot window
        fig.canvas.manager.set_window_title(f"{self.n} Reservoirs")
        fig.set_size_inches(size)

        i: int = 1

        for r in self.los:  # signals
            if r.plot == "yes":
                plot_object_data(geo, i, r)
                i = i + 1

        for r in self.lor:  # reservoirs
            if r.plot == "yes":
                plot_object_data(geo, i, r)
                i = i + 1

        for r in self.lvr:  # virtual reservoirs
            if r.plot == "yes":
                plot_object_data(geo, i, r)
                i = i + 1

        for r in self.ldf:  # datafields
            plot_object_data(geo, i, r)
            i = i + 1

        fig.tight_layout()
        plt.show()  # create the plot windows
        fig.subplots_adjust(top=0.88)
        fig.savefig(filename)

    def run(self, **kwargs) -> None:
        """Loop over the time vector, and for each time step, calculate the
        fluxes for each reservoir
        """

        # this has nothing todo with self.time below!
        wts = time.time()
        start: float = process_time()
        new: [NDArray, Float] = zeros(4)

        # put direction dictionary into a list
        for r in self.lor:  # loop over reservoirs
            r.lodir = []
            for f in r.lof:  # loop over fluxes
                a = r.lio[f]
                r.lodir.append(a)

        # take care of objects which require a delayed init
        for o in self.lto:
            o.__delayed_init__()

        if "solver" not in kwargs:
            solver = "python"
        else:
            solver = kwargs["solver"]

        if self.number_of_solving_iterations > 0:

            for i in range(self.number_of_solving_iterations):
                print(
                    f"\n Iteration {i+1} out of {self.number_of_solving_iterations}\n"
                )
                self.__run_solver__(solver, new)

                print(f"Restarting model")
                self.restart()

            duration: float = process_time() - start
            wcd = time.time() - wts
            print(f"\n Execution took {duration} cpu seconds, wt = {wcd}\n")
            print("Merge results")
            self.merge_temp_results()
            self.steps = self.number_of_datapoints
            # after merging, the model steps = number_of_datapoints
        # print("Saving data")
        # self.save_data(start=0, stop=self.number_of_datapoints, stride=1)
        # print("Done Saving")
        else:
            self.__run_solver__(solver, new)

        # flag that the model has executed
        self.state = 1

        process = psutil.Process(os.getpid())
        print(f"This run used {process.memory_info().rss/1e9:.2f} Gbytes of memory \n")

    def get_delta_values(self):
        """Calculate the isotope ratios in the usual delta notation"""

        for r in self.lor:
            if r.isotopes:
                r.d = get_delta_h(r)

        # for vr in self.lvr:
        #     vr.d = get_delta_h(vr)

        for f in self.lof:
            if f.save_flux_data:
                f.d = get_delta_h(f)

    def sub_sample_data(self):
        """Subsample the data. No need to save 100k lines of data You need to
        do this _after_ saving the state, but before plotting and
        saving the data

        """

        for r in self.lor:
            r.__sub_sample_data__()

        for vr in self.lvr:
            vr.__sub_sample_data__()

        for f in self.lof:
            f.__sub_sample_data__()

        stride = int(len(self.time) / self.number_of_datapoints)
        self.time = self.time[2:-2:stride]

    def __run_solver__(self, solver, new) -> None:

        if solver == "numba":
            execute_e(
                self,
                new,
                self.lop,
                self.lor,
                self.lpc_f,
                self.lpc_r,
            )
        else:
            execute(new, self.time, self.lop, self.lor, self.lpc_f, self.lpc_r)

    def __step_process__(self, r, i) -> None:
        """For debugging. Provide reservoir and step number,"""
        for p in r.lop:  # loop over reservoir processes
            print(f"{p.n}")
            p(r, i)  # update fluxes

    def __step_update_reservoir__(self, r, i) -> None:
        """For debugging. Provide reservoir and step number,"""
        flux_list = r.lof
        # new = sum_fluxes(flux_list,r,i) # integrate all fluxes in self.lof

        ms = ls = hs = 0
        for f in flux_list:  # do sum of fluxes in this reservoir
            direction = r.lio[f]
            ms = ms + f.m[i] * direction  # current flux and direction
            ls = ls + f.l[i] * direction  # current flux and direction
            hs = hs + f.h[i] * direction  # current flux and direction

        new = array([ms, ls, hs])
        new = new * r.mo.dt  # get flux / timestep
        new = new + r[i - 1]  # add to data from last time step
        # new = new * (new > 0)  # set negative values to zero
        r[i] = new  # update reservoir data

    def list_species(self):
        """List all  defined species."""
        for e in self.lel:
            print(f"{e.n}")
            e.list_species()

    def flux_summary(self, **kwargs: dict) -> tuple:
        """Show a summary of all model fluxes

        Optional parameters:

        index :int = i > 1 and i < number of timesteps -1
        filter_by :str = filter on flux name or part of flux name
        exclude :str = None
        return: bool = True

        returns the sum of the fluxes, and a list
        fluxes matching the filter_by string

        Example:

        sum, names = M.flux_summary(filter_by="POP", return_list=True)

        """

        rl: list = []

        if "index" in kwargs:
            i: int = kwargs["index"]
        else:
            i: int = -3

        if "filter_by" in kwargs:
            fby: str = kwargs["filter_by"]
        else:
            fby: str = ""

        if "exclude" in kwargs:
            ex: str = kwargs["exclude"]
            do_ex: bool = True
        else:
            do_ex: bool = False
            ex = ""

        if "filter" in kwargs:
            raise ValueError("use filter_by instead of filter")

        if "return_list" in kwargs:
            return_list = True
        else:
            return_list = False
            print(f"\n --- Flux Summary -- filtered by {fby}\n")

        for f in self.lof:  # loop over flux list
            if fby in f.full_name:  # match on fby
                # print(f"{fby} in {f.full_name}")
                if do_ex:  # exclude argument present
                    # print("do_ex = True")
                    if ex in f.full_name:  # exclude if string matches
                        # print(f"found {ex} in {f.full_name}")
                        continue
                    else:  # otherwise append
                        rl.append(f)
                        if not return_list:
                            print(f"{f.full_name}")
                else:
                    rl.append(f)
                    if not return_list:
                        print(f"{f.full_name}")

        if not return_list:
            rl = None

        return rl

    def connection_summary(self, **kwargs: dict) -> None:
        """Show a summary of all connections

        Optional parameters:

        filter_by :str = filter on flux name or part of flux name

        """

        if "filter_by" in kwargs:
            fby: str = kwargs["filter_by"]
        else:
            fby: str = ""

        if "filter" in kwargs:
            raise ValueError("use filter_by instead of filter")

        self.cg_list: list = []
        # extract all connection groups. Note that loc contains all conections
        # i.e., not connection groups.
        for c in list(self.loc):
            # if "." in c.full_name:
            # if c.register not in self.cg_list and c.register != "None":
            if c not in self.cg_list and c.register != "None":
                self.cg_list.append(c)
            else:  # this is a regular connnection
                self.cg_list.append(c)

        print(f"\n --- Connection Group Summary -- filtered by {fby}\n")
        print(f"       run the following command to see more details:\n")

        for c in self.cg_list:
            if fby in c.full_name:
                print(f"{c.full_name}.info()")

        print("")

    def clear(self):
        """delete all model objects"""

        import builtins

        for o in self.lmo:
            print(f"deleting {o}")
            del __builtins__[o]


class Element(esbmtkBase):
    """Each model, can have one or more elements.  This class sets
    element specific properties

    Example::

            Element(name      = "S "           # the element name
                    model     = Test_model     # the model handle
                    mass_unit =  "mol",        # base mass unit
                    li_label  =  "$^{32$S",    # Label of light isotope
                    hi_label  =  "$^{34}S",    # Label of heavy isotope
                    d_label   =  r"$\delta^{34}$S",  # Label for delta value
                    d_scale   =  "VCDT",       # Isotope scale
                    r         = 0.044162589,   # isotopic abundance ratio for element
                  )

    """

    # set element properties
    def __init__(self, **kwargs) -> any:
        """Initialize all instance variables"""

        # provide a dict of known keywords and types
        self.lkk = {
            "name": str,
            "model": Model,
            "mass_unit": str,
            "li_label": str,
            "hi_label": str,
            "d_label": str,
            "d_scale": str,
            "r": Number,
            "full_name": str,
            "register": any,
        }

        # provide a list of absolutely required keywords
        self.lrk: list = ["name", "model", "mass_unit"]
        # list of default values if none provided
        self.lod = {
            "li_label": "None",
            "hi_label": "None",
            "d_label": "None",
            "d_scale": "None",
            "r": 1,
            "full_name": "None",
            "register": "None",
        }

        self.__initerrormessages__()
        self.__validateandregister__(kwargs)  # initialize keyword values

        # legacy name aliases
        self.n: str = self.name  # display name of species
        self.mo: Model = self.model  # model handle
        self.mu: str = self.mass_unit  # display name of mass unit
        self.ln: str = self.li_label  # display name of light isotope
        self.hn: str = self.hi_label  # display name of heavy isotope
        self.dn: str = self.d_label  # display string for delta
        self.ds: str = self.d_scale  # display string for delta scale
        self.lsp: list = []  # list of species for this element.
        self.mo.lel.append(self)

        if self.mo.register == "local" and self.register == "None":
            self.register = self.mo

        self.__register_name__()

    def list_species(self) -> None:
        """List all species which are predefined for this element"""

        for e in self.lsp:
            print(e.n)


class Species(esbmtkBase):
    """Each model, can have one or more species.  This class sets species
    specific properties

          Example::

                Species(name = "SO4",
                        element = S,
    )

    """

    __slots__ = "r"

    # set species properties
    def __init__(self, **kwargs) -> None:
        """Initialize all instance variables"""

        # provide a list of all known keywords
        self.lkk: Dict[any, any] = {
            "name": str,
            "element": Element,
            "display_as": str,
            "m_weight": Number,
            "register": any,
        }

        # provide a list of absolutely required keywords
        self.lrk = ["name", "element"]

        # list of default values if none provided
        self.lod = {
            "display_as": kwargs["name"],
            "m_weight": 0,
            "register": "None",
        }

        self.__initerrormessages__()

        self.__validateandregister__(kwargs)  # initialize keyword values

        if not "display_as" in kwargs:
            self.display_as = self.name

        # legacy names
        self.n = self.name  # display name of species
        self.mu = self.element.mu  # display name of mass unit
        self.ln = self.element.ln  # display name of light isotope
        self.hn = self.element.hn  # display name of heavy isotope
        self.dn = self.element.dn  # display string for delta
        self.ds = self.element.ds  # display string for delta scale
        self.r = self.element.r  # ratio of isotope standard
        self.mo = self.element.mo  # model handle
        self.eh = self.element.n  # element name
        self.e = self.element  # element handle
        self.dsa = self.display_as  # the display string.

        # self.mo.lsp.append(self)   # register self on the list of model objects
        self.e.lsp.append(self)  # register this species with the element

        if self.mo.register == "local" and self.register == "None":
            self.register = self.mo
        self.__register_name__()


class ReservoirBase(esbmtkBase):
    """Base class for all Reservoir objects"""

    __slots__ = ("m", "l", "h", "d", "c", "lio", "rvalue", "lodir", "lof", "lpc")

    def __init__(self, **kwargs) -> None:

        raise NotImplementedError(
            "ReservoirBase should never be used. Use the derived classes"
        )

    def __set_legacy_names__(self, kwargs) -> None:
        """
        Move the below out of the way
        """

        self.lof: list[Flux] = []  # flux references
        self.led: list[ExternalData] = []  # all external data references
        self.lio: dict[str, int] = {}  # flux name:direction pairs
        self.lop: list[Process] = []  # list holding all processe references
        self.loe: list[Element] = []  # list of elements in thiis reservoir
        self.doe: Dict[Species, Flux] = {}  # species flux pairs
        self.loc: set[Connection] = set()  # set of connection objects
        self.ldf: list[DataField] = []  # list of datafield objects
        # list of processes which calculate reservoirs
        self.lpc: list[Process] = []

        # legacy names
        self.n: str = self.name  # name of reservoir
        # if "register" in self.kwargs:
        if self.register == "None":
            self.pt = self.name
        else:
            self.pt: str = f"{self.register.name}_{self.n}"
            self.groupname = self.register.name
            self.full_name = f"{self.register.name}.{self.n}"
        # else:
        #   self.pt = self.name

        self.sp: Species = self.species  # species handle
        self.mo: Model = self.species.mo  # model handle
        self.rvalue = self.sp.r

        # right y-axis label
        self.ld: str = f"{self.species.dn} [{self.species.ds}]"
        self.xl: str = self.mo.xl  # set x-axis lable to model time

        if self.legend_left == "None":
            self.legend_left = self.species.dsa

        self.legend_right = f"{self.species.dn} [{self.species.ds}]"
        # legend_left is in __init__ !

        # decide whether we use isotopes
        if self.mo.m_type == "both":
            self.isotopes = True
        elif self.mo.m_type == "mass_only":
            self.isotopes = False

        if self.geometry != "None":
            get_box_geometry_parameters(self)

        if self.display_precision == 0:
            self.display_precision = self.mo.display_precision

    # setup a placeholder setitem function
    def __setitem__(self, i: int, value: float):
        return self.__set_data__(i, value)

    def __call__(self) -> None:  # what to do when called as a function ()
        pass
        return self

    def __getitem__(self, i: int) -> NDArray[np.float64]:
        """Get flux data by index"""

        return np.array([self.m[i], self.l[i], self.c[i]])

    def __set_with_isotopes__(self, i: int, value: float) -> None:
        """write data by index"""

        self.m[i]: float = value[0]
        # update concentration and delta next. This is computationally inefficient
        # but the next time step may depend on on both variables.
        self.c[i]: float = value[0] / self.v[i]  # update concentration
        self.l[i]: float = value[1]

    def __set_without_isotopes__(self, i: int, value: float) -> None:
        """write data by index"""

        self.m[i]: float = value[0]
        self.c[i]: float = self.m[i] / self.v[i]  # update concentration

    def __update_mass__() -> None:
        """Place holder function"""

        raise NotImplementedError("__update_mass__ is not yet implmented")

    def get_process_args(self):
        """Provide the data structure which needs to be passed to the numba solver"""

        data = List(
            [
                self.m,  # 0
                self.l,  # 1
                self.c,  # 2
                self.v,  # 3
            ]
        )

        func_name: function = self.__update_mass__
        params = List([float(reservoir.species.element.r)])

        return func_name, data, params

    def __write_data__(
        self,
        prefix: str,
        start: int,
        stop: int,
        stride: int,
        append: bool,
        directory: str,
    ) -> None:
        """To be called by write_data and save_state"""

        from pathlib import Path

        p = Path(directory)
        p.mkdir(parents=True, exist_ok=True)

        # some short hands
        sn = self.sp.n  # species name
        sp = self.sp  # species handle
        mo = self.sp.mo  # model handle

        smu = f"{mo.m_unit:~P}"
        mtu = f"{mo.t_unit:~P}"
        fmu = f"{mo.f_unit:~P}"
        cmu = f"{mo.c_unit:~P}"

        sdn = self.sp.dn  # delta name
        sds = self.sp.ds  # delta scale
        rn = self.full_name  # reservoir name
        mn = self.sp.mo.n  # model name
        if self.sp.mo.register == "None":
            fn = f"{directory}/{prefix}{mn}_{rn}.csv"  # file name
        elif self.sp.mo.register == "local":
            fn = f"{directory}/{prefix}{rn}.csv"  # file name
        else:
            raise ValueError(
                f"Model register keyword must be 'None'/'local' not {self.sp.mo.register}"
            )

        # build the dataframe
        df: pd.dataframe = DataFrame()

        df[f"{rn} Time [{mtu}]"] = self.mo.time[start:stop:stride]  # time
        df[f"{rn} {sn} [{smu}]"] = self.m[start:stop:stride]  # mass
        df[f"{rn} {sp.ln} [{smu}]"] = self.l[start:stop:stride]  # light isotope
        df[f"{rn} {sn} [{cmu}]"] = self.c[start:stop:stride]  # concentration

        fullname: list = []

        for f in self.lof:  # Assemble the headers and data for the reservoir fluxes
            if f.full_name in fullname:
                raise ValueError(f"{f.full_name} is a double")
            fullname.append(f.full_name)

            if f.save_flux_data:
                df[f"{f.full_name} {sn} [{fmu}]"] = f.m[start:stop:stride]  # m
                df[f"{f.full_name} {sn} [{sp.ln}]"] = f.l[start:stop:stride]  #  l
            else:
                df[f"{f.full_name} {sn} [{fmu}]"] = f.fa[0]  # m
                df[f"{f.full_name} {sn} [{sp.ln}]"] = f.fa[1]  # l

        file_path = Path(fn)
        if append:
            if file_path.exists():
                df.to_csv(file_path, header=False, mode="a", index=False)
            else:
                df.to_csv(file_path, header=True, mode="w", index=False)
        else:
            df.to_csv(file_path, header=True, mode="w", index=False)

        return df

    def __sub_sample_data__(self) -> None:
        """There is usually no need to keep more than a thousand data points
        so we subsample the results before saving, or processing them

        """
        stride = int(len(self.m) / self.mo.number_of_datapoints)

        # print(f"Reset data with {len(self.m)}, stride = {self.mo.reset_stride}")
        self.m = self.m[2:-2:stride]
        self.l = self.l[2:-2:stride]
        # self.h = self.h[2:-2:stride]
        # self.d = self.d[2:-2:stride]
        self.c = self.c[2:-2:stride]

    def __reset_state__(self) -> None:
        """Copy the result of the last computation back to the beginning
        so that a new run will start with these values

        save the current results into the temp fields

        """

        # print(f"Reset data with {len(self.m)}, stride = {self.mo.reset_stride}")
        self.mc = np.append(self.mc, self.m[0 : -2 : self.mo.reset_stride])
        # self.dc = np.append(self.dc, self.d[0 : -2 : self.mo.reset_stride])
        self.cc = np.append(self.cc, self.c[0 : -2 : self.mo.reset_stride])

        # copy last result into first field
        self.m[0] = self.m[-2]
        self.l[0] = self.l[-2]
        # self.h[0] = self.h[-2]
        # self.d[0] = self.d[-2]
        self.c[0] = self.c[-2]

    def __merge_temp_results__(self) -> None:
        """Once all iterations are done, replace the data fields
        with the saved values

        """

        self.m = self.mc
        self.c = self.cc
        # self.d = self.dc

    def __read_state__(self, directory: str) -> None:
        """read data from csv-file into a dataframe

        The CSV file must have the following columns

        Model Time     t
        Reservoir_Name m
        Reservoir_Name l
        Reservoir_Name h
        Reservoir_Name d
        Reservoir_Name c
        Flux_name m
        Flux_name l etc etc.

        """

        from .utility_functions import is_name_in_list, get_object_from_list

        read: set = set()
        curr: set = set()

        if self.sp.mo.register == "None":
            fn = f"{directory}/state_{self.mo.n}_{self.full_name}.csv"
        elif self.sp.mo.register == "local":
            fn = f"{directory}/state_{self.full_name}.csv"
        else:
            raise ValueError(
                f"Model register keyword must be 'None'/'local' not {self.sp.mo.register}"
            )

        logging.info(f"reading state for {self.full_name} from {fn}")

        if not os.path.exists(fn):
            raise FileNotFoundError(
                f"Flux {fn} does not exist in Reservoir {self.full_name}"
            )

        # get a set of all current fluxes
        for f in self.lof:
            curr.add(f.full_name)
            logging.debug(f"    Adding Flux {f.full_name} to list of fluxes to read")

        self.df: pd.DataFrame = pd.read_csv(fn)
        self.headers: list = list(self.df.columns.values)
        df = self.df
        headers = self.headers

        # the headers contain the object name for each data in the
        # reservoir or flux thus, we must reduce the list to unique
        # object names first. Note, we must preserve order
        header_list: list = []
        for x in headers:
            n = x.split(" ")[0]
            if n not in header_list:
                header_list.append(n)

        # loop over all columns
        col: int = 1  # we ignore the time column
        i: int = 0
        for n in header_list:
            name = n.split(" ")[0]
            logging.debug(f"Looking for {name}")
            # this finds the reservoir name
            if name == self.full_name:
                logging.debug(f"found reservoir data for {name}")
                col = self.__assign_reservoir_data__(self, df, col, True)
            # this loops over all fluxes in a reservoir
            elif is_name_in_list(name, self.lof):
                logging.debug(f"{name} is in {self.full_name}.lof")
                obj = get_object_from_list(name, self.lof)
                logging.debug(
                    f"found object {obj.full_name} adding flux data for {name}"
                )
                read.add(obj.full_name)
                col = self.__assign_flux_data__(obj, df, col, False)
                i += 1
            else:
                raise ValueError(f"Unable to find Flux {n} in {self.full_name}")

        # test if we missed any fluxes
        for f in list(curr.difference(read)):
            print(f"\n Warning: Did not find values for {f}\n in saved state")

    def __assign_flux_data__(
        self, obj: any, df: pd.DataFrame, col: int, res: bool
    ) -> int:
        """
        Assign the third last entry data to all values in flux

        parameters: df = dataframe
                    col = column number
                    res = true if reservoir

        """

        obj.fa[0] = df.iloc[0, col]
        obj.fa[1] = df.iloc[0, col + 1]
        # obj.fa[2] = df.iloc[0, col + 2]
        # obj.fa[3] = df.iloc[0, col + 3]
        col = col + 2

        return col

    def __assign_reservoir_data__(
        self, obj: any, df: pd.DataFrame, col: int, res: bool
    ) -> int:
        """
        Assign the third last entry data to all values in reservoir

        parameters: df = dataframe
                    col = column number
                    res = true if reservoir

        """

        obj.m[:] = df.iloc[-3, col]
        obj.l[:] = df.iloc[-3, col + 1]
        # obj.h[:] = df.iloc[-3, col + 2]
        # obj.d[:] = df.iloc[-3, col + 3]
        obj.c[:] = df.iloc[-3, col + 2]
        col = col + 3

        return col

    def __plot__(self, i: int) -> None:
        """Plot data from reservoirs and fluxes into a multiplot window"""

        model = self.sp.mo
        species = self.sp
        obj = self
        # time = model.time + model.offset  # get the model time
        # xl = f"Time [{model.bu}]"

        size, geo = get_plot_layout(self)  # adjust layout
        filename = f"{model.n}_{self.full_name}.pdf"
        fn = 1  # counter for the figure number

        plt.style.use(model.plot_style)
        fig = plt.figure(i)  # Initialize a plot window
        fig.canvas.manager.set_window_title(f"Reservoir Name: {self.n}")
        fig.set_size_inches(size)

        # plot reservoir data
        if self.plot == "yes":
            plot_object_data(geo, fn, self)

            # plot the fluxes assoiated with this reservoir
            for f in sorted(self.lof):  # plot flux data
                if f.plot == "yes":
                    fn = fn + 1
                    plot_object_data(geo, fn, f)

            for d in sorted(self.ldf):  # plot data fields
                fn = fn + 1
                plot_object_data(geo, fn, d)

            if geo != [1, 1]:
                if self.groupname == "None":
                    fig.suptitle(f"Model: {model.n}, Reservoir: {self.n}\n", size=16)
                else:
                    # filename = f"{self.groupname}_{self.n}.pdf"
                    fig.suptitle(
                        f"Group: {self.groupname}, Reservoir: {self.n}\n", size=16
                    )

            fig.tight_layout()
            fig.subplots_adjust(top=0.88)
            print(f"Saving as {filename}")
            fig.savefig(filename)

    def __plot_reservoirs__(self, i: int) -> None:
        """Plot only the  reservoirs data, and ignore the fluxes"""

        model = self.sp.mo
        species = self.sp
        obj = self
        time = model.time + model.offset  # get the model time
        xl = f"Time [{model.bu}]"

        size: list = [5, 3]
        geo: list = [1, 1]
        filename = f"{model.n}_{self.n}.pdf"
        fn: int = 1  # counter for the figure number

        plt.style.use(model.plot_style)
        fig = plt.figure(i)  # Initialize a plot window
        fig.set_size_inches(size)

        # plt.legend()ot reservoir data
        plot_object_data(geo, fn, self)

        fig.tight_layout()
        # fig.subplots_adjust(top=0.88)
        fig.savefig(filename)

    def info(self, **kwargs) -> None:
        """Show an overview of the object properties.
        Optional arguments are
        index  :int = 0 this will show data at the given index
        indent :int = 0 indentation

        """
        off: str = "  "
        if "index" not in kwargs:
            index = 0
        else:
            index = kwargs["index"]

        if "indent" not in kwargs:
            indent = 0
            ind = ""
        else:
            indent = kwargs["indent"]
            ind = " " * indent

        # print basic data bout this reservoir
        print(f"{ind}{self.__str__(kwargs)}")
        print(f"{ind}Data sample:")
        show_data(self, index=index, indent=indent)

        print(f"\n{ind}Connnections:")
        for p in sorted(self.loc):
            print(f"{off}{ind}{p.full_name}.info()")

        print(f"\n{ind}Fluxes:")
        from esbmtk import Q_

        # m = Q_("1 Sv").to("l/a").magnitude
        for i, f in enumerate(self.lof):
            print(f"{off}{ind}{f.full_name}: {self.lodir[i]*f.m[-2]:.2e}")

        print()
        print("Use the info method on any of the above connections")
        print("to see information on fluxes and processes")

    @property
    def concentration(self) -> float:
        return self._concentration

    @concentration.setter
    def concentration(self, c) -> None:
        self._concentration: Number = c.to(self.mo.c_unit).magnitude
        self.mass: Number = self.concentration * self.volume  # caculate mass
        self.c = self.c * 0 + self.concentration
        self.m = self.m * 0 + self.mass


class Reservoir(ReservoirBase):
    """This object holds reservoir specific information.

          Example::

                  Reservoir(name = "foo",      # Name of reservoir
                            species = S,          # Species handle
                            delta = 20,           # initial delta - optional (defaults  to 0)
                            mass/concentration = "1 unit"  # species concentration or mass
                            volume/geometry = "1E5 l",      # reservoir volume (m^3)
                            plot = "yes"/"no", defaults to yes
                            plot_transform_c = a function reference, optional (see below)
                            legend_left = str, optional, useful for plot transform
                            display_precision = number, optional, inherited from Model
                            register = optional, use to register with Reservoir Group
                            isotopes = True/False otherwise use Model.m_type
                            seawater_parameters= dict, optional
                            )

          You must either give mass or concentration.  The result will always be displayed
          as concentration though.

          You must provide either the volume or the geometry keyword. In the latter case
          provide a list where the first entry is the upper depth datum, the second entry is
          the lower depth datum, and the third entry is the area percentage. E.g., to specify
          the upper 200 meters of the entire ocean, you would write:

                 geometry=[0,-200,1]

          the corresponding ocean volume will then be calculated by the calc_volume method
          in this case the following instance variables will also be set:

                 self.volume in model units (usually liter)
                 self.are:a surface area in m^2 at the upper bounding surface
                 self.area_dz: area of seafloor which is intercepted by this box.
                 self.area_fraction: area of seafloor which is intercepted by this
                                    relative to the total ocean floor area

          Adding seawater_properties:
          ~~~~~~~~~~~~~~~~~~~~~~~~~~~
          If this optional parameter is specified, a SeaWaterConstants instance will be registered
          for this Reservoir as Reservoir.swc
          See the  SeaWaterConstants class for details how to specify the parameters, e.g.:
          seawater_parameters = {"temperature": 2, "pressure": 240, "salinity" : 35},

          Using a transform function
          ~~~~~~~~~~~~~~~~~~~~~~~~~~

          In some cases, it is useful to transform the reservoir
          concentration data before plotting it.  A good example is the H+
          concentration in water which is better displayed as pH.  We can
          do this by specifying a function to convert the reservoir
          concentration into pH units::

              def phc(c :float) -> float:
                  # Calculate concentration as pH. c can be a number or numpy array

                  import numpy as np

                  pH :float = -np.log10(c)
                  return pH

          this function can then be added to a reservoir as::

          hplus.plot_transform_c = phc

          You can modify the left legend to suit the transform via the legend_left keyword

          Note, at present the plot_transform_c function will only take one
          argument, which always defaults to the reservoir
          concentration. The function must return a single argument which
          will be interpreted as the transformed reservoir concentration.

    Accesing Reservoir Data:
    ~~~~~~~~~~~~~~~~~~~~~~~~

    You can access the reservoir data as:

    - Name.m # mass
    - Name.d # delta
    - Name.c # concentration

    Useful methods include:

    - Name.write_data() # save data to file
    - Name.info()   # info Reservoir
    """

    __slots__ = ("m", "l", "h", "d", "c", "lio", "rvalue", "lodir", "lof", "lpc")

    def __init__(self, **kwargs) -> None:
        """Initialize a reservoir."""

        from . import ureg, Q_

        # provide a dict of all known keywords and their type
        self.lkk: Dict[str, any] = {
            "name": str,
            "species": Species,
            "delta": (Number, str),
            "concentration": (str, Q_),
            "mass": (str, Q_),
            "volume": (str, Q_),
            "geometry": (list, str),
            "plot_transform_c": any,
            "legend_left": str,
            "plot": str,
            "groupname": str,
            "function": any,
            "display_precision": Number,
            "register": (SourceGroup, SinkGroup, ReservoirGroup, ConnectionGroup, str),
            "full_name": str,
            "seawater_parameters": (dict, str),
            "isotopes": bool,
        }

        # provide a list of absolutely required keywords
        self.lrk: list = [
            "name",
            "species",
            ["volume", "geometry"],
            ["mass", "concentration"],
        ]

        self.drn = {
            "concentration": "_concentration",
            "delta": "_delta",
        }

        # list of default values if none provided
        self.lod: Dict[any, any] = {
            "delta": "None",
            "plot": "yes",
            "mass": "None",
            "volume": "None",
            "geometry": "None",
            "concentration": "None",
            "plot_transform_c": "None",
            "legend_left": "None",
            "function": "None",
            "groupname": "None",
            "register": "None",
            "full_name": "Not Set",
            "isotopes": False,
            "seawater_parameters": "None",
            "display_precision": 0,
        }

        # validate and initialize instance variables
        self.__initerrormessages__()
        self.bem.update(
            {
                "mass": "a  string or quantity",
                "concentration": "a string or quantity",
                "volume": "a string or quantity",
                "plot": "yes or no",
                "register": "Group Object",
                "legend_left": "A string",
                "function": "A function",
            }
        )
        self.__validateandregister__(kwargs)

        if self.delta == "None":
            self.delta = 0

        self.__set_legacy_names__(kwargs)

        # geoemtry information
        if self.volume == "None":
            get_box_geometry_parameters(self)

        # convert units
        self.volume: Number = Q_(self.volume).to(self.mo.v_unit).magnitude

        # This should probably be species specific?
        self.mu: str = self.sp.e.mass_unit  # massunit xxxx

        if self.mass == "None":
            c = Q_(self.concentration)
            self.plt_units = c.units
            self._concentration: Number = c.to(self.mo.c_unit).magnitude
            self.mass: Number = self._concentration * self.volume  # caculate mass
            self.display_as = "concentration"
        elif self.concentration == "None":
            m = Q_(self.mass)
            self.plt_units = self.mo.m_unit
            self.mass: Number = m.to(self.mo.m_unit).magnitude
            self.concentration = self.mass / self.volume
            self.display_as = "mass"
        else:
            raise ValueError("You need to specify mass or concentration")

        # save the unit which was provided by the user for display purposes
        # left y-axis label
        self.lm: str = f"{self.species.n} [{self.mu}/l]"

        # initialize mass vector
        self.m: [NDArray, Float[64]] = zeros(self.species.mo.steps) + self.mass
        self.l: [NDArray, Float[64]] = zeros(self.mo.steps)
        self.v: [NDArray, Float[64]] = (
            np.zeros(self.mo.steps) + self.volume
        )  # reservoir volume

        if self.mass == 0:
            self.c: [NDArray, Float[64]] = zeros(self.species.mo.steps)
        else:
            # initialize concentration vector
            self.c: [NDArray, Float[64]] = self.m / self.v
            # isotope mass
            self.l = get_l_mass(self.m, self.delta, self.species.r)
            # delta of reservoir

        # create temporary memory if we use multiple solver iterations
        if self.mo.number_of_solving_iterations > 0:
            self.mc = np.empty(0)
            self.cc = np.empty(0)
            self.dc = np.empty(0)

        self.mo.lor.append(self)  # add this reservoir to the model
        # register instance name in global name space
        if self.mo.register == "local" and self.register == "None":
            self.register = self.mo
        self.__register_name__()

        # decide which setitem functions to use
        if self.isotopes:
            self.__set_data__ = self.__set_with_isotopes__
        else:
            self.__set_data__ = self.__set_without_isotopes__

        # any auxilliary init - normally empty, but we use it here to extend the
        # reservoir class in virtual reservoirs
        self.__aux_inits__()

        if self.seawater_parameters != "None":
            if "temperature" in self.seawater_parameters:
                temperature = self.seawater_parameters["temperature"]
            else:
                temperature = 25
            if "salinity" in self.seawater_parameters:
                salinity = self.seawater_parameters["salinity"]
            else:
                salinity = 35
            if "pressure" in self.seawater_parameters:
                pressure = self.seawater_parameters["pressure"]
            else:
                pressure = 1

            SeawaterConstants(
                name="swc",
                model=self.mo,
                temperature=temperature,
                pressure=pressure,
                salinity=salinity,
                register=self,
                units=self.mo.c_unit,
            )

        self.state = 0

    @property
    def delta(self) -> float:
        return self._delta

    @delta.setter
    def delta(self, d: float) -> None:
        self._delta: float = d
        self.isotopes = True
        self.l = get_l_mass(self.m, d, self.species.r)


class Flux(esbmtkBase):
    """A class which defines a flux object. Flux objects contain
    information which links them to an species, describe things like
    the mass and time unit, and store data of the total flux rate at
    any given time step. Similarly, they store the flux of the light
    and heavy isotope flux, as well as the delta of the flux. This
    is typically handled through the Connect object. If you set it up manually

    Flux = (name = "Name"
            species = species_handle,
            delta = any number,
            rate  = "12 mol/s" # must be a string
            display_precision = number, optional, inherited from Model
    )

     You can access the flux data as
    - Name.m # mass
    - Name.d # delta
    - Name.c # concentration

    """

    __slots__ = ("m", "l", "h", "d", "rvalue", "lpc")

    def __init__(self, **kwargs: Dict[str, any]) -> None:
        """
        Initialize a flux. Arguments are the species name the flux rate
        (mol/year), the delta value and unit

        """

        from . import ureg, Q_, AirSeaExchange

        # provide a dict of all known keywords and their type
        self.lkk: Dict[str, any] = {
            "name": str,
            "species": Species,
            "delta": Number,
            "rate": (str, Q_),
            "plot": str,
            "display_precision": Number,
            "isotopes": bool,
            "register": any,
            "save_flux_data": (bool, str),
            "id": str,
        }

        # provide a list of absolutely required keywords
        self.lrk: list = ["name", "species", "rate"]

        # list of default values if none provided
        self.lod: Dict[any, any] = {
            "delta": 0,
            "plot": "yes",
            "display_precision": 0,
            "isotopes": False,
            "register": "None",
            "id": "",
            "save_flux_data": "None",
        }

        # initialize instance
        self.__initerrormessages__()
        self.bem.update({"rate": "a string", "plot": "a string"})
        self.__validateandregister__(kwargs)  # initialize keyword values

        # if save_flux_data is unsepcified, use model default
        if self.save_flux_data == "None":
            self.save_flux_data = self.species.mo.save_flux_data

        # legacy names
        self.n: str = self.name  # name of flux
        self.sp: Species = self.species  # species name
        self.mo: Model = self.species.mo  # model name
        self.model: Model = self.species.mo  # model handle
        self.rvalue = self.sp.r

        if self.display_precision == 0:
            self.display_precision = self.mo.display_precision

        # model units
        self.plt_units = Q_(self.rate).units
        self.mu: str = f"{self.species.mu}/{self.mo.tu}"

        # and convert flux into model units
        fluxrate: float = Q_(self.rate).to(self.mo.f_unit).magnitude

        if self.delta:
            li = get_l_mass(fluxrate, self.delta, self.sp.r)
        else:
            li = 0
        self.fa: [NDArray, Float[64]] = np.array([fluxrate, li])

        # in case we want to keep the flux data
        if self.save_flux_data:
            self.m: [NDArray, Float[64]] = (
                zeros(self.model.steps) + fluxrate
            )  # add the flux
            self.l: [NDArray, Float[64]] = np.zeros(self.model.steps)

            if self.mo.number_of_solving_iterations > 0:
                self.mc = np.empty(0)
                self.dc = np.empty(0)

            if self.rate != 0:
                self.l = get_l_mass(self.m, self.delta, self.species.r)
                self.fa[1] = self.l[0]

        else:
            # setup dummy variables to keep existing numba data structures
            self.m = np.zeros(2)
            self.l = np.zeros(2)

            if self.rate != 0:
                self.fa[1] = get_l_mass(self.fa[0], self.delta, self.species.r)

        self.lm: str = f"{self.species.n} [{self.mu}]"  # left y-axis a label
        self.ld: str = f"{self.species.dn} [{self.species.ds}]"  # right y-axis a label

        self.legend_left: str = self.species.dsa
        self.legend_right: str = f"{self.species.dn} [{self.species.ds}]"

        self.xl: str = self.model.xl  # se x-axis label equal to model time
        self.lop: list[Process] = []  # list of processes
        self.lpc: list = []  # list of external functions
        self.led: list[ExternalData] = []  # list of ext data
        self.source: str = ""  # Name of reservoir which acts as flux source
        self.sink: str = ""  # Name of reservoir which acts as flux sink

        if self.name == "None":
            if self.mo.register == "None":  # global name_space
                if self.register == "None":
                    self.full_name = self.name
                else:
                    self.full_name = f"{self.register.full_name}.{self.name}"
            else:  # local name_space
                self.name = f"{self.id}_F"

        self.__register_name__()
        # print(f"f name set to {self.name}. fn =  {self.full_name}\n")
        self.mo.lof.append(self)  # register with model flux list

        # decide which setitem functions to use
        # decide whether we use isotopes
        if self.mo.m_type == "both":
            self.isotopes = True
        elif self.mo.m_type == "mass_only":
            self.isotopes = False

        if self.isotopes:
            self.__set_data__ = self.__set_with_isotopes__
            # self.__get_data__ = self.__get_with_isotopes__
        else:
            self.__set_data__ = self.__set_without_isotopes__
            # self.__get_data__ = self.__get_without_isotopes__

    # setup a placeholder setitem function
    def __setitem__(self, i: int, value: [NDArray, float]):
        return self.__set_data__(i, value)

    def __getitem__(self, i: int) -> NDArray[np.float64]:
        """Get data by index"""
        # return self.__get_data__(i)
        return self.fa
        # return array([self.m[i], self.l[i], self.h[i], self.d[i]])

    # def __get_with_isotopes__(self, i: int) -> NDArray[np.float64]:
    #     """Get data by index"""

    #     return array([self.m[i], self.l[i], self.h[i], self.d[i]])

    # def __get_without_isotopes__(self, i: int) -> NDArray[np.float64]:
    #     """Get data by index"""

    #     return array([self.m[i]])

    def __set_with_isotopes__(self, i: int, value: [NDArray, float]) -> None:
        """Write data by index"""

        self.m[i] = value[0]
        self.l[i] = value[1]
        self.fa = value[0:4]
        # self.d[i] = get_delta(self.l[i], self.h[i], self.sp.r)  # update delta

    def __set_without_isotopes__(self, i: int, value: [NDArray, float]) -> None:
        """Write data by index"""

        self.fa = [value[0], 0]
        self.m[i] = value[0]

    def __call__(self) -> None:  # what to do when called as a function ()
        pass
        return

    def __add__(self, other):
        """adding two fluxes works for the masses, but not for delta"""

        self.fa = self.fa + other.fa
        self.m = self.m + other.m
        self.l = self.l + other.l

    def __sub__(self, other):
        """substracting two fluxes works for the masses, but not for delta"""

        self.fa = self.fa - other.fa
        self.m = self.m - other.m
        self.l = self.l - other.l
        # self.h = self.h - other.h
        # self.d = get_delta(self.l, self.h, self.sp.r)

    def info(self, **kwargs) -> None:
        """Show an overview of the object properties.
        Optional arguments are
        index  :int = 0 this will show data at the given index
        indent :int = 0 indentation

        """
        off: str = "  "
        if "index" not in kwargs:
            index = 0
        else:
            index = kwargs["index"]

        if "indent" not in kwargs:
            indent = 0
            ind = ""
        else:
            indent = kwargs["indent"]
            ind = " " * indent

        # print basic data bout this object
        print(f"{ind}{self.__str__(kwargs)}")
        print(f"{ind}Data sample:")
        show_data(self, index=index, indent=indent)

        if len(self.lop) > 0:
            print(f"\n{ind}Process(es) acting on this flux:")
            for p in self.lop:
                print(f"{off}{ind}{p.__repr__()}")

            print("")
            print(
                "Use help on the process name to get an explanation what this process does"
            )
            if self.register == "None":
                print(f"e.g., help({self.lop[0].n})")
            else:
                print(f"e.g., help({self.register.name}.{self.lop[0].name})")
        else:
            print("There are no processes for this flux")

    def plot(self, **kwargs: dict) -> None:
        """Plot the flux data:"""

        fig, ax1 = plt.subplots()
        fig.set_size_inches(5, 4)  # Set figure size in inches
        fig.set_dpi(100)  # Set resolution in dots per inch

        ax1.plot(self.mo.time, self.m, c="C0")
        ax2 = ax1.twinx()  # get second y-axis
        ax2.plot(self.mo.time, self.d, c="C1", label=self.n)

        ax1.set_title(self.n)
        ax1.set_xlabel(f"Time [{self.mo.tu}]")  #
        ax1.set_ylabel(f"{self.sp.n} [{self.sp.mu}]")
        ax2.set_ylabel(f"{self.sp.dn} [{self.sp.ds}]")
        ax1.spines["top"].set_visible(False)  # remove unnecessary frame
        ax2.spines["top"].set_visible(False)  # remove unnecessary frame

        fig.tight_layout()
        plt.show()
        plt.savefig(self.n + ".pdf")

    def __sub_sample_data__(self) -> None:
        """There is usually no need to keep more than a thousand data points
        so we subsample the results before saving, or processing them

        """

        if self.save_flux_data:
            stride = int(len(self.m) / self.mo.number_of_datapoints)

            self.m = self.m[2:-2:stride]
            self.l = self.m[2:-2:stride]

    def __reset_state__(self) -> None:
        """Copy the result of the last computation back to the beginning
        so that a new run will start with these values.

        Also, copy current results into temp field
        """

        if self.save_flux_data:
            self.mc = np.append(self.mc, self.m[0 : -2 : self.mo.reset_stride])
            # copy last element to first position
            self.m[0] = self.m[-2]
            self.l[0] = self.l[-2]

    def __merge_temp_results__(self) -> None:
        """Once all iterations are done, replace the data fields
        with the saved values

        """

        self.m = self.mc


class SourceSink(esbmtkBase):
    """
    This is a meta class to setup a Source/Sink objects. These are not
    actual reservoirs, but we stil need to have them as objects
    Example::

           Sink(name = "Pyrite",
               species = SO4,
               display_precision = number, optional, inherited from Model
               delta = number or str. optional defaults to "None"
           )

    where the first argument is a string, and the second is a reservoir handle

    """

    def __init__(self, **kwargs) -> None:

        self._delta = "None"
        # provide a dict of all known keywords and their type
        self.lkk: Dict[str, any] = {
            "name": str,
            "species": Species,
            "display_precision": Number,
            "register": (SourceGroup, SinkGroup, ReservoirGroup, ConnectionGroup, str),
            "delta": (Number, str),
            "isotopes": bool,
        }

        # variables which are properties
        self.drn = {
            "delta": "_delta",
        }

        # provide a list of absolutely required keywords
        self.lrk: list[str] = ["name", "species"]

        # list of default values if none provided
        self.lod: Dict[str, any] = {
            "display_precision": 0,
            "delta": "None",
            "isotopes": False,
            "register": "None",
        }

        self.__initerrormessages__()
        self.__validateandregister__(kwargs)  # initialize keyword values

        self.loc: set[Connection] = set()  # set of connection objects

        # legacy names
        # if self.register != "None":
        #    self.full_name = f"{self.name}.{self.register.name}"

        self.n = self.name
        self.sp = self.species
        self.mo = self.species.mo
        self.u = self.species.mu + "/" + str(self.species.mo.bu)
        self.lio: list = []

        if self.mo.register == "local" and self.register == "None":
            self.register = self.mo
        else:
            if self.register == "None":
                self.pt = self.name
            else:
                self.pt: str = f"{self.register.name}_{self.n}"
                self.groupname = self.register.name

        if self.display_precision == 0:
            self.display_precision = self.mo.display_precision

        self.__register_name__()

    @property
    def delta(self):
        return self._delta

    @delta.setter
    def delta(self, d):
        """Set/Update delta"""
        if d != "None":
            self._delta = d
            self.isotopes = True
            self.m = 1
            self.l = get_l_mass(self.m, d, self.species.r)
            self.c = self.l / (self.m - self.l)
            self.provided_kwargs.update({"delta": d})


class Sink(SourceSink):
    """
    This is just a wrapper to setup a Sink object
    Example::

           Sink(name = "Pyrite",species =SO4)

    where the first argument is a string, and the second is a species handle
    """


class Source(SourceSink):
    """
    This is just a wrapper to setup a Source object
    Example::

           Source(name = "SO4_diffusion", species ="SO4")

    where the first argument is a string, and the second is a species handle
    """


from .extended_classes import *
from .connections import Connection, ConnectionGroup
from .processes import *

from .species_definitions import (
    carbon,
    sulfur,
    hydrogen,
    phosphor,
    oxygen,
    nitrogen,
    boron,
)

from .carbonate_chemistry import *
from .sealevel import *
from .solver import *
