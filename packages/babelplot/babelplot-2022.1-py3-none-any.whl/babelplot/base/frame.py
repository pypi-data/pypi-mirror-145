# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2022)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from __future__ import annotations

import dataclasses as dtcl
from enum import Enum as enum_t
from enum import unique
from typing import Any, Dict, List, Union

from babelplot.backend.base import backend_frame_h, backend_plot_h, has_properties_p
from babelplot.backend.plot import plot_e
from babelplot.base.plot import plot_t
from babelplot.type.enum import EnumValues


@unique
class dim_e(enum_t):
    """
    Data Dimension (corresponding frame/plotting dimensions are given by FRAME_DIM_FOR_DATA_DIM)

    C=Channel, T=Time.
    C* corresponds to a channel-less frame of type * with a channel slider.
    T and TY are equivalent to X and XY, respectively.
    T* (other than T and TY) corresponds to a time-less frame of type * with a time slider.
    """

    X = "x"
    XY = "xy"
    XYZ = "xyz"
    #
    CX = "cx"
    CXY = "cxy"
    CXYZ = "cxyz"
    #
    T = "t"
    TY = "ty"
    TXY = "txy"
    TXYZ = "txyz"
    #
    CT = "ct"
    CTY = "cty"
    CTXY = "ctxy"
    CTXYZ = "ctxyz"

    @staticmethod
    def IsValid(description: str, /) -> bool:
        """"""
        return description in VALID_DIMS_AS_STR

    @classmethod
    def NewFromName(cls, description: str, /) -> dim_e:
        """"""
        if description in VALID_DIMS_AS_STR:
            return cls(description)

        raise ValueError(
            f"{description}: Invalid frame dimension. Expected={VALID_DIMS_AS_STR}."
        )


VALID_DIMS_AS_STR = EnumValues(dim_e)


FRAME_DIM_FOR_DATA_DIM = {
    dim_e.X: 1,
    dim_e.XY: 2,
    dim_e.XYZ: 3,
    #
    dim_e.CX: 1,
    dim_e.CXY: 2,
    dim_e.CXYZ: 3,
    #
    dim_e.T: 1,
    dim_e.TY: 2,
    dim_e.TXY: 2,
    dim_e.TXYZ: 3,
    #
    dim_e.CT: 1,
    dim_e.CTY: 2,
    dim_e.CTXY: 2,
    dim_e.CTXYZ: 3,
}


class frame_p(has_properties_p):

    plot_class: type(plot_t) = None

    @staticmethod
    def NewBackendPlot(
        frame: frame_t,
        type_: Union[str, plot_e, type(backend_plot_h)],
        *args,
        title: str = None,
        **kwargs,
    ) -> backend_plot_h:
        ...

    @staticmethod
    def RemoveBackendPlot(plot: backend_plot_h, frame: backend_frame_h) -> None:
        ...


@dtcl.dataclass(repr=False, eq=False)
class frame_t(frame_p):
    title: str = None
    dim: dim_e = None
    frame_dim: int = dtcl.field(init=False, default=0)
    plots: List[plot_t] = dtcl.field(init=False, default_factory=list)
    backend_frame: backend_frame_h = dtcl.field(init=False, default=None)

    def __post_init__(self) -> None:
        """"""
        self.frame_dim = FRAME_DIM_FOR_DATA_DIM[self.dim]

    def SetProperty(self, name: str, value: Any, /) -> None:
        """"""
        self.BackendSetProperty(self.backend_frame, name, value)

    def SetProperties(self, properties: Dict[str, Any], /) -> None:
        """"""
        for name, value in properties.items():
            self.SetProperty(name, value)

    def Property(self, name: str, /) -> Any:
        """"""
        return self.BackendProperty(self.backend_frame, name)

    def AddPlot(
        self,
        type_: Union[str, plot_e, type(backend_plot_h)],
        *args,
        title: str = None,
        **kwargs,
    ) -> plot_t:
        """"""
        plot = self.plot_class(title=title)
        backend_plot = self.NewBackendPlot(type_, *args, title=title, **kwargs)
        plot.backend_plot = backend_plot

        self.plots.append(plot)

        return plot

    def RemovePlot(self, plot: plot_t, /) -> None:
        """"""
        self.plots.remove(plot)
        self.RemoveBackendPlot(plot.backend_plot, self.backend_frame)

    def Clear(self) -> None:
        """"""
        # Do not use a for-loop since self.plots will be modified during looping
        while self.plots.__len__() > 0:
            plot = self.plots[0]
            self.RemovePlot(plot)
