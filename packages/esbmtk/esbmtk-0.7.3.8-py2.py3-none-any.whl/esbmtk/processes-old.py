from numbers import Number
from nptyping import *
from typing import *
from numpy import array, set_printoptions, arange, zeros, interp, mean
from pandas import DataFrame
from copy import deepcopy, copy
from time import process_time
from numba import njit
from numba.typed import List

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import logging
import time
import builtins

set_printoptions(precision=4)
# from .utility_functions import *
from .esbmtk import esbmtkBase, Reservoir, Flux, Signal, Source, Sink
from .utility_functions import sort_by_type
from .solver import get_imass, get_frac, get_delta, get_flux_data
from . import ureg, Q_

# from .connections import ConnnectionGroup


class Process(esbmtkBase):
    """This class defines template for process which acts on one or more
    reservoir flux combinations. To use it, you need to create an
    subclass which defines the actual process implementation in their
    call method. See 'PassiveFlux as example'

    """

    __slots__ = ("reservoir", "r", "flux", "r", "mo", "direction", "scale")

    def __init__(self, **kwargs: Dict[str, any]) -> None:
        """
        Create a new process object with a given process type and options
        """

        self.__defaultnames__()  # default kwargs names
        self.__initerrormessages__()  # default error messages
        self.bem.update({"rate": "a string"})
        self.bem.update({"scale": "Number or quantity"})
        self.__validateandregister__(kwargs)  # initialize keyword values

        self.__postinit__()  # do some housekeeping
        self.__register_name__()

    def __postinit__(self) -> None:
        """Do some housekeeping for the process class"""

        # legacy name aliases
        self.n: str = self.name  # display name of species
        self.r: Reservoir = self.reservoir
        self.f: Flux = self.flux
        self.m: Model = self.r.sp.mo  # the model handle
        self.mo: Model = self.m

        # self.rm0: float = self.r.m[0]  # the initial reservoir mass
        if isinstance(self.r, Reservoir):
            self.direction: Dict[Flux, int] = self.r.lio[self.f]

        self.__misc_init__()

    def __delayed_init__(self) -> None:
        """
        Initialize stuff which is only known after the entire model has been defined.
        This will be executed just before running the model. You need to add the following
        two lines somewhere in the init procedure (preferably by redefining __misc_init__)
        and redefine __delayed_init__ to actually execute any code below

        # this process requires delayed init
        self.mo.lto.append(self)

        """

        pass

    def __misc_init__(self) -> None:
        """This is just a place holder method which will be called by default
        in __post_init__() This can be overloaded to add additional
        code to the init procedure without the need to redefine
        init. This useful for processes which only define a call method.

        """

        pass

    def __defaultnames__(self) -> None:
        """Set up the default names and dicts for the process class. This
        allows us to extend these values without modifying the entire init process

        """

        from .connections import ConnectionGroup
        from esbmtk import Reservoir, ReservoirGroup, Flux, GasReservoir

        # provide a dict of known keywords and types
        self.lkk: Dict[str, any] = {
            "name":
            str,
            "reservoir": (Reservoir, Source, Sink, GasReservoir),
            "flux":
            Flux,
            "rate": (Number, np.float64),
            "delta": (Number, np.float64),
            "lt":
            Flux,
            "alpha": (Number, np.float64),
            "scale": (Number, np.float64),
            "ref_reservoirs": (Flux, Reservoir, GasReservoir, list, str),
            "register": (
                str,
                ConnectionGroup,
                Reservoir,
                ReservoirGroup,
                GasReservoir,
                Flux,
            ),
        }

        # provide a list of absolutely required keywords
        self.lrk: list[str] = ["name"]

        # list of default values if none provided
        self.lod: Dict[str, any] = {"scale": 1}

    def __register__(self, reservoir: Reservoir, flux: Flux) -> None:
        """Register the flux/reservoir pair we are acting upon, and register
        the process with the reservoir

        """

        # register the reservoir flux combination we are acting on
        self.f: Flux = flux
        self.r: Reservoir = reservoir
        # add this process to the list of processes acting on this reservoir
        reservoir.lop.append(self)
        flux.lop.append(self)
        # Add to model flux list
        reservoir.mo.lop.append(self)

    def show_figure(self, x, y) -> None:
        """Apply the current process to the vector x, and show the result as y.
        The resulting figure will be automatically saved.

        Example::
             process_name.show_figure(x,y)

        """
        pass


class GenericFunction(Process):
    """This Process class creates a GenericFunction instance which is
    typically used with the VirtualReservoir, and
    ExternalCode classes. This class is not user facing,
    please see the ExternalCode class docstring for the
    function template of a user provided function.

    see calc_carbonates in the carbonate chemistry for an example how
    to write a function for this class.

    """

    __slots__ = ("function", "input_data", "vr_data", "params")

    def __init__(self, **kwargs: Dict[str, any]) -> None:
        """
        Create a new process object with a given process type and options

        """

        from . import Reservoir_no_set

        self.__defaultnames__()  # default kwargs names

        # list of allowed keywords
        self.lkk: Dict[str, any] = {
            "name": str,
            "function": any,
            "input_data": (List, str),
            "vr_data": (List, str),
            "function_params": (List, str),
            "model": any,
        }

        # required arguments
        self.lrk: list = [
            "name", "input_data", "vr_data", "function_params", "model"
        ]

        # list of default values if none provided
        self.lod: Dict[any, any] = {}

        self.__initerrormessages__()  # default error messages
        self.bem.update({
            "function": "a function",
            "input_data": "list of one or more numpy arrays",
            "vr_data": "list of one or more numpy arrays",
            "function_params": "a list of float values",
        })
        self.__validateandregister__(kwargs)  # initialize keyword values
        self.mo = self.model

        if not callable(self.function):
            raise ValueError(
                "function must be defined before it can be used here")

        self.__postinit__()  # do some housekeeping

        if self.mo.register == "local" and self.register == "None":
            self.register = self.mo

        self.__register_name__()  #

    def __call__(self, i: int) -> None:
        """Here we execute the user supplied function
        Where i = index of the current timestep

        """

        self.function(i, self.input_data, self.vr_data, self.function_params)

    # redefine post init
    def __postinit__(self) -> None:
        """Do some housekeeping for the process class"""

        self.__misc_init__()

    def get_process_args(self) -> tuple:
        """return the data associated with this object"""

        self.func_name: function = self.function

        return (
            self.func_name,
            self.input_data,
            self.vr_data,
            self.function_params,
        )


class LookupTable(Process):
    """This process replaces the flux-values with values from a static
    lookup table

         Example::

         LookupTable("name", upstream_reservoir_handle, lt=flux-object)

         where the flux-object contains the mass, li, hi, and delta values
         which will replace the current flux values.

    """
    def __call__(self, i: int) -> None:
        """Here we replace the flux value with the value from the flux object
        which we use as a lookup-table

        """
        self.m[i]: float = self.lt.m[i]
        self.d[i]: float = self.lt.d[i]
        self.l[i]: float = self.lt.l[i]
        self.h[i]: float = self.lt.h[i]


class AddSignal(Process):
    """This process adds values to the current flux based on the values provided by the signal object.
    This class is typically invoked through the connector object

     Example::

     AddSignal(name = "name",
               reservoir = upstream_reservoir_handle,
               flux = flux_to_act_upon,
               lt = flux with lookup values)

     where - the upstream reservoir is the reservoir the process belongs too
             the flux is the flux to act upon
             lt= contains the flux object we lookup from

    """
    def __init__(self, **kwargs: Dict[str, any]) -> None:
        """
        Create a new process object with a given process type and options
        """

        # get default names and update list for this Process
        self.__defaultnames__()  # default kwargs names
        self.lrk.extend(["lt", "flux", "reservoir"])  # new required keywords

        self.__initerrormessages__()
        # self.bem.update({"rate": "a string"})
        self.__validateandregister__(kwargs)  # initialize keyword values

        # legacy variables
        self.mo = self.reservoir.mo
        self.__postinit__()  # do some housekeeping
        self.__register_name__()

        # decide whichh call function to use
        # if self.mo.m_type == "both":

        if self.reservoir.isotopes:
            self.__execute__ = self.__add_with_isotopes__
        else:
            self.__execute__ = self.__add_without_isotopes__

    # setup a placeholder call function
    def __call__(self, i: int):
        return self.__execute__(i)

    # use this when we do isotopes
    def __add_with_isotopes__(self, i) -> None:
        """Each process is associated with a flux (self.f). Here we replace
        the flux value with the value from the signal object which
        we use as a lookup-table (self.lt)

        """
        # add signal mass to flux mass

        self.f.m[i] = self.f.m[i] + self.lt.m[i]
        self.f.d[i] = self.f.d[i] + self.lt.d[i]
        if self.f.m[i] != 0:
            # self.f[i] = self.f[i] + self.lt[i]
            self.f.l[i], self.f.h[i] = get_imass(self.f.m[i], self.f.d[i],
                                                 self.r.rvalue)
        # signals may have zero mass, but may have a delta offset. Thus, we do not know
        # the masses for the light and heavy isotope. As such we have to calculate the masses
        # after we add the signal to a flux

    # use this when we do isotopes
    def __add_without_isotopes__(self, i) -> None:
        """Each process is associated with a flux (self.f). Here we replace
        the flux value with the value from the signal object which
        we use as a lookup-table (self.lt)

        """
        # add signal mass to flux mass
        self.f.m[i] = self.f.m[i] + self.lt.m[i]

    def get_process_args(self):

        func_name: function = self.p_add_signal

        print(f"flux_name = {self.flux.full_name}")

        data = List([
            self.flux.m,  # 0
            self.flux.l,  # 1
            self.flux.h,  # 2
            self.flux.d,  # 3
            self.lt.m,  # 4
            self.lt.l,  # 5
            self.lt.h,  # 6
            self.lt.d,  # 7
        ])

        params = List([float(self.reservoir.species.element.r)])

        return func_name, data, params

    @staticmethod
    @njit(fastmath=True, error_model="numpy")
    def p_add_signal(data, params, i) -> None:

        r: float = params[0]

        # flux masses and delta
        # fm: float = data[0][i]
        # fl: float = data[1][i]
        # fh: float = data[2][i]
        # fd: float = data[3][i]

        # signal masses and delta
        # sm: float = data[4][i]
        # sl: float = data[5][i]
        # sd: float = data[7][i]

        # new masses and delta. Note that signals may have zero mass
        # but a non-zero delta. So simply adding h and l won't work

        data[0][i] = data[0][i] + data[4][i]
        data[3][i] = data[3][i] + data[7][i]
        # fl = (1000.0 * fm) / ((sd + 1000.0) * r + 1000.0)
        data[1][i] = (1000.0 * data[0][i]) / (
            (data[3][i] + 1000.0) * r + 1000.0)
        data[2][i] = data[0][i] - data[1][i]


class MultiplySignal(Process):
    """This process mulitplies a given flux witthe the data in the signal.
    This class is typically invoked through the connector object:

    Note that this process will not modify the delta value of a given flux.
    If you needto vary the delta value it is best to add a second signal which uses the
    add signal type.

     Example::

     MultiplySignal(name = "name",
               reservoir = upstream_reservoir_handle,
               flux = flux_to_act_upon,
               lt = flux with lookup values)

     where - the upstream reservoir is the reservoir the process belongs too
             the flux is the flux to act upon
             lt= contains the flux object we lookup from

    """
    def __init__(self, **kwargs: Dict[str, any]) -> None:
        """
        Create a new process object with a given process type and options
        """

        # get default names and update list for this Process
        self.__defaultnames__()  # default kwargs names
        self.lrk.extend(["lt", "flux", "reservoir"])  # new required keywords

        self.__initerrormessages__()
        # self.bem.update({"rate": "a string"})
        self.__validateandregister__(kwargs)  # initialize keyword values

        # legacy variables
        self.mo = self.reservoir.mo
        self.__postinit__()  # do some housekeeping
        self.__register_name__()

        # decide whichh call function to use
        # if self.mo.m_type == "both":

        if self.reservoir.isotopes:
            self.__execute__ = self.__multiply_with_isotopes__
        else:
            self.__execute__ = self.__multiply_without_isotopes__

    # setup a placeholder call function
    def __call__(self, i: int):
        return self.__execute__(i)

    # use this when we do isotopes
    def __multiply_with_isotopes__(self, i) -> None:
        """Each process is associated with a flux (self.f). Here we replace
        the flux value with the value from the signal object which
        we use as a lookup-table (self.lt)
        """
        # multiply flux mass with signal
        self.f.m[i] = self.f.m[i] * self.lt.m[i]
        self.f.l[i] = self.f.l[i] * self.lt.m[i]
        self.f.h[i] = self.f.m[i] - self.f.l[i]

    def __multiply_without_isotopes__(self, i) -> None:
        """Each process is associated with a flux (self.f). Here we replace
        the flux value with the value from the signal object which
        we use as a lookup-table (self.lt)

        """
        # multiply flux mass with signal
        self.f.m[i] = self.f.m[i] * self.lt.m[i]

    def get_process_args(self):

        func_name: function = self.p_multiply_signal
        data = List([
            self.flux.m,  # 0
            self.flux.l,  # 1
            self.flux.h,  # 2
            self.flux.d,  # 3
            self.lt.m,  # 4
            self.lt.l,  # 5
            self.lt.h,  # 6
            self.lt.d,  # 7
        ])
        params = List([float(self.reservoir.species.element.r)])

        return func_name, data, params

    @staticmethod
    @njit(fastmath=True, error_model="numpy")
    def p_multiply_signal(data, params, i) -> None:

        # flux masses and delta
        # fm: float = data[0][i]
        # fl: float = data[1][i]
        # fh: float = data[2][i]
        # fd: float = data[3][i]

        # signal masses and delta
        # sm: float = data[4][i]
        # sl: float = data[5][i]
        # sd: float = data[7][i]

        data[0][i] = data[0][i] * data[4][i]
        data[1][i] = data[1][i] * data[4][i]
        data[2][i] = data[0][i] - data[1][i]


class PassiveFlux(Process):
    """This process sets the output flux from a reservoir to be equal to
    the sum of input fluxes, so that the reservoir concentration does
    not change. Furthermore, the isotopic ratio of the output flux
    will be set equal to the isotopic ratio of the reservoir The init
    and register methods are inherited from the process class. The
    overall result can be scaled, i.e., in order to create a split flow etc.
    Example::

    PassiveFlux(name = "name",
                reservoir = upstream_reservoir_handle
                scale = optional
                flux = flux handle)

    """
    def __init__(self, **kwargs: Dict[str, any]) -> None:
        """ Initialize this Process """

        # get default names and update list for this Process
        self.__defaultnames__()  # default kwargs names
        self.lrk.extend(["reservoir", "flux"])  # new required keywords
        self.__initerrormessages__()
        # self.bem.update({"rate": "a string"})
        self.__validateandregister__(kwargs)  # initialize keyword values
        # legacy variables
        self.mo = self.reservoir.mo
        self.__postinit__()  # do some housekeeping
        self.__register_name__()

    def __misc_init__(self) -> None:
        """This is just a place holder method which will be called by default
        in __post_init__() This can be overloaded to add additional
        code to the init procedure without the need to redefine
        init. This useful for processes which only define a call method.

        """

        # this process requires delayed init.
        print(f"Added {self.name} to lto")
        self.mo.lto.append(self)

    def __delayed_init__(self) -> None:
        """
        Initialize stuff which is only known after the entire model has been defined.
        This will be executed just before running the model.

        """

        # Create a list of fluxes wich excludes the flux this process
        # will be acting upon

        # print(f"delayed init for {self.name}")
        self.fws: List[Flux] = self.r.lof.copy()
        self.fws.remove(self.f)  # remove this handle

    def __call__(self, i: int) -> None:
        """Here we re-balance the flux. That is, we calculate the sum of all fluxes
        excluding this flux. This sum will be equal to this flux. This will likely only
        work for outfluxes though.

        Should this be done for output fluxes as well?

        """

        new: float = 0.0

        # calc sum of fluxes in fws. Note that at this point, not all fluxes
        # will be known so we need to use the flux values from the previous times-step
        for j, f in enumerate(self.fws):
            # print(f"{f.n} = {f.m[i-1] * reservoir.lio[f]}")
            new += f.m[i - 1] * self.reservoir.lio[f] * self.scale

        # print(f"sum = {new:.0f}\n")

        self.f[i] = get_flux_data(new, self.reservoir.d[i - 1],
                                  self.reservoir.rvalue)


class ScaleRelativeToInputFluxes(PassiveFlux):
    """Scale output flux relative to the input fluxes"""
    def __delayed_init__(self) -> None:
        """
        Initialize stuff which is only known after the entire model has been defined.
        This will be executed just before running the model.

        Specifically, find all input fluxes
        """

        print(f"delayed init for {self.name}")

        self.in_fluxes: list = []
        for i, f in enumerate(self.r.lof):
            if self.r.lodir[i] > 0:
                self.in_fluxes.append(f)

    def __call__(self, i: int) -> None:
        """Here we re-balance the flux. That is, we calculate the sum of all fluxes
        excluding this flux. This sum will be equal to this flux. This will likely only
        work for outfluxes though.

        Should this be done for output fluxes as well?

        """

        new: float = 0.0

        for j, f in enumerate(self.in_fluxes):
            # print(f"{f.n} = {f.m[i-1] * reservoir.lio[f]}")
            new += f.m[i - 1]

        new = new * self.scale
        # print(f"sum = {new:.0f}\n")
        self.f[i] = [new, 1, 1, 1]


class PassiveFlux_fixed_delta(Process):
    """This process sets the output flux from a reservoir to be equal to
    the sum of input fluxes, so that the reservoir concentration does
    not change. However, the isotopic ratio of the output flux is set
    at a fixed value. The init and register methods are inherited
    from the process class. The overall result can be scaled, i.e.,
    in order to create a split flow etc.  Example::

    PassiveFlux_fixed_delta(name = "name",
                            reservoir = upstream_reservoir_handle,
                            flux handle,
                            delta = delta offset)

    """
    def __init__(self, **kwargs: Dict[str, any]) -> None:
        """ Initialize this Process """

        self.__defaultnames__()  # default kwargs names
        self.lrk.extend(["reservoir", "delta",
                         "flux"])  # new required keywords

        self.__initerrormessages__()
        # self.bem.update({"rate": "a string"})
        self.__validateandregister__(kwargs)  # initialize keyword values
        self.__postinit__()  # do some housekeeping

        # legacy names
        self.f: Flux = self.flux
        # legacy variables
        self.mo = self.reservoir.mo

        print(
            "\nn *** Warning, you selected the PassiveFlux_fixed_delta method ***\n "
        )
        print(
            " This is not a particularly phyiscal process is this really what you want?\n"
        )
        print(self.__doc__)
        self.__register_name__()

    def __call__(self, i: int) -> None:
        """Here we re-balance the flux. This code will be called by the
        apply_flux_modifier method of a reservoir which itself is
        called by the model execute method

        """

        r: float = self.reservoir.rvalue  # the isotope reference value

        varflux: Flux = self.f
        flux_list: List[Flux] = self.reservoir.lof.copy()
        flux_list.remove(varflux)  # remove this handle

        # sum up the remaining fluxes
        newflux: float = 0
        for f in flux_list:
            newflux = newflux + f.m[i - 1] * self.reservoir.lio[f]

        # set isotope mass according to keyword value
        self.f[i] = array(get_flux_data(newflux, self.delta, r))


class VarDeltaOut(Process):
    """Unlike a passive flux, this process sets the flux istope ratio
    equal to the isotopic ratio of the reservoir. The
    init and register methods are inherited from the process
    class.

    VarDeltaOut(name = "name",
                reservoir = upstream_reservoir_handle,
                flux = flux handle,
                rate = rate,)

    """

    __slots__ = ("rate", "flux", "reservoir")

    def __init__(self, **kwargs: Dict[str, any]) -> None:
        """Initialize this Process"""

        from . import ureg, Q_
        from .connections import ConnectionGroup
        from esbmtk import Flux, Reservoir, ReservoirGroup

        # get default names and update list for this Process
        self.__defaultnames__()
        self.lkk: Dict[str, any] = {
            "name": str,
            "reservoir": (Reservoir, Source, Sink),
            "flux": Flux,
            "rate": (str, Q_),
            "register":
            (ConnectionGroup, ReservoirGroup, Reservoir, Flux, str),
            "scale": (Number, np.float64, str),
        }
        self.lrk.extend(["reservoir", "flux"])  # new required keywords
        self.__initerrormessages__()
        self.__validateandregister__(kwargs)  # initialize keyword values
        self.mo = self.reservoir.mo
        self.__postinit__()  # do some housekeeping
        self.__register_name__()

        # decide which call function to use
        # if self.mo.m_type == "both":
        if self.reservoir.isotopes:
            # print(
            #    f"vardeltaout with isotopes for {self.reservoir.register.name}.{self.reservoir.name}"
            # )
            if isinstance(self.reservoir, Reservoir):
                # print("Using reservoir")
                self.__execute__ = self.__with_isotopes_reservoir__
            elif isinstance(self.reservoir, Source):
                # print("Using Source")
                self.__execute__ = self.__with_isotopes_source__
            else:
                raise ValueError(
                    f"{self.name}, reservoir must be of type Source or Reservoir, not {type(self.reservoir)}"
                )
        else:
            self.__execute__ = self.__without_isotopes__

    # setup a placeholder call function
    def __call__(self, i: int):
        return self.__execute__(i)

    def __with_isotopes_reservoir__(self, i: int) -> None:
        """Here we re-balance the flux. This code will be called by the
        apply_flux_modifier method of a reservoir which itself is
        called by the model execute method

        """

        m: float = self.flux.m[i]
        if m != 0:
            # if reservoir.register.name == "db":
            #    print(f"{reservoir.name} d={reservoir.d[i-1]}")
            r: float = self.reservoir.species.element.r
            d: float = self.reservoir.d[i - 1]
            l: float = (1000.0 * m) / ((d + 1000.0) * r + 1000.0)
            h: float = m - l

            self.flux[i] = [m, l, h, d]

    def get_process_args(self):
        """Provide the data structure which needs to be passed to the numba solver"""

        # if upstream is a source, we only have a single delta value
        # so we need to patch this. Maybe this should move to source?
        if isinstance(self.reservoir, Source):
            delta = self.reservoir.d
        else:
            delta = self.reservoir.d

        func_name: function = self.p_vardeltaout

        data = List([
            self.flux.m,  # 0
            self.flux.l,  # 1
            self.flux.h,  # 2
            self.flux.d,  # 3
            delta,  # 4
        ])

        params = List([float(reservoir.species.element.r)])

        return func_name, data, params

    @staticmethod
    @njit(fastmath=True, error_model="numpy")
    def p_vardeltaout(data, params, i) -> None:
        # concentration times scale factor

        r: float = params[0]  # r-value
        m: float = data[0][i - 1]  # flux mass
        d: float = data[4][i - 1]  # reservoir delta
        l: float = (1000.0 * m) / ((d + 1000.0) * r + 1000.0)

        data[0][i] = m
        data[1][i] = l
        data[2][i] = m - l
        data[3][i] = d

    def __with_isotopes_source__(self, i: int) -> None:
        """If the source of the flux is a source, there is only a single delta value.
        Changes to the flux delta are applied through the Signal class.

        """

        m: float = self.flux.m[i]
        if m != 0:
            d: float = self.reservoir.delta
            r: float = self.reservoir.species.element.r
            l: float = (1000.0 * m) / ((d + 1000.0) * r + 1000.0)
            h: float = m - l

            self.flux[i] = [m, l, h, d]

    def __without_isotopes__(self, i: int) -> None:
        """Here we re-balance the flux. This code will be called by the
        apply_flux_modifier method of a reservoir which itself is
        called by the model execute method

        """

        pass


class SaveFluxData(Process):
    """This process scales the mass of a flux (m,l,h) relative to another
    flux but does not affect delta. The scale factor "scale" and flux
    reference must be present when the object is being initalized

    Example::
         ScaleFlux(name = "Name",
                   flux = Flux Handle)

    """

    __slots__ = ("flux")

    def __init__(self, **kwargs: Dict[str, any]) -> None:
        """Initialize this Process"""
        # get default names and update list for this Process
        self.__defaultnames__()  # default kwargs names
        self.lrk.extend(["flux"])  # new required keywords

        self.__validateandregister__(kwargs)  # initialize keyword values

        # legacy variables
        self.__postinit__()  # do some housekeeping
        self.__register_name__()

    # setup a placeholder call function
    def __call__(self, i: int):
        self.f[i] = self.fa

    def get_process_args(self):
        """"""

        func_name: function = self.p_save_flux

        data = List([
            self.flux.m,  # 0
            self.flux.l,  # 1
            self.flux.h,  # 2
            self.flux.d,  # 3
            self.fa,  # 4
        ])

        params = List()

        return func_name, data, params

    @staticmethod
    @njit(fastmath=True, error_model="numpy")
    def p_scale_flux(data, params, i) -> None:

        r: float = params[0]  # r value
        s: float = params[1]  # scale

        m: float = data[4][i]  # mass of reference object
        d: float = data[5][i - 1]  # delta of reservoir_ref

        m = m * s
        l: float = (1000.0 * m) / ((d + 1000.0) * r + 1000.0)
        # print(f"ScaleFlux m = {m:.2e}, scale = {proc_const[1]}")

        data[0][i] = data[4][0]
        data[1][i] = data[4][1]
        data[2][i] = data[4][2]
        data[3][i] = data[4][3]


class ScaleFlux(Process):
    """This process scales the mass of a flux (m,l,h) relative to another
    flux but does not affect delta. The scale factor "scale" and flux
    reference must be present when the object is being initalized

    Example::
         ScaleFlux(name = "Name",
                   reservoir = reservoir_handle (upstream or downstream)
                   scale = 1
                   ref_reservoirs = flux we use for scale)

    """

    __slots__ = ("rate", "scale", "ref_reservoirs", "reservoir", "flux")

    def __init__(self, **kwargs: Dict[str, any]) -> None:
        """Initialize this Process"""
        # get default names and update list for this Process
        self.__defaultnames__()  # default kwargs names
        self.lrk.extend(["reservoir", "flux", "scale",
                         "ref_reservoirs"])  # new required keywords

        self.__validateandregister__(kwargs)  # initialize keyword values

        # legacy variables
        self.mo = self.reservoir.mo
        self.__postinit__()  # do some housekeeping
        self.__register_name__()

        if self.ref_reservoirs == "None":
            raise ValueError("You need reference to scale against")

        # decide which call function to use
        # if self.mo.m_type == "both":
        if self.reservoir.isotopes:
            self.__execute__ = self.__with_isotopes__
        else:
            self.__execute__ = self.__without_isotopes__

    # setup a placeholder call function
    def __call__(self, i: int):
        return self.__execute__(i)

    def __with_isotopes__(self, i: int) -> None:
        """Apply the scale factor. This is typically done through the the
        model execute method.
        Note that this will use the mass of the reference object, but that we will set the
        delta according to the reservoir

        """

        m: float = self.ref_reservoirs.m[i] * self.scale
        r: float = self.reservoir.species.element.r
        d: float = self.reservoir.d[i - 1]
        l: float = (1000.0 * m) / ((d + 1000.0) * r + 1000.0)

        self.flux[i]: np.array = [m, l, m - l, d]

    def __without_isotopes__(self, i: int) -> None:
        """Apply the scale factor. This is typically done through the the
        model execute method.
        Note that this will use the mass of the reference object, but that we will set the
        delta according to the reservoir (or the flux?)

        """

        self.f[i] = self.ref_reservoirs[i] * self.scale

    def get_process_args(self):
        """"""

        func_name: function = self.p_scale_flux

        data = List([
            self.flux.m,  # 0
            self.flux.l,  # 1
            self.flux.h,  # 2
            self.flux.d,  # 3
            self.ref_reservoirs.m,  # 4
            self.reservoir.d,  # 5
        ])

        params = List(
            [float(self.reservoir.species.element.r),
             float(self.scale)])

        return func_name, data, params

    @staticmethod
    @njit(fastmath=True, error_model="numpy")
    def p_scale_flux(data, params, i) -> None:

        r: float = params[0]  # r value
        s: float = params[1]  # scale

        m: float = data[4][i]  # mass of reference object
        d: float = data[5][i - 1]  # delta of reservoir_ref

        m = m * s
        l: float = (1000.0 * m) / ((d + 1000.0) * r + 1000.0)
        # print(f"ScaleFlux m = {m:.2e}, scale = {proc_const[1]}")

        data[0][i] = m
        data[1][i] = l
        data[2][i] = m - l
        data[3][i] = d


class Reaction(ScaleFlux):
    """This process approximates the effect of a chemical reaction between
    two fluxes which belong to a differents species (e.g., S, and O).
    The flux belonging to the upstream reservoir will simply be
    scaled relative to the flux it reacts with. The scaling is given
    by the ratio argument. So this function is equivalent to the
    ScaleFlux class.

    Example::

       Connect(source=IW_H2S,
               sink=S0,
               ctype = "react_with",
               scale=1,
               ref_reservoirs = O2_diff_to_S0,
               scale =1,
       )
    """


class FluxDiff(Process):
    """The new flux will be the difference of two fluxes"""
    """This process scales the mass of a flux (m,l,h) relative to another
     flux but does not affect delta. The scale factor "scale" and flux
     reference must be present when the object is being initalized

     Example::
          ScaleFlux(name = "Name",
                    reservoir = upstream_reservoir_handle,
                    scale = 1
                    ref_reservoirs = flux we use for scale)

     """
    def __init__(self, **kwargs: Dict[str, any]) -> None:
        """Initialize this Process"""
        # get default names and update list for this Process
        self.__defaultnames__()  # default kwargs names
        self.lrk.extend(["reservoir", "flux", "scale",
                         "ref_reservoirs"])  # new required keywords

        self.__validateandregister__(kwargs)  # initialize keyword values
        self.__postinit__()  # do some housekeeping

        # legacy variables
        self.mo = self.reservoir.mo
        self.__register_name__()

    def __call__(self, i: int) -> None:
        """Apply the scale factor. This is typically done through the the
        model execute method.
        Note that this will use the mass of the reference object, but that we will set the
        delta according to the reservoir (or the flux?)

        """
        self.f[i] = (self.ref_reservoirs[0][i] -
                     self.ref_reservoirs[1][i]) * self.scale


class Fractionation(Process):
    """This process offsets the isotopic ratio of the flux by a given
       delta value. In other words, we add a fractionation factor

    Example::
         Fractionation(name = "Name",
                       reservoir = upstream_reservoir_handle,
                       flux = flux handle
                       alpha = 12 in permil (e.f)

    """

    __slots__ = ("flux", "reservoir")

    def __init__(self, **kwargs: Dict[str, any]) -> None:
        """ Initialize this Process """
        # get default names and update list for this Process
        self.__defaultnames__()  # default kwargs names
        self.lrk.extend(["reservoir", "flux",
                         "alpha"])  # new required keywords

        self.__validateandregister__(kwargs)  # initialize keyword values
        self.__postinit__()  # do some housekeeping

        # alpha is given in permil, but the fractionation routine expects
        # it as 1 + permil, i.e., 70 permil would 1.007

        self.alp = 1 + self.alpha / 1000
        self.mo = self.reservoir.mo
        self.__register_name__()

    def __call__(self, i: int) -> None:
        """
        Set flux isotope masses based on fractionation factor

        """
        #print(f"self.f.m[i] =  {self.f.m[i]}")
        if self.f.m[i] != 0:
            # get target ratio based on reservoir ratio
            c = (
                self.reservoir.l[i - 1] /
                (self.reservoir.m[i - 1] - self.reservoir.l[i - 1])) / self.alp

            # calculate 32S in flux
            self.f.l[i] = self.f.m[i] * c / (c + 1)
            # retire the next two lines
            self.f.h[i] = self.f.m[i] - self.f.l[i]
            self.f.d[i] = get_delta(self.f.l[i], self.f.h[i],
                                    self.reservoir.species.element.r)
        return

    def get_process_args(self):

        func_name: function = self.p_fractionation

        data = List([
            self.flux.m,  # 0
            self.flux.l,  # 1
            self.flux.h,  # 2
            self.flux.d,  # 3
            self.reservoir.m,  # 4
            self.reservoir.l,  # 5
        ])
        params = List(
            [float(self.reservoir.species.element.r),
             float(self.alp)])

        return func_name, data, params

    @staticmethod
    @njit(fastmath=True, error_model="numpy")
    def p_fractionation(data, params, i) -> None:
        # params
        r: float = params[0]  # rvalue
        a: float = params[1]  # alpha

        # data
        rm: float = data[4][i - 1]  # 4 reservoir mass
        rl: float = data[5][i - 1]  # 4 reservoir light isotope
        fm: float = data[0][i]  # flux mass

        c = (rl / (rm - rl)) / a

        data[1][i] = data[0][i] * c / (c + 1)  # flux li
        data[2][i] = data[0][i] - data[1][i]  # flux hi
        data[3][i] = 1000 * (data[2][i] / data[1][i] - r) / r  # flux d


class RateConstant(Process):
    """This is a wrapper for a variety of processes which depend on rate constants
    Please see the below class definitions for details on how to call them
    At present, the following processes are defined

    ScaleRelativeToNormalizedConcentration
    ScaleRelativeToConcentration

    """

    __slots__ = ("scale", "ref_value", "k_value", "flux", "reservoir")

    def __init__(self, **kwargs: Dict[str, any]) -> None:
        """Initialize this Process"""

        from . import ureg, Q_
        from .connections import SourceGroup, SinkGroup, ReservoirGroup
        from .connections import ConnectionGroup, GasReservoir
        from esbmtk import Flux

        # Note that self.lkk values also need to be added to the lkk
        # list of the connector object.

        # get default names and update list for this Process
        self.__defaultnames__()  # default kwargs names

        # update the allowed keywords
        self.lkk: dict = {
            "scale": (Number, np.float64),
            "k_value": (Number, np.float64),
            "name":
            str,
            "reservoir": (Reservoir, Source, Sink, GasReservoir, np.ndarray),
            "flux":
            Flux,
            "ref_reservoirs":
            list,
            "reservoir_ref": (Reservoir, GasReservoir),
            "left": (list, Reservoir, Number, np.float64, np.ndarray),
            "right": (list, Reservoir, Number, np.ndarray),
            "register": (
                SourceGroup,
                SinkGroup,
                ReservoirGroup,
                ConnectionGroup,
                Flux,
                str,
            ),
            "gas": (Reservoir, GasReservoir, Source, Sink, np.ndarray),
            "liquid": (Reservoir, Source, Sink),
            "solubility": (Number, np.float64),
            "piston_velocity": (Number, np.float64),
            "water_vapor_pressure": (Number, np.float64),
            "ref_species":
            np.ndarray,
            "seawaterconstants":
            any,
            "isotopes":
            bool,
            "function_reference":
            any,
            "f_0": (str),
            "pco2_0": (str),
            "ex":
            Number,
        }

        # new required keywords
        self.lrk.extend([["reservoir", "atmosphere"], ["scale", "k_value"]])

        # dict with default values if none provided
        # self.lod = {r
        self.lod: dict = {"isotopes": False, "function_reference": "None"}

        self.__initerrormessages__()

        # add these terms to the known error messages
        self.bem.update({
            "scale": "a number",
            "reservoir": "Reservoir handle",
            "ref_reservoirs": "List of Reservoir handle(s)",
            "ref_value": "a number or flux quantity",
            "name": "a string value",
            "flux": "a flux handle",
            "left": "list, reservoir or number",
            "right": "list, reservoir or number",
            "function_reference": "A function reference",
        })

        # initialize keyword values
        self.__validateandregister__(kwargs)
        if "reservoir" in kwargs:
            self.mo = self.reservoir.mo
        elif "gas_reservoir" in kwargs:
            self.mo = self.gas_reservoir

        self.__misc_init__()
        self.__postinit__()  # do some housekeeping
        # legacy variables

        self.__register_name__()

        if self.reservoir.isotopes or self.isotopes:
            self.__execute__ = self.__with_isotopes__
        else:
            self.__execute__ = self.__without_isotopes__

    def __postinit__(self) -> "None":
        self.mo = self.reservoir.mo

    # setup a placeholder call function
    def __call__(self, i: int):
        return self.__execute__(i)


class weathering(RateConstant):
    """This process calculates the flux as a function of the upstream
     reservoir concentration C and a constant which describes thet
     strength of relation between the reservoir concentration and
     the flux scaling

     F = f_0 * (scale * C/pco2_0)**ncc

     where C denotes the concentration in the ustream reservoir, k is a
     constant. This process is typically called by the connector
     instance. However you can instantiate it manually as

     weathering(
                       name = "Name",
                       reservoir = upstream_reservoir_handle,
                       reservoir_ref = reference_reservoir (Atmosphere)
                       flux = flux handle,
                       ex = exponent
                       pco2_0 = 280,
                       f_0 = 12 / 17e12
                       Scale =  1000,
    )

    """
    def __misc_init__(self):
        """
        Scale the reference flux into the model flux units
        """

        self.f_0: float = Q_(self.f_0).to(self.mo.f_unit).magnitude
        self.pco2_0 = Q_(self.pco2_0).to("ppm").magnitude * 1e-6

    def __without_isotopes__(self, i: int) -> None:

        # print(
        #    f"f_0={self.f_0}, scale={self.scale}, c={self.reservoir_ref.c[i-1]}, p0={self.pco2_0}, ex={self.ex}"
        # )
        self.flux.m[i] = (
            self.f_0 *
            (self.scale * self.reservoir_ref.c[i - 1] / self.pco2_0)**self.ex)

    def __with_isotopes__(self, i: int) -> None:
        """
        C = M/V so we express this as relative to mass which allows us to
        use the isotope data.

        The below calculates the flux as function of reservoir concentration,
        rather than scaling the flux.
        """

        raise NotImplementedError("weathering has currently no isotope method")
        # c: float = self.reservoir.c[i - 1]
        # if c > 0:  # otherwise there is no flux
        #     m = c * self.scale
        #     r: float = reservoir.species.element.r
        #     d: float = reservoir.d[i - 1]
        #     l: float = (1000.0 * m) / ((d + 1000.0) * r + 1000.0)
        #     self.flux[i]: np.array = [m, l, m - l, d]

    def get_process_args(self):

        func_name: function = self.p_weathering

        data = List([
            self.flux.m,  # 0
            self.flux.l,  # 1
            self.flux.h,  # 2
            self.flux.d,  # 3
            self.reservoir_ref.d,  # 4
            self.reservoir_ref.c,  # 5
            self.reservoir_ref.m,  # 6
        ])
        params = List([
            float(self.reservoir.species.element.r),  # 0
            float(self.scale),  # 1
            float(self.f_0),  # 2
            float(self.pco2_0),  # 3
            float(self.ex),  # 4
        ])

        return func_name, data, params

    @staticmethod
    @njit(fastmath=True, error_model="numpy")
    def p_weathering(data, params, i) -> None:
        # concentration times scale factor
        s: float = params[1]
        f_0: float = params[2]
        pco2_0: float = params[3]
        ex: float = params[4]

        c: float = data[5][i - 1]
        f: float = f_0 * (c * s / pco2_0)**ex
        data[0][i] = f
        # data[3][i] = data[4][i - 1]
        # print(i)
        # print(" ")


class ScaleRelativeToConcentration(RateConstant):
    """This process calculates the flux as a function of the upstream
     reservoir concentration C and a constant which describes thet
     strength of relation between the reservoir concentration and
     the flux scaling

     F = C * k

     where C denotes the concentration in the ustream reservoir, k is a
     constant. This process is typically called by the connector
     instance. However you can instantiate it manually as

     ScaleRelativeToConcentration(
                       name = "Name",
                       reservoir= upstream_reservoir_handle,
                       flux = flux handle,
                       Scale =  1000,
    )

    """
    def __without_isotopes__(self, i: int) -> None:
        m: float = self.reservoir.m[i - 1]
        if m > 0:  # otherwise there is no flux
            # convert to concentration
            c = m / self.reservoir.volume
            f = c * self.scale
            self.flux.m[i] = f

    def __with_isotopes__(self, i: int) -> None:
        """
        C = M/V so we express this as relative to mass which allows us to
        use the isotope data.

        The below calculates the flux as function of self.reservoir concentration,
        rather than scaling the flux.
        """

        c: float = self.reservoir.c[i - 1]
        if c > 0:  # otherwise there is no flux
            m = c * self.scale
            r: float = self.reservoir.species.element.r
            d: float = self.reservoir.d[i - 1]
            l: float = (1000.0 * m) / ((d + 1000.0) * r + 1000.0)
            self.flux[i]: np.array = [m, l, m - l, d]

    def get_process_args(self):

        func_name: function = self.p_scale_relative_to_concentration

        data = List([
            self.flux.m,  # 0
            self.flux.l,  # 1
            self.flux.h,  # 2
            self.flux.d,  # 3
            self.reservoir.d,  # 4
            self.reservoir.c,  # 5
            self.reservoir.m,  # 6
        ])
        params = List([
            float(self.reservoir.species.element.r),
            float(self.scale),
            float(self.reservoir.v),
        ])

        return func_name, data, params

    @staticmethod
    @njit(fastmath=True, error_model="numpy")
    def p_scale_relative_to_concentration(data, params, i) -> None:
        # concentration times scale factor
        r: float = params[0]
        s: float = params[1]
        m: float = data[6][i - 1]
        v: float = params[2]

        if m > 0:
            c: float = m / v
            f: float = c * s
            d: float = data[4][i - 1]  # delta
            l: float = (1000.0 * f) / ((d + 1000.0) * r + 1000.0)
            data[0][i] = f
            data[1][i] = l
            data[2][i] = m - l
            data[3][i] = d


class ScaleRelativeToMass(RateConstant):
    """This process scales the flux as a function of the upstream
     reservoir Mass M and a constant which describes the
     strength of relation between the reservoir mass and
     the flux scaling

     F = F0 *  M * k

     where M denotes the mass in the ustream reservoir, k is a
     constant and F0 is the initial unscaled flux. This process is
     typically called by the connector instance. However you can
     instantiate it manually as

     Note that we scale the flux, rather than compute the flux!

     This is faster than setting a new flux, computing the isotope
     ratio and setting delta. So you either have to set the initial
     flux F0 to 1, or calculate the scale accordingly

     ScaleRelativeToMass(
                       name = "Name",
                       reservoir= upstream_reservoir_handle,
                       flux = flux handle,
                       Scale =  1000,
    )

    """
    def __without_isotopes__(self, i: int) -> None:
        m: float = self.reservoir.m[i - 1] * self.scale
        self.flux.m[i]: float = m

    def __with_isotopes__(self, i: int) -> None:
        """
        this will be called by the Model.run() method

        """
        m: float = self.reservoir.m[i - 1] * self.scale
        r: float = self.reservoir.species.element.r
        d: float = self.reservoir.d[i - 1]
        l: float = (1000.0 * m) / ((d + 1000.0) * r + 1000.0)
        self.flux[i]: np.array = [m, l, m - l, d]

    def get_process_args(self):
        """return the data associated with this object"""

        func_name: function = self.p_scale_relative_to_mass

        data = List([
            self.flux.m,  # 0
            self.flux.l,  # 1
            self.flux.h,  # 2
            self.flux.d,  # 3
            self.reservoir.m,  # 4
            self.reservoir.d,  # 5
        ])

        params = List([float(reservoir.species.element.r), float(self.scale)])

        return func_name, data, params

    @staticmethod
    @njit(fastmath=True, error_model="numpy")
    def p_scale_relative_to_mass(data, params, i) -> None:
        # concentration times scale factor

        r: float = params[0]
        s: float = params[1]
        m: float = data[0][i - 1] * s
        d: float = data[1][i - 1]  # delta
        l: float = (1000.0 * m) / ((d + 1000.0) * r + 1000.0)

        data[0][i] = m
        data[1][i] = l
        data[2][i] = m - l
        data[3][i] = d


class ScaleRelative2otherReservoir(RateConstant):
    """This process scales the flux as a function one or more reservoirs
    constant which describes the
    strength of relation between the reservoir concentration and
    the flux scaling

    F = C1 * C1 * k

    where Mi denotes the concentration in one  or more reservoirs, k is one
    or more constant(s). This process is typically called by the connector
    instance when you specify the connection as

    Connect(source =  upstream reservoir,
              sink = downstream reservoir,
              ctype = "scale_relative_to_multiple_reservoirs"
              ref_reservoirs = [r1, r2, k etc] # you must provide at least one
                                               # reservoir or constant
              scale = a overall scaling factor
           )
    """
    def __misc_init__(self) -> None:
        """Test that self.reservoir only contains numbers and reservoirs"""

        self.rs: list = []
        self.constant: Number = 1

        for r in self.ref_reservoirs:
            if isinstance(r, (Reservoir)):
                self.rs.append(r)
            elif isinstance(r, (Number)):
                self.constant = self.constant * r
            else:
                raise ValueError(
                    f"{r} must be reservoir or number, not {type(r)}")

    def __without_isotopes__(self, i: int) -> None:
        c: float = 1
        for r in self.rs:
            c = c * r.c[i - 1]

        scale: float = c * self.scale * self.constant

        # scale = scale * (scale >= 0)  # prevent negative fluxes.
        self.f[i] = [scale, scale, scale, 1]

    def __with_isotopes__(self, i: int) -> None:
        """
        not sure that this correct WRT isotopes

        """

        raise NotImplementedError(
            "Scale relative to multiple reservoirs is undefined for isotope calculations"
        )

        # c: float = 1
        # for r in self.rs:
        #     c = c * r.c[i - 1]

        # scale: float = c * self.scale * self.constant

        # # scale = scale * (scale >= 0)  # prevent negative fluxes.
        # self.f[i] = [scale, scale, scale, 1]


class Flux_Balance(RateConstant):
    """This process calculates a flux between two reservoirs as a function
    of multiple reservoir concentrations and constants.

    Note that could result in negative fluxes. which might cause
    issues with isotope ratios (untested)

    This will work with equilibrium reactions between two reservoirs where the
    reaction can be described as

    K * [R1] = R[2] * [R3]

    you can have more than two terms on each side as long as they are
    constants or reservoirs

    Equilibrium(
                name = "Name",
                reservoir = reservoir handle,
                left = [] # list with reservoir names or constants
                right = [] # list with reservoir names or constants
                flux = flux handle,
                k_value = a constant, defaults to 1
    )

    """

    # redefine misc_init which is being called by post-init
    def __misc_init__(self):
        """Sort out input variables"""

        Rl: List[Reservoir] = []
        Rr: List[Reservoir] = []
        Cl: List[float] = []
        Cr: List[float] = []
        # parse the left hand side

        em = "left/right values must be constants or reservoirs"
        [self.Rl, self.Cl] = sort_by_type(self.left, [Reservoir, Number], em)
        [self.Rr, self.Cr] = sort_by_type(self.right, [Reservoir, Number], em)

    def __without_isotopes__(self, i: int) -> None:

        kl: NDArray = np.array([1.0, 1.0, 1.0, 1.0])
        kr: NDArray = np.array([1.0, 1.0, 1.0, 1.0])
        scale: NDArray = np.array([1.0, 1.0, 1.0, 1.0])

        # calculate the product of reservoir concentrations for left side
        for r in self.Rl:
            kl *= r[i - 1]
        # multiply with any any constants on the right
        for c in self.Cl:
            kl *= c

        # calculate the product of reservoir concentrations for right side
        for r in self.Rr:
            kr *= r[i - 1]
        # multiply with any any constants on the right
        for c in self.Cr:
            kr *= c

        # set flux
        self.f[i] = (kl - kr) * self.k_value

    def __with_isotopes__(self, i: int) -> None:
        """
        not sure that this correct WRT isotopes

        """

        raise NotImplementedError(
            "Flux Balance is undefined for isotope calculations")


class GasExchange(RateConstant):
    """

    GasExchange(
          gas =GasReservoir, #
          liquid = Reservoir, #,
          ref_species = array of concentrations #
          solubility=Atmosphere.swc.SA_co2 [mol/(m^3 atm)],
          area = area, # m^2
          piston_velocity = m/year
          seawaterconstants = Ocean.swc
          water_vapor_pressure=Ocean.swc.p_H2O,
    )


    """

    # redefine misc_init which is being called by post-init
    def __misc_init__(self):
        """Sort out input variables"""

        self.p_H2O = self.seawaterconstants.p_H2O
        self.a_dg = self.seawaterconstants.a_dg
        self.a_db = self.seawaterconstants.a_db
        self.a_u = self.seawaterconstants.a_u
        self.rvalue = self.liquid.sp.r
        self.volume = self.gas.volume

    def __without_isotopes__(self, i: int) -> None:

        # set flux
        # note that the sink delta is co2aq as returned by the carbonate VR
        # this equation is for mmol but esbmtk uses mol, so we need to
        # multiply by 1E3

        a = self.scale * (  # area in m^2
            self.gas.c[i - 1]  #  Atmosphere
            * (1 - self.p_H2O)  # p_H2O
            * self.solubility  # SA_co2 = mol/(m^3 atm)
            - self.ref_species[i - 1] * 1000  # [CO2]aq mol
        )
        # print(self.gas.c[i - 1])

        # changes in the mass of CO2 also affect changes in the total mass
        # of the atmosphere. So we need to update the reservoir volume
        # variable which we use the store the total atmospheric mass
        # reservoir.v[i] = reservoir.v[i] + a * reservoir.mo.dt
        self.flux[i] = [a, 1, 1, 1]

    def __with_isotopes__(self, i: int) -> None:
        """
        In the following I assume near neutral pH between 7 and 9, so that
        the isotopic composition of HCO3- is approximately equal to the isotopic
        ratio of DIC. The isotopic ratio of [CO2]aq can then be obtained from DIC via
        swc.e_db (swc.a_db)

        The fractionation factor subscripts denote the following:

        g = gaseous
        d = dissolved
        b = bicarbonate ion
        c = carbonate ion

        a_db is thus the fractionation factor between dissolved CO2aq and HCO3-
        and a_gb between CO2g HCO3-
        """

        f = self.scale * (
            self.gas.c[i - 1]  # p Atmosphere
            * (1 - self.p_H2O)  # p_H2O
            * self.solubility  # SA_co2
            - self.ref_species[i - 1] * 1000  # [CO2]aq
        )

        co2aq_c13 = self.ref_species[i - 1] * self.r.h[i - 1] / self.r.m[i - 1]
        co2at_c13 = self.gas.h[i - 1] / self.gas.volume

        f13 = (
            self.scale * self.a_u * (
                self.a_dg * co2at_c13 * (1 - self.p_H2O)  # p_H2O
                * self.solubility  # SA_co2
                - self.a_db * co2aq_c13 * 1000))

        # h = flux!
        f12 = f - f13
        d = (f13 / f12 / self.rvalue - 1) * 1000

        # print(f"f={f:.2e}")
        # print(f"P: f={f:.2e}, f12={f12:.2e}, f13={f13:.2e}, d={d:.2f}")
        self.flux[i] = [f, f12, f13, d]

        # changes in the mass of CO2 also affect changes in the total mass
        # of the atmosphere. So we need to update the reservoir volume
        # variable which we use the store the total atmospheric mass

        # print(f"Name = {reservoir.full_name}")
        # reservoir.v[i] = reservoir.v[i] + f * reservoir.mo.dt

        # raise NotImplementedError()

    def __postinit__(self) -> None:
        """Do some housekeeping for the process class"""

        # legacy name aliases
        self.n: str = self.name  # display name of species
        self.r = self.liquid
        self.reservoir = self.liquid

    def get_process_args(self):
        """return the data associated with this object"""

        func_name: function = self.p_gas_exchange

        data = List([
            self.flux.m,  # 0
            self.flux.l,  # 1
            self.flux.h,  # 2
            self.flux.d,  # 3
            self.liquid.m,  # 4
            self.liquid.h,  # 5
            self.ref_species,  # 6
            self.gas.c,  # 7
            self.gas.h,  # 8
            self.gas.v,  # 9
            self.r.m,  # 10
            self.r.h,  # 11
        ])

        params = List([
            float(self.scale),  # 0
            float(self.solubility * (1 - self.p_H2O)),  # 1
            float(self.rvalue),  # 2
            float(self.gas.volume),  # 3
            float(self.a_u),  # 4
            float(self.a_dg),  # 5
            float(self.a_db),  # 6
            float(self.reservoir.mo.dt),  # 7
            float(self.p_H2O),  # 8
            float(self.solubility),  #9 
        ])

        self.params = params
        return func_name, data, params

    @staticmethod
    @njit(fastmath=True, error_model="numpy")
    def p_gas_exchange(data, params, i) -> None:
        """the below equation moved as many constants as possible outside of
        the function compared to the __with/without_isotopes__ method(s). See the
        __get_process_args__ method for details

        This process does not yet work with variable volumes

        """

        scale: float = params[0]  # scale
        SA: float = params[1]  # solubility
        r: float = params[2]  # r value
        gv: float = params[3]  # gas volume
        au: float = params[4]  #
        dg: float = params[5]  #
        db: float = params[6]  #
        dt: float = params[7]  # dt
        pH2O: float = params[8]  # p_H2O
        solubility: float = params[9]  # solubility

        rs = data[6][i - 1]  # ref species
        rm = data[10][i - 1]
        rh = data[11][i - 1]
        gc = data[7][i - 1]
        gh = data[8][i - 1]  # gas.h

        f = scale * (gc * (1 - pH2O) * solubility - rs * 1000)
        co2aq_c13 = rs * rh / rm  #
        co2at_c13 = gh / gv

        f13 = scale * au * (dg * co2at_c13 *
                            (1 - pH2O) * solubility - db * co2aq_c13 * 1000)
        f12 = f - f13
        d = (f13 / f12 / r - 1) * 1000

        data[0][i] = f
        data[1][i] = f12
        data[2][i] = f13
        data[3][i] = d
        data[9][i] = data[9][i] + f * dt


class Monod(Process):
    """This process scales the flux as a function of the upstream
    reservoir concentration using a Michaelis Menten type
    relationship

    F = F * a * F0 x C/(b+C)

    where F0 denotes the unscaled flux (i.e., at t=0), C denotes
    the concentration in the ustream reservoir, and a and b are
    constants.

    Example::
         Monod(name = "Name",
               reservoir =  upstream_reservoir_handle,
               flux = flux handle ,
               ref_value = reference concentration
               a_value = constant,
               b_value = constant )

    """
    def __init__(self, **kwargs: Dict[str, any]) -> None:
        """"""

        from . import ureg, Q_
        """ Initialize this Process """
        # get default names and update list for this Process
        self.__defaultnames__()  # default kwargs names

        # update the allowed keywords
        self.lkk: dict = {
            "a_value": (Number, np.float64),
            "b_value": (Number, np.float64),
            "ref_value": ((Number, np.float64), str, Q_),
            "name":
            str,
            "reservoir": (Reservoir, Source, Sink),
            "flux":
            Flux,
            "register":
            (SourceGroup, SinkGroup, ReservoirGroup, ConnectionGroup, str),
        }

        self.lrk.extend(["reservoir", "a_value", "b_value",
                         "ref_value"])  # new required keywords

        self.__initerrormessages__()
        self.bem.update({
            "a_value": "a number",
            "b_value": "a number",
            "reservoir": "Reservoir handle",
            "ref_value": "a number",
            "name": "a string value",
            "flux": "a flux handle",
        })

        self.__validateandregister__(kwargs)  # initialize keyword values
        self.__postinit__()  # do some housekeeping
        # legacy variables
        self.mo = self.reservoir.mo
        self.__register_name__()

    def __call__(self, i: int) -> None:
        """
        this willbe called by Model.execute apply_processes
        """

        scale: float = (self.a_value *
                        (self.ref_value * self.reservoir.c[i - 1]) /
                        (self.b_value + self.reservoir.c[i - 1]))

        scale = scale * (scale >= 0)  # prevent negative fluxes.
        self.f[i] + self.f[i] * scale

    def __plot__(self, start: int, stop: int, ref_reservoirs: float, a: float,
                 b: float) -> None:
        """Test the implementation"""

        y = []
        x = range(start, stop)

        for e in x:
            y.append(a * ref_reservoirs * e / (b + e))

        fig, ax = plt.subplots()  #
        ax.plot(x, y)
        # Create a scatter plot for ax
        plt.show()
