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

import importlib as mprt
import sys as sstm
from pathlib import Path as path_t
from typing import Any, Dict, Optional, Tuple, Union

from babelplot.backend.base import backend_plot_h
from babelplot.backend.implemented import backend_e
from babelplot.backend.plot import plot_e

from babelplot.base.figure import figure_t
from babelplot.base.frame import dim_e, frame_t
from babelplot.base.plot import plot_t


def NewBabelPlotFigure(
    *args,
    title: str = None,
    offline_version: bool = False,
    pbe: Union[str, path_t, backend_e] = None,
    **kwargs,
) -> figure_t:
    """
    pbe: str=installed module, path_t=path to module, backend_e=implemented backend
    """
    if pbe is None:
        pbe = backend_e.MATPLOTLIB
    elif isinstance(pbe, str) and backend_e.IsValid(pbe):
        pbe = backend_e.NewFromName(pbe)

    if isinstance(pbe, str):
        backend = mprt.import_module(pbe)
    elif isinstance(pbe, path_t):
        module_name = pbe.stem
        spec = mprt.util.spec_from_file_location(module_name, pbe)
        backend = mprt.util.module_from_spec(spec)
        sstm.modules[module_name] = backend
        spec.loader.exec_module(backend)
    else:
        try:
            backend = mprt.import_module(f"babelplot.backend.{pbe.value}_")
        except ModuleNotFoundError:
            print(
                f"{pbe.value}: Unusable backend. Might be due to backend not being installed."
            )
            sstm.exit(1)

    instance = backend.figure_t(title=title, offline_version=offline_version)
    if hasattr(instance, "NewBackendFigure"):
        instance.backend_figure = instance.NewBackendFigure(*args, **kwargs)
    else:
        instance.backend_figure = instance

    return instance


def NewBabelPlot(
    type_: Union[str, plot_e, type(backend_plot_h)],
    *plt_args,
    fig_args=(),
    frm_args=(),
    fig_kwargs: Dict[str, Any] = None,
    frm_kwargs: Dict[str, Any] = None,
    fig_title: str = None,
    frm_title: str = None,
    plt_title: str = None,
    dim: Union[str, dim_e] = dim_e.XY,
    pbe: Union[str, path_t, backend_e] = None,
    should_show: bool = True,
    modal: bool = True,
    **plt_kwargs,
) -> Optional[Tuple[figure_t, frame_t, plot_t]]:
    """"""
    if fig_kwargs is None:
        fig_kwargs = ({},)
    if frm_kwargs is None:
        frm_kwargs = ({},)
    if plt_kwargs is None:
        plt_kwargs = ({},)

    figure = NewBabelPlotFigure(
        *fig_args,
        title=fig_title,
        pbe=pbe,
        **fig_kwargs,
    )
    frame = figure.AddFrame(
        *frm_args,
        title=frm_title,
        dim=dim,
        **frm_kwargs,
    )
    plot = frame.AddPlot(
        type_,
        *plt_args,
        title=plt_title,
        **plt_kwargs,
    )

    if should_show:
        figure.Show(modal=modal)

    if should_show and modal:
        return None

    return figure, frame, plot


# def CloseFigure(figure: figure_t, /)->None:
#     """"""


# def CloseAllFigures()->None:
#     """"""
