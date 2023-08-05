from typing import Union

from osaft.core.fluids import InviscidFluid, ViscoelasticFluid, ViscousFluid

t_fluid = Union[InviscidFluid, ViscousFluid, ViscoelasticFluid]
