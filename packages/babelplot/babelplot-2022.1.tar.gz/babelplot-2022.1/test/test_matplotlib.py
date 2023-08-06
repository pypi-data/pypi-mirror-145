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

# From: https://matplotlib.org/3.5.1/gallery/lines_bars_and_markers/scatter_demo2.html
import matplotlib.cbook as cbook
import matplotlib.cm as cm
import numpy as nmpy

from babelplot import NewBabelPlotFigure, ShowAllFigures


price_data = cbook.get_sample_data("goog.npz", np_load=True)["price_data"].view(
    nmpy.recarray
)
price_data = price_data[-250:]
delta1 = nmpy.diff(price_data.adj_close) / price_data.adj_close[:-1]
volume = (15 * price_data.volume[:-2] / price_data.volume[0]) ** 2
close = 0.003 * price_data.close[:-2] / 0.003 * price_data.open[:-2]
#
X = nmpy.arange(-5, 5, 0.25)
Y = nmpy.arange(-5, 5, 0.25)
X, Y = nmpy.meshgrid(X, Y)
R = nmpy.sqrt(X**2 + Y**2)
Z = nmpy.sin(R)
#
# from pathlib import Path as path_t
figure = (
    NewBabelPlotFigure()
)  # pbe=path_t("/home/eric/Code/brick/abc/babelplot/babelplot/backend/matplotlib_.py"))
#
frame = figure.AddFrame()
frame.AddPlot("scatter", delta1[:-1], delta1[1:], size=volume, color=close, alpha=0.5)
#
frame_3d = figure.AddFrame(dim="xyz", col=1)
frame_3d.AddPlot(
    "scatter", delta1[:-1], delta1[1:], delta1[1:], size=volume, color=close, alpha=0.5
)
#
frame_3d = figure.AddFrame(dim="xyz", col=2)
frame_3d.AddPlot("surface", X, Y, Z, cmap=cm.cool_r, linewidth=0, antialiased=False)
#
backend_frame = frame.backend_frame
backend_frame.set_xlabel(r"$\Delta_i$", fontsize=15)
backend_frame.set_ylabel(r"$\Delta_{i+1}$", fontsize=15)
backend_frame.set_title("Volume and percent change")
backend_frame.grid(True)
#
figure.backend_figure.tight_layout()


ShowAllFigures()
