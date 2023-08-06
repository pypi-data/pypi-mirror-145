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

from babelplot.type.enum import EnumMembers, EnumValues


# TODO: describe here below the positional arguments of each plot type


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
                pass
                # if isinstance(value, tuple):
                #     if (n_descriptions := value.__len__()) == 4:
                #         # TODO: make sure a description is available for each dimension of the spec
                #         for dim, description in enumerate(value, start=1):
                #             if isinstance(description, tuple):
                #                 if (description_length := description.__len__()) == 2:
                #                     if not isinstance(description[0], Callable):
                #                         issues.append(
                #                             f"{key}/{type(description[0]).__name__}: "
                #                             f"Invalid first description element. Expected=Callable."
                #                         )
                #                     if isinstance(description[1], tuple):
                #                         idx = 0
                #                         while description[1][idx] is pos_arg_t:
                #                             idx += 1
                #                         if any(
                #                             not isinstance(_prm, str)
                #                             for _prm in description[1][idx:]
                #                         ):
                #                             issues.append(
                #                                 f"{key}: Past the (optional) positional argument(s), "
                #                                 f"all arguments must be of type str."
                #                             )
                #                     else:
                #                         issues.append(
                #                             f"{key}/{type(description[1]).__name__}: "
                #                             f"Invalid second description element. Expected=tuple."
                #                         )
                #                 else:
                #                     issues.append(
                #                         f"{key}/{description_length}: Invalid description length. Expected=2."
                #                     )
                #             elif description is not UNAVAILABLE:
                #                 issues.append(
                #                     f"Invalid plot description for dimension {dim} of key {key}. "
                #                     f"Expected=tuple or UNAVAILABLE."
                #                 )
                #     else:
                #         issues.append(
                #             f"{key}/{n_descriptions}: Invalid plot record length. Expected=4."
                #         )
                # else:
                #     issues.append(
                #         f"{key}/{type(value).__name__}: Invalid plot record. Expected=tuple."
                #     )
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
    def FormattedPlots(cls) -> str:
        """"""
        as_members = str(EnumMembers(cls))[1:-1].replace("'", "")
        as_names = str(KNOWN_PLOTS_AS_STR)[1:-1].replace("'", "")

        output = f"As {cls.__name__} members: {as_members}\n" f"As names: {as_names}"

        return output

    @staticmethod
    def IsValid(name: str, /) -> bool:
        """"""
        return name in KNOWN_PLOTS_AS_STR

    @classmethod
    def NewFromName(cls, name: str, /) -> plot_e:
        """"""
        if name in KNOWN_PLOTS_AS_STR:
            return cls(name)

        raise ValueError(f"{name}: Invalid plot type. Expected={KNOWN_PLOTS_AS_STR}.")

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
            if description is UNAVAILABLE:
                raise TypeError(
                    f"{self.value}: Unavailable {backend} plotting object for a {frame_dim}-dimensional frame."
                )

            return description

        raise TypeError(f"{self.value}: Unknown {backend} plotting object.")


KNOWN_PLOTS_AS_STR = EnumValues(plot_e)


# The second element of the description is a tuple of the dimensions the plot type is available in
PLOT_DESCRIPTION = {
    # Brief description
    # Description
    # Valid frame dimension(s)
    # For each dimension, number of positional-only arguments and their brief description
    plot_e.SCATTER: (
        "Set of Points",
        "Each point of a scatter plot is plotted using a so-called marker.",
        (1, 2, 3),
        ((1, "Xs"), (2, "Xs", "Ys"), (3, "Xs", "Ys", "Zs")),
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
        ((2, "Xs", "Ys"), (3, "Xs", "Ys", "Zs")),
    ),
    plot_e.POLYLINES: (
        "Set of Polygonal Chains",
        'See "Polygonal Chain". '
        "Use case: some plotting libraries may deal with sets more efficiently than looping over the chains in Python.",
        (2, 3),
        ((2, "(Xs, ...)", "(Ys, ...)"), (3, "(Xs, ...)", "(Ys, ...)", "(Zs, ...)")),
    ),
    plot_e.POLYGONE: (
        "Polygone",
        "A polygone is a closed polygonal chain represented as a sequence of vertices "
        "without repetition of the first one at the end of the sequence.",
        (2,),
        ((2, "Xs", "Ys"),),
    ),
    plot_e.POLYGONES: (
        "Set of Polygones",
        'See "Polygone". '
        "Use case: some plotting libraries may deal with sets more efficiently "
        "than looping over the polygones in Python.",
        (2,),
        ((2, "(Xs, ...)", "(Ys, ...)"),),
    ),
    plot_e.SURFACE: (
        "Surface",
        "A surface is defined as an altitude Z computed by a function f for each planar position (X,Y): Z = f(X,Y).",
        (3,),
        ((3, "X", "Y", "Z"),),
    ),
    plot_e.LEVELSET: (
        "Level Set",
        "A level set is the set of points at which a function f takes a given value V: "
        "{point | f(point)=V} where point=X,Y or X,Y,Z.",
        (2, 3),
        ((2, "X", "Y", "V"), (3, "X", "Y", "Z", "V")),
    ),
    plot_e.MESH: ("Triangular Mesh", None, (3,), ((0,),)),
    plot_e.PMESH: ("Polygonal Mesh", "Use case: probably rare.", (3,), ((0,),)),
    plot_e.BARH: ("Horizontal Bar Plot", None, (2,), ((0,),)),
    plot_e.BARV: (
        "Vertical Bar Plot",
        "A vertical bar plot is equivalent to a 2-dimensional histogram.",
        (2,),
        ((0,),),
    ),
    plot_e.BAR3: (
        "Three-dimensional Bar Plot",
        "A three-dimensional bar plot is equivalent to a 3-dimensional histogram.",
        (3,),
        ((0,),),
    ),
    plot_e.PIE: ("Pie Plot", None, (2,), ((0,),)),
    plot_e.IMAGE: (
        "Two-dimensional Image",
        "When plotting a 2-dimensional image in a 3-dimensional frame, a plotting plane specification is required.",
        (2, 3),
        ((0,),),
    ),
}


UNAVAILABLE = None


plot_description_h = Callable
backend_plots_per_dim_h = Tuple[Union[type(UNAVAILABLE), plot_description_h], ...]
backend_plots_h = Dict[type(plot_e), backend_plots_per_dim_h]
positional_to_keyword_h = Tuple[Callable, int]
keyword_to_positional_h = Tuple[Callable, str]


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
    output_2 = {translations.get(_key, _key): _val for _key, _val in kwargs.items()}

    for idx, value in enumerate(args):
        if (key := translations.get((plot_function, idx))) is None:
            output_1.append(value)
        else:
            output_2[key] = value

    return output_1, output_2
