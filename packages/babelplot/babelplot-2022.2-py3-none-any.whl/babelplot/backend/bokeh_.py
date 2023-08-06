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

from typing import List, Optional, Union

from bokeh.embed import file_html as HTMLofBackendContent  # noqa
from bokeh.layouts import LayoutDOM as backend_content_t  # noqa
from bokeh.layouts import column as NewBackendColLayout  # noqa
from bokeh.layouts import grid as NewBackendGridLayout  # noqa
from bokeh.layouts import row as NewBackendRowLayout  # noqa
from bokeh.models.renderers import GlyphRenderer as backend_plot_t  # noqa
from bokeh.plotting.figure import Figure as backend_frame_t  # noqa
from bokeh.resources import INLINE  # noqa

from babelplot.backend.brick.html import Show as BackendShow
from babelplot.backend.specification.plot import (
    TranslatedArguments,
    UNAVAILABLE_for_this_DIM,
    plot_e,
)
from babelplot.type.dimension import dim_e
from babelplot.type.figure import figure_t as base_figure_t
from babelplot.type.frame import frame_t as base_frame_t
from babelplot.type.plot import plot_t as base_plot_t


NAME = "Bokeh"


backend_figure_t = base_frame_t


def _NewFrame(
    _: backend_figure_t,
    __: int,
    ___: int,
    *args,
    title: str = None,
    dim: dim_e = dim_e.XY,  # If _, then it is swallowed by kwargs!
    **kwargs,
) -> backend_frame_t:
    """"""
    return backend_frame_t(*args, title=title, **kwargs)


def _NewPlot(
    frame: frame_t,
    type_: Union[str, plot_e, type(backend_plot_t)],
    *args,
    title: str = None,  # If _, then it is swallowed by kwargs!
    **kwargs,
) -> tuple[backend_plot_t, type(backend_plot_t)]:
    """"""
    if isinstance(type_, str):
        if plot_e.IsValid(type_):
            plot_type = plot_e.NewFromName(type_)
            plot_function = plot_type.BackendPlot(frame.frame_dim, NAME, PLOTS)
        elif hasattr(backend_frame_t, type_):
            plot_function = getattr(backend_frame_t, type_)
        else:
            raise TypeError(f"{type_}: Unknown {NAME} graph object.")
    elif isinstance(type_, plot_e):
        plot_function = type_.BackendPlot(frame.frame_dim, NAME, PLOTS)
    else:
        plot_function = type_

    args, kwargs = TranslatedArguments(
        plot_function, args, kwargs, PARAMETERS_TRANSLATIONS
    )
    output = plot_function(frame.backend, *args, **kwargs)

    return output, plot_function


def _ContentFromArrangedFrames(
    figure: figure_t, arranged_frames: List[List[Optional[backend_frame_t]]], /
) -> backend_content_t:
    """"""
    if figure.shape[0] > 1:
        if figure.shape[1] > 1:
            output = NewBackendGridLayout(arranged_frames)
        else:
            column = [_row[0] for _row in arranged_frames]
            output = NewBackendColLayout(column)
    else:
        output = NewBackendRowLayout(arranged_frames[0])

    return output


def _HTMLofContent(_, content: backend_content_t, *__, **___) -> str:
    """"""
    return HTMLofBackendContent(content, INLINE)


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
        "NewBackendFrame": staticmethod(_NewFrame),
        "BackendShow": staticmethod(BackendShow),
        "HTMLofContent": staticmethod(_HTMLofContent),
        "ContentFromArrangedFrames": _ContentFromArrangedFrames,
    },
)


PLOTS = {
    plot_e.SCATTER: (
        UNAVAILABLE_for_this_DIM,
        backend_frame_t.scatter,
        UNAVAILABLE_for_this_DIM,
    ),
}


PARAMETERS_TRANSLATIONS = {
    "color_face": "fill_color",
}
