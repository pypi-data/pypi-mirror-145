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

from typing import List, Tuple, Union

from matplotlib.gridspec import GridSpec as grid_spec_t
from matplotlib.pyplot import Axes as backend_frame_2d_t
from matplotlib.pyplot import Figure as backend_figure_t
from matplotlib.pyplot import figure as NewBackendFigure
from mpl_toolkits.mplot3d import Axes3D as backend_frame_3d_t

from babelplot.backend.base import backend_plot_h
from babelplot.backend.plot import plot_e, TranslatedArguments, UNAVAILABLE
from babelplot.base.frame import frame_t as base_frame_t
from babelplot.base.frame import dim_e
from babelplot.base.figure import figure_t as base_figure_t
from babelplot.base.plot import plot_t as base_plot_t


NAME = "Matplotlib"


backend_frame_h = Union[backend_frame_2d_t, backend_frame_3d_t]


def _NewFrame(
    figure: backend_figure_t,
    _: int,
    __: int,
    *args,
    title: str = None,
    dim: dim_e = dim_e.XY,
    **kwargs,
) -> backend_frame_h:
    """"""
    if dim is dim_e.XY:
        output = figure.subplots(*args, **kwargs)
    elif dim is dim_e.XYZ:
        # See note below
        output = backend_frame_3d_t(figure, *args, auto_add_to_figure=False, **kwargs)
        figure.add_axes(output)
    else:
        raise NotImplementedError(f"{dim}: Dimension management not implemented yet")
    if title is not None:
        output.set_title(title)

    return output


def _NewPlot(
    frame: frame_t,
    type_: Union[str, plot_e, type(backend_plot_h)],
    *args,
    title: str = None,  # If _, then it is swallowed by kwargs!
    **kwargs,
) -> backend_plot_h:
    """"""
    if isinstance(type_, str):
        if plot_e.IsValid(type_):
            plot_type = plot_e.NewFromName(type_)
            plot_function = plot_type.BackendPlot(frame.frame_dim, NAME, PLOTS)
        # Next, priority is given to 2-D plots... which might be a problem if a 2-D and 3-D frame have plot types with the
        # same name. For example, scatter in 2-D and 3-D.
        elif hasattr(backend_frame_2d_t, type_):
            plot_function = getattr(backend_frame_2d_t, type_)
        elif hasattr(backend_frame_3d_t, type_):
            plot_function = getattr(backend_frame_3d_t, type_)
        else:
            raise TypeError(f"{type_}: Unknown {NAME} graph object.")
    elif isinstance(type_, plot_e):
        plot_function = type_.BackendPlot(frame.frame_dim, NAME, PLOTS)
    else:
        plot_function = type_

    args, kwargs = TranslatedArguments(
        plot_function, args, kwargs, PARAMETERS_TRANSLATIONS
    )
    output = plot_function(frame.backend_frame, *args, **kwargs)

    return output


def _ShowPreparation(
    figure: backend_figure_t,
    shape: List[int],
    frames: List[frame_t],
    locations: List[Tuple[int, int]],
    /,
) -> None:
    """"""
    if frames.__len__() < 2:
        return

    grid_spec = grid_spec_t(*shape, figure=figure)
    bottoms, tops, lefts, rights = grid_spec.get_grid_positions(figure)

    for frame, (row, col) in zip(frames, locations):
        left, bottom, width, height = (
            lefts[col],
            bottoms[row],
            rights[col] - lefts[col],
            tops[row] - bottoms[row],
        )
        frame.backend_frame.set_position((left, bottom, width, height))


def _Show(
    figure: backend_figure_t,
    /,
) -> None:
    """"""
    figure.show()

    event_manager = figure.canvas
    event_manager.mpl_connect("close_event", lambda _: event_manager.stop_event_loop())
    event_manager.start_event_loop()


plot_t: base_plot_t = type("plot_t", (base_plot_t,), {})
frame_t: base_frame_t = type(
    "frame_t", (base_frame_t,), {"plot_class": plot_t, "NewBackendPlot": _NewPlot}
)
figure_t: base_figure_t = type(
    "figure_t",
    (base_figure_t,),
    {
        "frame_class": frame_t,
        "NewBackendFigure": staticmethod(NewBackendFigure),
        "NewBackendFrame": staticmethod(_NewFrame),
        "BackendShowPreparation": staticmethod(_ShowPreparation),
        "BackendShow": staticmethod(_Show),
    },
)


# TODO: change pos_arg_t,... with number of pos args, or tuple of pos arg names, for doc.
#     Or even remove all the parameter definition, which is never used, right?
#     Or simply describe the accepted positional arguments (order and meaning), the keywords ones being defined in
#     the backend documentation (except for their corresponding babelplot translations).


PLOTS = {
    plot_e.SCATTER: (
        UNAVAILABLE,
        backend_frame_2d_t.scatter,
        backend_frame_3d_t.scatter,
    ),
    plot_e.SURFACE: (
        UNAVAILABLE,
        UNAVAILABLE,
        backend_frame_3d_t.plot_surface,
    ),
    plot_e.LEVELSET: (
        UNAVAILABLE,
        UNAVAILABLE,
        backend_frame_3d_t.contour,
    ),
    plot_e.PIE: (
        UNAVAILABLE,
        backend_frame_2d_t.pie,
        UNAVAILABLE,
    ),
    plot_e.BARH: (
        UNAVAILABLE,
        backend_frame_2d_t.barh,
        UNAVAILABLE,
    ),
    plot_e.BARV: (
        UNAVAILABLE,
        backend_frame_2d_t.bar,
        UNAVAILABLE,
    ),
    plot_e.BAR3: (
        UNAVAILABLE,
        UNAVAILABLE,
        backend_frame_2d_t.hist2d,
    ),
}


# TODO: allow several translations: str->str (valid for all plots), (plot_e, Callable, int), and (plot_e, Callable, str)
#     Then look for key in complex to simple order (tuples, then str). Also allow conversion from keyword here to
#     positional in backend.


PARAMETERS_TRANSLATIONS = {
    "color": "c",
    "color_edge": "edgecolors",
    "color_face": "facecolor",
    "color_max": "vmax",
    "color_min": "vmin",
    "color_scaling": "norm",
    "plot_non_finite": "plotnonfinite",
    "size": "s",
    "width_edge": "linewidths",
    #
    (backend_frame_3d_t.scatter, 2): "zs",
    "depth_shade": "depthshade",
}


# From: https://matplotlib.org/stable/api/prev_api_changes/api_changes_3.4.0.html
# *Axes3D automatically adding itself to Figure is deprecated*
#
# New Axes3D objects previously added themselves to figures when they were created, unlike all other Axes
# classes, which lead to them being added twice if fig.add_subplot(111, projection='3d') was called.
#
# This behavior is now deprecated and will warn. The new keyword argument auto_add_to_figure controls the
# behavior and can be used to suppress the warning. The default value will change to False in Matplotlib 3.5,
# and any non-False value will be an error in Matplotlib 3.6.
#
# In the future, Axes3D will need to be explicitly added to the figure
#
# fig = Figure()
# ax = Axes3d(fig)
# fig.add_axes(ax)
#
# as needs to be done for other axes.Axes sub-classes. Or, a 3D projection can be made via:
#
# fig.add_subplot(projection='3d')
