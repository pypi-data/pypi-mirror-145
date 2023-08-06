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
from typing import Any, List, Union

from babelplot.backend.specification.plot import plot_e
from babelplot.type.base import babelplot_element_t as base_frame_t
from babelplot.type.base import backend_frame_h, backend_plot_h
from babelplot.type.dimension import FRAME_DIM_FOR_DATA_DIM, dim_e
from babelplot.type.plot import plot_t


@dtcl.dataclass(repr=False, eq=False)
class frame_t(base_frame_t):
    title: str = None
    dim: dim_e = None
    frame_dim: int = dtcl.field(init=False, default=0)
    plot_class: type(plot_t) = dtcl.field(init=False, default=None)
    plots: List[plot_t] = dtcl.field(init=False, default_factory=list)

    def __post_init__(self) -> None:
        """"""
        self.frame_dim = FRAME_DIM_FOR_DATA_DIM[self.dim]

    def AddPlot(
        self,
        type_: Union[str, plot_e, type(backend_plot_h)],
        *args,
        title: str = None,
        **kwargs,
    ) -> plot_t:
        """"""
        plot = self.plot_class(title=title, property=kwargs.copy())
        plot.backend, plot.backend_type = self.NewBackendPlot(
            type_, *args, title=title, **kwargs
        )
        if hasattr(plot, "BackendDefaultProperties"):
            for name, value in plot.BackendDefaultProperties(plot.backend_type).items():
                if name not in plot.property:
                    plot.property[name] = value

        self.plots.append(plot)

        return plot

    def RemovePlot(self, plot: plot_t, /) -> None:
        """"""
        self.plots.remove(plot)
        self.RemoveBackendPlot(plot.backend, self.backend)

    def Clear(self) -> None:
        """"""
        # Do not use a for-loop since self.plots will be modified during looping
        while self.plots.__len__() > 0:
            plot = self.plots[0]
            self.RemovePlot(plot)

    @staticmethod
    def NewBackendPlot(
        frame: frame_t,
        type_: str | plot_e | type(backend_plot_h),
        *args,
        title: str = None,
        **kwargs,
    ) -> tuple[Any, type(backend_plot_h)]:
        """
        The returned object should be backend_plot_h. However, some backends might not have a specific class for each
        plot type. For example, Matplotlib returns an instance of matplotlib.collections.PathCollection when making a
        scatter plot with matplotlib.axes.Axes.scatter.
        """
        raise NotImplemented(
            f"{frame_t.NewBackendPlot.__name__}: Not provided by backend."
        )

    @staticmethod
    def RemoveBackendPlot(plot: backend_plot_h, frame: backend_frame_h, /) -> None:
        """"""
        raise NotImplemented(
            f"{frame_t.RemoveBackendPlot.__name__}: Not provided by backend."
        )
