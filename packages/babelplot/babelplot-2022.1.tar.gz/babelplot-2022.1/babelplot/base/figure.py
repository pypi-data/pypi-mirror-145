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
from multiprocessing import Process as process_t
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from babelplot.backend.base import backend_frame_h, backend_figure_h, has_properties_p
from babelplot.base.frame import frame_t, dim_e


class figure_p(has_properties_p):

    frame_class: type(frame_t) = None

    @staticmethod
    def NewBackendFrame(
        figure: backend_figure_h,
        row: int,
        col: int,
        *args,
        title: str = None,
        dim: dim_e = dim_e.XY,
        **kwargs,
    ) -> backend_frame_h:
        ...

    @staticmethod
    def RemoveBackendFrame(frame: backend_frame_h, figure: backend_figure_h, /) -> None:
        ...

    @staticmethod
    def BackendShow(
        figure: backend_figure_h,
        /,
    ) -> None:
        ...


_unshown_figures = []


def _DefaultShape() -> List[int]:
    """
    Meant to be a mutable Tuple[int, int]
    """
    return [0, 0]


@dtcl.dataclass(repr=False, eq=False)
class figure_t(figure_p):

    title: str = None
    offline_version: bool = False
    frames: List[frame_t] = dtcl.field(init=False, default_factory=list)
    locations: List[Tuple[int, int]] = dtcl.field(init=False, default_factory=list)
    shape: List[int] = dtcl.field(init=False, default_factory=_DefaultShape)
    backend_figure: backend_figure_h = dtcl.field(init=False, default=None)

    def __post_init__(self) -> None:
        """"""
        if not self.offline_version:
            _unshown_figures.append(self)

    def SetProperty(self, name: str, value: Any, /) -> None:
        """"""
        self.BackendSetProperty(self.backend_figure, name, value)

    def SetProperties(self, properties: Dict[str, Any], /) -> None:
        """"""
        for name, value in properties.items():
            self.SetProperty(name, value)

    def Property(self, name: str, /) -> Any:
        """"""
        return self.BackendProperty(self.backend_figure, name)

    def AddFrame(
        self,
        *args,
        title: str = None,
        dim: Union[str, dim_e] = dim_e.XY,
        row: int = 0,
        col: int = 0,
        **kwargs,
    ) -> frame_t:
        """"""
        if isinstance(dim, str):
            dim = dim_e.NewFromName(dim)

        if (where := (row, col)) in self.locations:
            raise ValueError(f"{where}: Frame grid cell already filled")
        if (row < 0) and (col < 0):
            raise ValueError(f"{where}: Grid coordinates cannot be both negative")
        if row < 0:
            row = self.shape[0]
        elif col < 0:
            col = self.shape[1]

        frame = self.frame_class(title=title, dim=dim)
        backend_frame = self.NewBackendFrame(
            self.backend_figure, row, col, *args, title=title, dim=dim, **kwargs
        )
        frame.backend_frame = backend_frame

        self.frames.append(frame)
        self.locations.append((row, col))
        self.shape[0] = max(self.shape[0], row + 1)
        self.shape[1] = max(self.shape[1], col + 1)

        return frame

    def FrameAtLocation(
        self,
        row: int,
        col: int,
        *,
        as_backend: bool = False,
        strict_mode: bool = True,
    ) -> Optional[frame_t]:
        """"""
        if (row < 0) or (col < 0):
            raise ValueError(f"({row},{col}): Row or col cannot be negative.")
        if (row >= self.shape[0]) or (col >= self.shape[1]):
            if strict_mode:
                raise ValueError(
                    f"({row},{col}): Out-of-bound cell coordinates. "
                    f"Expected: row<{self.shape[0]} and col<{self.shape[1]}."
                )
            else:
                return None

        if (where := (row, col)) in self.locations:
            where = self.locations.index(where)
            output = self.frames[where]

            if as_backend:
                return output.backend_frame
            else:
                return output

        return None

    def LocationOfFrame(self, frame: frame_t, /) -> Tuple[int, int]:
        """"""
        if frame not in self.frames:
            raise ValueError(f"{frame}: Not a frame of the figure.")

        where = self.frames.index(frame)

        return self.locations[where]

    def RemoveFrame(self, frame: Union[frame_t, Sequence[int]], /) -> None:
        """"""
        if isinstance(frame, Sequence):
            location = frame
            frame = self.FrameAtLocation(*location)
        else:
            location = self.LocationOfFrame(frame)

        self.frames.remove(frame)
        self.locations.remove(location)

        if self.frames.__len__() > 0:
            max_row = max(_row for _row, _ in self.locations)
            max_col = max(_col for _, _col in self.locations)
            self.shape = [max_row + 1, max_col + 1]
        else:
            self.shape = _DefaultShape()

        self.RemoveBackendFrame(frame.backend_frame, self.backend_figure)

    def Clear(self) -> None:
        """"""
        # Do not use a for-loop since self.frames will be modified during looping
        while self.frames.__len__() > 0:
            frame = self.frames[0]
            self.RemoveFrame(frame)

    def Show(
        self,
        /,
        *,
        modal: bool = True,
    ) -> None:
        """"""
        if self not in _unshown_figures:
            return
        if self.frames.__len__() == 0:
            return

        _unshown_figures.remove(self)

        if hasattr(self, "BackendShowPreparation"):
            self.BackendShowPreparation(
                self.backend_figure, self.shape, self.frames, self.locations
            )

        if modal:
            self.BackendShow(self.backend_figure)
        else:
            thread = process_t(target=lambda: self.BackendShow(self.backend_figure))
            thread.start()


def ShowAllFigures(
    *,
    modal: bool = True,
) -> None:
    """"""
    while _unshown_figures.__len__() > 1:
        _unshown_figures[0].Show(modal=False)
    if _unshown_figures.__len__() > 0:
        _unshown_figures[0].Show(modal=modal)
