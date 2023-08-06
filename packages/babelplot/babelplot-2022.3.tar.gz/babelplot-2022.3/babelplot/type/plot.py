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

import dataclasses as dtcl
from typing import Callable, Optional

from babelplot.backend.specification.plot import (
    UNAVAILABLE_for_this_DIM,
    backend_plots_h,
    plot_e,
)
from babelplot.type.base import babelplot_element_t as base_plot_t
from babelplot.type.base import backend_plot_h


@dtcl.dataclass(repr=False, eq=False)
class plot_t(base_plot_t):
    title: str = None
    # See babelplot.type.frame.NewBackendPlot for an explanation
    backend_type: type(backend_plot_h) = dtcl.field(init=False, default=None)


def BackendPlotFromPlotE(
    plot: plot_e, frame_dim: int, backend: str, backend_plots: backend_plots_h, /
) -> Callable:
    """
    Returns the plot type callable for the given plot_e member and the dimension passed as "frame_dim". The available
    callables are passed as "backend_plots". The name of the backend, passed as "backend", is only used in error
    messages.
    """
    if plot in backend_plots:
        description = backend_plots[plot]
        if description.__len__() <= frame_dim - 1:
            raise TypeError(
                f"{plot.value}: Invalid {backend} plotting object for a {frame_dim}-dimensional frame."
            )

        description = description[frame_dim - 1]
        if description is UNAVAILABLE_for_this_DIM:
            raise TypeError(
                f"{plot.value}: Unavailable {backend} plotting object for a {frame_dim}-dimensional frame."
            )

        return description

    raise TypeError(f"{plot.value}: Unknown {backend} plotting object.")


def BackendPlotFromAny(
    spec: str | plot_e | type(backend_plot_h),
    frame_dim: int,
    backend: str,
    backend_plots: backend_plots_h,
    /,
) -> Optional[Callable]:
    """"""
    if isinstance(spec, str):
        if plot_e.IsValid(spec):
            spec = plot_e.NewFromName(spec)
            output = BackendPlotFromPlotE(spec, frame_dim, backend, backend_plots)
        else:
            output = None
    elif isinstance(spec, plot_e):
        output = BackendPlotFromPlotE(spec, frame_dim, backend, backend_plots)
    else:
        output = spec

    return output
