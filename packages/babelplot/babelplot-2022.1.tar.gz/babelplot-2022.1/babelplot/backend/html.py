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

from typing import List, Optional

from PySide6.QtWebEngineWidgets import QWebEngineView as widget_t
from PySide6.QtWidgets import QApplication as application_t

from babelplot.backend.base import backend_frame_h
from babelplot.base.figure import figure_t


def Show(figure: figure_t, /) -> None:
    """"""
    if figure.frames.__len__() > 1:
        arranged_frames: List[List[Optional[backend_frame_h]]]
        arranged_frames = [figure.shape[1] * [None] for _ in range(figure.shape[0])]
        for frame, (row, col) in zip(figure.frames, figure.locations):
            arranged_frames[row][col] = frame.backend_frame

        content = figure._ContentFromArrangedFrames(arranged_frames)
    else:
        content = figure.frames[0].backend_frame
    html = figure._HTMLofContent(figure.backend_figure, content)

    # The application must be instantiated in the same thread/process as the one running exec()
    if (application := application_t.instance()) is None:
        application = application_t()

    widget = widget_t()
    widget.setHtml(html)
    widget.show()

    application.exec()
