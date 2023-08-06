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

from typing import Callable, Optional, Union

import vedo  # noqa
from numpy import ndarray as array_t
from vedo import Plotter as backend_figure_t  # noqa
from vedo import Volume as volume_t  # noqa

from babelplot.backend.specification.plot import UNAVAILABLE_for_this_DIM, plot_e
from babelplot.type.base import backend_plot_h
from babelplot.type.dimension import dim_e
from babelplot.type.figure import figure_t as base_figure_t
from babelplot.type.frame import frame_t as base_frame_t
from babelplot.type.plot import plot_t as base_plot_t


NAME = "Vedo"


backend_frame_t = backend_figure_t


def _NewFrame(
    figure: backend_figure_t,
    __: int,
    ___: int,
    *args,
    title: str = None,
    dim: dim_e = dim_e.XY,  # If _, then it is swallowed by kwargs!
    **kwargs,
) -> backend_frame_t:
    """"""
    return figure


def _NewPlot(
    frame: frame_t,
    type_: Union[str, plot_e, type(backend_plot_h)],
    plot_function: Optional[Callable],
    *args,
    title: str = None,  # If _, then it is swallowed by kwargs!
    **kwargs,
) -> tuple[backend_plot_h, type(backend_plot_h)]:
    """"""
    if plot_function is None:
        if hasattr(vedo, type_):
            plot_function = getattr(vedo, type_)
        else:
            raise TypeError(f"{type_}: Unknown {NAME} graph object.")

    output = plot_function(*args, **kwargs)
    frame.backend.__iadd__(output)

    return output, type(output)


def _IsoSurface(volume: array_t, iso_value: float, *_, **__) -> None:
    """"""
    return volume_t(volume).isosurface(threshold=[iso_value])


def _Show(
    figure: backend_figure_t,
    /,
) -> None:
    """"""
    figure.show().close()


# noinspection PyTypeChecker
plot_t: base_plot_t = type("plot_t", (base_plot_t,), {})
# noinspection PyTypeChecker
frame_t: base_frame_t = type(
    "frame_t", (base_frame_t,), {"plot_class": plot_t, "NewBackendPlot": _NewPlot}
)
# noinspection PyTypeChecker
figure_t: base_figure_t = type(
    "figure_t",
    (base_figure_t,),
    {
        "frame_class": frame_t,
        "NewBackendFigure": staticmethod(backend_figure_t),
        "NewBackendFrame": staticmethod(_NewFrame),
        "BackendShow": staticmethod(_Show),
    },
)


PLOTS = {
    plot_e.ISOSET: (
        UNAVAILABLE_for_this_DIM,
        UNAVAILABLE_for_this_DIM,
        _IsoSurface,
    ),
}


TRANSLATIONS = {}
