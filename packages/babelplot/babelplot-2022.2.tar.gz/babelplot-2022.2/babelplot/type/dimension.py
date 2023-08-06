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

from enum import Enum as enum_t
from enum import unique

from babelplot.brick.enum import EnumValues


@unique
class dim_e(enum_t):
    """
    Data Dimension (corresponding frame/plotting dimensions are given by FRAME_DIM_FOR_DATA_DIM)

    C=Channel, T=Time.
    C* corresponds to a channel-less frame of type * with a channel slider.
    T and TY are equivalent to X and XY, respectively.
    T* (other than T and TY) corresponds to a time-less frame of type * with a time slider.
    """

    X = "x"
    XY = "xy"
    XYZ = "xyz"
    #
    CX = "cx"
    CXY = "cxy"
    CXYZ = "cxyz"
    #
    T = "t"
    TY = "ty"
    TXY = "txy"
    TXYZ = "txyz"
    #
    CT = "ct"
    CTY = "cty"
    CTXY = "ctxy"
    CTXYZ = "ctxyz"

    @staticmethod
    def IsValid(description: str, /) -> bool:
        """"""
        return description in VALID_DIMS_AS_STR

    @classmethod
    def NewFromName(cls, description: str, /) -> dim_e:
        """"""
        if description in VALID_DIMS_AS_STR:
            return cls(description)

        raise ValueError(
            f"{description}: Invalid frame dimension. Expected={VALID_DIMS_AS_STR}."
        )


VALID_DIMS_AS_STR = EnumValues(dim_e)


FRAME_DIM_FOR_DATA_DIM = {
    dim_e.X: 1,
    dim_e.XY: 2,
    dim_e.XYZ: 3,
    #
    dim_e.CX: 1,
    dim_e.CXY: 2,
    dim_e.CXYZ: 3,
    #
    dim_e.T: 1,
    dim_e.TY: 2,
    dim_e.TXY: 2,
    dim_e.TXYZ: 3,
    #
    dim_e.CT: 1,
    dim_e.CTY: 2,
    dim_e.CTXY: 2,
    dim_e.CTXYZ: 3,
}
