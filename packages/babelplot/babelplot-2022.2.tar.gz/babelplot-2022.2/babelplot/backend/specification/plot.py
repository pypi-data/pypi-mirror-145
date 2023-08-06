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

from enum import Enum as enum_t, unique
from typing import Any, Callable, Dict, Optional, Sequence, Tuple, Union

from babelplot.brick.enum import EnumMembers, EnumValues


UNAVAILABLE_for_this_DIM = None


positional_to_keyword_h = Tuple[Callable, int]
keyword_to_positional_h = Tuple[Callable, str]


@unique
class plot_e(enum_t):
    """
    Available plot types.

    The value of each enum member is the plot name that can be used in place of the enum member in some
    function/method calls.
    """

    SCATTER = "scatter"
    POLYLINE = "polyline"
    POLYLINES = "polylines"
    POLYGONE = "polygone"
    POLYGONES = "polygones"
    SURFACE = "surface"
    LEVELSET = "levelset"
    MESH = "mesh"
    PMESH = "pmesh"
    BARH = "barh"
    BARV = "barv"
    BAR3 = "bar3"
    PIE = "pie"
    IMAGE = "image"

    @classmethod
    def PlotsIssues(cls, plots: dict, /) -> Optional[Sequence[str]]:
        """"""
        issues = []

        for key, value in plots.items():
            if isinstance(key, cls):
                if isinstance(value, tuple):
                    how_defined = PLOT_DESCRIPTION[key]
                    if (n_dimensions := value.__len__()) == (
                        n_required := how_defined[2].__len__()
                    ):
                        for d_idx, for_dim in enumerate(value):
                            if isinstance(
                                for_dim, (type(UNAVAILABLE_for_this_DIM), Callable)
                            ):
                                pass
                            else:
                                issues.append(
                                    f"{key}/{for_dim}: Invalid plot function for dim {how_defined[2][d_idx]}. "
                                    f"Expected=UNAVAILABLE_for_this_DIM or Callable."
                                )
                    else:
                        issues.append(
                            f"{key}/{n_dimensions}: Invalid number of possible dimensions. Expected={n_required}."
                        )
                else:
                    issues.append(
                        f"{key}/{type(value).__name__}: Invalid plot record type. Expected=tuple."
                    )
            else:
                issues.append(
                    f"{key}/{type(key).__name__}: Invalid plot type. Expected={cls.__name__}."
                )

        missing = set(cls.__members__.values()).difference(plots.keys())
        if missing.__len__() > 0:
            missing = str(sorted(_elm.name for _elm in missing))[1:-1].replace("'", "")
            issues.append(f"Missing plot type(s): {missing}")

        if issues.__len__() > 0:
            return issues

        return None

    @classmethod
    def FormattedPlots(cls, /, *, with_descriptions: bool = True) -> str:
        """"""
        members = EnumMembers(cls)
        as_members = str(members)[1:-1].replace("'", "")
        as_names = str(KNOWN_PLOT_TYPES)[1:-1].replace("'", "")

        if with_descriptions:
            descriptions = []
            for member in members:
                description = PLOT_DESCRIPTION[eval(member)]
                arguments = "\n".join(
                    f"    Dim.{_dim}: " + ", ".join(_arg)
                    for _dim, _arg in zip(description[2], description[3])
                )
                descriptions.append(
                    f"{member}: {description[0]}\n{description[1]}\n{arguments}"
                )
            descriptions = "\n\nDescriptions:\n" + "\n".join(descriptions)
        else:
            descriptions = ""

        output = (
            f"As {cls.__name__} members: {as_members}\n"
            f"As names: {as_names}{descriptions}"
        )

        return output

    @staticmethod
    def IsValid(name: str, /) -> bool:
        """"""
        return name in KNOWN_PLOT_TYPES

    @classmethod
    def NewFromName(cls, name: str, /) -> plot_e:
        """"""
        if name in KNOWN_PLOT_TYPES:
            return cls(name)

        raise ValueError(f"{name}: Invalid plot type. Expected={KNOWN_PLOT_TYPES}.")

    def BackendPlot(
        self, frame_dim: int, backend: str, backend_plots: backend_plots_h, /
    ) -> Callable:
        """
        Returns the plot type callable for the given plot_e member (self) and the dimension passed as "frame_dim". The
        available callables are passed as "backend_plots". The name of the backend, passed as "backend", is only used in
        error messages.
        """
        if self in backend_plots:
            description = backend_plots[self]
            if description.__len__() <= frame_dim - 1:
                raise TypeError(
                    f"{self.value}: Invalid {backend} plotting object for a {frame_dim}-dimensional frame."
                )

            description = description[frame_dim - 1]
            if description is UNAVAILABLE_for_this_DIM:
                raise TypeError(
                    f"{self.value}: Unavailable {backend} plotting object for a {frame_dim}-dimensional frame."
                )

            return description

        raise TypeError(f"{self.value}: Unknown {backend} plotting object.")


KNOWN_PLOT_TYPES = EnumValues(plot_e)


backend_plots_per_type_h = Tuple[Union[type(UNAVAILABLE_for_this_DIM), Callable], ...]
backend_plots_h = Dict[type(plot_e), backend_plots_per_type_h]


# The second element of the description is a tuple of the dimensions the plot type is available in
PLOT_DESCRIPTION = {
    # Brief description
    # Description
    # Valid frame dimension(s)
    # For each dimension, brief description of the positional-only arguments
    plot_e.SCATTER: (
        "Set of Points",
        "Each point of a scatter plot is plotted using a so-called marker.",
        (1, 2, 3),
        (("Xs",), ("Xs", "Ys"), ("Xs", "Ys", "Zs")),
    ),
    plot_e.POLYLINE: (
        "Polygonal Chain",
        "A polygonal chain is a connected series of line segments specified by a sequence of points enumerated "
        "consecutively called vertices. "
        "It typically describes an open path. It can have markers like a scatter plot.\n"
        "A polygonal chain may also be called a polygonal curve, polygonal path, polyline, piecewise linear curve, "
        "or broken line.\n"
        "-- Description adapted from Wikipedia, The Free Encyclopedia [https://en.wikipedia.org/wiki/Polygonal_chain].",
        (2, 3),
        (("Xs", "Ys"), ("Xs", "Ys", "Zs")),
    ),
    plot_e.POLYLINES: (
        "Set of Polygonal Chains",
        'See "Polygonal Chain". '
        "Use case: some plotting libraries may deal with sets more efficiently than looping over the chains in Python.",
        (2, 3),
        (("(Xs, ...)", "(Ys, ...)"), ("(Xs, ...)", "(Ys, ...)", "(Zs, ...)")),
    ),
    plot_e.POLYGONE: (
        "Polygone",
        "A polygone is a closed polygonal chain represented as a sequence of vertices "
        "without repetition of the first one at the end of the sequence.",
        (2,),
        (("Xs", "Ys"),),
    ),
    plot_e.POLYGONES: (
        "Set of Polygones",
        'See "Polygone". '
        "Use case: some plotting libraries may deal with sets more efficiently "
        "than looping over the polygones in Python.",
        (2,),
        (("(Xs, ...)", "(Ys, ...)"),),
    ),
    plot_e.SURFACE: (
        "Surface",
        "A surface is defined as an altitude Z computed by a function f for each planar position (X,Y): Z = f(X,Y).",
        (3,),
        (("Xs", "Ys", "Zs"),),
    ),
    plot_e.LEVELSET: (
        "Level Set",
        "A level set is the set of points at which a function f takes a given value V: "
        "{point | f(point)=V} where point=X,Y or X,Y,Z.",
        (2, 3),
        (("Xs", "Ys", "V"), ("Xs", "Ys", "Zs", "V")),
    ),
    plot_e.MESH: ("Triangular Mesh", "", (3,), ((),)),
    plot_e.PMESH: ("Polygonal Mesh", "Use case: probably rare.", (3,), ((),)),
    plot_e.BARH: ("Horizontal Bar Plot", "", (2,), ((),)),
    plot_e.BARV: (
        "Vertical Bar Plot",
        "A vertical bar plot is equivalent to a 2-dimensional histogram.",
        (2,),
        ((),),
    ),
    plot_e.BAR3: (
        "Three-dimensional Bar Plot",
        "A three-dimensional bar plot is equivalent to a 3-dimensional histogram.",
        (3,),
        ((),),
    ),
    plot_e.PIE: ("Pie Plot", "", (2,), ((),)),
    plot_e.IMAGE: (
        "Two-dimensional Image",
        "When plotting a 2-dimensional image in a 3-dimensional frame, a plotting plane specification is required.",
        (2, 3),
        ((),),
    ),
}


def TranslatedArguments(
    plot_function: Callable,
    args: Sequence[Any],
    kwargs: Dict[str, Any],
    translations: Dict[
        Union[keyword_to_positional_h, positional_to_keyword_h, str], Union[str, int]
    ],
    /,
) -> Tuple[Sequence[Any], Dict[str, Any]]:
    """"""
    output_1 = []
    output_2 = {}

    for idx, value in enumerate(args):
        if (key := translations.get((plot_function, idx))) is None:
            output_1.append(value)
        else:
            output_2[key] = value

    from_kwargs_to_args = []
    max_idx = -1
    for key, value in kwargs.items():
        # It is important to search for specific translation first (i.e. (plot_function, key), as opposed to key alone)
        if (idx := translations.get((plot_function, key))) is None:
            output_2[translations.get(key, key)] = value
        else:
            from_kwargs_to_args.append((value, idx))
            max_idx = max(max_idx, idx)
    if max_idx >= (n_output_1 := output_1.__len__()):
        output_1.extend((max_idx - n_output_1 + 1) * [None])
    for value, idx in from_kwargs_to_args:
        output_1[idx] = value

    return output_1, output_2
