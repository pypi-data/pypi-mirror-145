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

from babelplot.backend.implemented import backend_e
from babelplot.backend.plot import plot_e


def PrintUsage() -> None:
    """"""
    print(
        "Usage: python -m babelplot.help parameter_1 [parameter_2...]\n"
        "    parameter_1 can be:\n"
        "        - backends: lists the available backends\n"
        '        - one of the backends listed when calling with parameter_1 being "backends": '
        "requires additional parameters (see below)\n"
        "    parameters_2, when required, can be:\n"
        "        - plots: lists the plots available for the specified backend\n"
        "        - parameters: lists the BabelPlot equivalents of some backend plot parameters"
    )


def Main() -> None:
    """"""
    if (n_arguments := sstm.argv.__len__()) == 1:
        PrintUsage()
    elif n_arguments == 2:
        if sstm.argv[1] == "backends":
            backends = backend_e.FormattedBackends().splitlines()
            backends = (f"    {_lne}" for _lne in backends)
            backends = "\n".join(backends)
            print(f"Available Backends:\n{backends}")
        elif sstm.argv[1] == "plots":
            plots = plot_e.FormattedPlots().splitlines()
            plots = (f"    {_lne}" for _lne in plots)
            plots = "\n".join(plots)
            print(f"Defined BabelPlot Plots:\n{plots}")
        else:
            print(f"{sstm.argv[1]}: Invalid parameter")
            PrintUsage()
    elif n_arguments == 3:
        if backend_e.IsValid(sstm.argv[1]):
            pbe = backend_e.NewFromName(sstm.argv[1])
            backend = mprt.import_module(f"babelplot.backend.{pbe.value}_")
            if sstm.argv[2] == "plots":
                print(f"Available Backend Plots:")
                print(backend.PLOTS)
            elif sstm.argv[2] == "parameters":
                if hasattr(backend, "PARAMETERS_TRANSLATIONS"):
                    translations = []
                    for babelplot, backend in backend.PARAMETERS_TRANSLATIONS.items():
                        translations.append(f"{babelplot} -> {backend}")
                    translations = "\n".join(translations)
                    print(
                        f"Available Backend Parameter Translations (BabelPlot -> {sstm.argv[1]}):\n{translations}"
                    )
                else:
                    print("No Translations Defined")
            else:
                print(f"{sstm.argv[2]}: Invalid parameter")
                PrintUsage()
        else:
            print(f"{sstm.argv[1]}: Invalid backend")
            PrintUsage()


if __name__ == "__main__":
    """"""
    Main()
