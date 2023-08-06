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

import ast
import importlib as mprt
import inspect as insp
import sys as sstm
from pathlib import Path as path_t
from types import FunctionType as function_type_t
from types import ModuleType as module_type_t
from typing import Dict, Optional, Sequence, Tuple, TypeVar, Union

from babelplot.backend.plot import plot_e


py_module_h = TypeVar("py_module_h")  # str such as module.submodule
module_path_t = str

parameter_type_t = str
parameter_annotation_h = TypeVar("parameter_annotation_h")
default_value_h = TypeVar("default_value_h")
returned_annotation_h = TypeVar("returned_annotation_h")

parameter_wo_name_h = Tuple[parameter_type_t, parameter_annotation_h, default_value_h]
parameter_w_name_h = Tuple[
    parameter_type_t, parameter_annotation_h, default_value_h, str
]
parameter_h = Union[parameter_wo_name_h, parameter_w_name_h]
parameters_h = Tuple[parameter_h, ...]
signature_h = Tuple[parameters_h, returned_annotation_h]


def CalledBackendMethods(py_module: py_module_h, target_class: str, /) -> Sequence[str]:
    """"""
    output = []

    spec = mprt.util.find_spec(py_module)
    with open(spec.origin) as accessor:
        tree = ast.parse(accessor.read())

    for main_node in ast.iter_child_nodes(tree):
        if isinstance(main_node, ast.ClassDef) and (main_node.name == target_class):
            for node in ast.walk(main_node):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and isinstance(node.func.value, ast.Name)
                ):
                    record = node.func
                    called = record.attr
                    context = record.value.id
                    if (context == "self") and ("Backend" in called):
                        output.append(called)
            break

    return tuple(sorted(set(output)))


def DefinedBackendMethods(
    module: Union[py_module_h, module_path_t],
    imported: module_type_t,
    target_class: str,
    /,
    *,
    should_keep_empty: bool = False,
) -> Dict[str, signature_h]:
    """"""
    output = {}

    if not hasattr(imported, target_class):
        raise ValueError(f'{module}: Does not define a "{target_class}" class')

    target_class = getattr(imported, target_class)
    for name in dir(target_class):
        attribute = getattr(target_class, name)

        if name == "__dict__":
            for key, value in attribute.items():
                if insp.isfunction(value) and ("Backend" in key):
                    # Method added through type(...) => do not test non-emptiness
                    output[key] = FunctionSignature(value)
        elif (
            insp.isfunction(attribute)
            and ("Backend" in name)
            and (_FunctionIsNotEmpty(attribute) or should_keep_empty)
        ):
            output[name] = FunctionSignature(attribute)

    return output


def _FunctionIsNotEmpty(function: function_type_t, /) -> bool:
    """"""
    return not insp.getsource(function).endswith("...\n")


def FunctionSignature(
    function: function_type_t, /, *, should_include_name: bool = False
) -> signature_h:
    """"""
    signature = insp.signature(function)

    parameters = []
    for name, parameter in signature.parameters.items():
        record = (
            parameter.kind.description,
            parameter.annotation,
            parameter.default,
        )
        if should_include_name:
            record += (name,)
        parameters.append(record)

    # /!\ Curiously, returned None => returned signature is "None" instead of None
    return (
        tuple(parameters),
        signature.return_annotation,
    )


_LABEL_TO_RANK = {1: "st", 2: "nd", 3: "rd"}


def SignaturePairIssues(
    signa: signature_h, ture: signature_h, /
) -> Optional[Sequence[str]]:
    """"""
    issues = []

    if (n_signa := signa[0].__len__()) != (n_ture := ture[0].__len__()):
        issues.append(f"{n_signa} != {n_ture}: Numbers of parameters do not match")
    for label, (param, eter) in enumerate(zip(signa[0], ture[0]), start=1):
        if param[:2] != eter[:2]:
            rank = _LABEL_TO_RANK.get(label, "th")
            if param[0] == eter[0]:
                issues.append(
                    f"{param[1]} != {eter[1]}: {label}{rank}-parameter annotations do not match"
                )
            else:
                issues.append(
                    f"{param[:2]} != {eter[:2]}: {label}{rank} parameters do not match"
                )
    # str(...): To avoid false mismatch detection between None and "None", for example
    if str(signa[1]) != str(ture[1]):
        issues.append(f"{signa[1]} != {ture[1]}: Return annotations do not match")

    if issues.__len__() > 0:
        return issues

    return None


def CheckBackend(backend: Union[py_module_h, module_path_t], /) -> None:
    """"""
    backend_path = path_t(backend)
    if backend_path.is_file():
        py_backend = backend_path.stem
        spec = mprt.util.spec_from_file_location(py_backend, backend_path)
        imported = mprt.util.module_from_spec(spec)
        sstm.modules[py_backend] = imported
        spec.loader.exec_module(imported)
    else:
        imported = mprt.import_module(backend)

    for reference, target_class in zip(
        ("babelplot.base.plot", "babelplot.base.frame", "babelplot.base.figure"),
        ("plot_t", "frame_t", "figure_t"),
    ):
        print(f"--- {target_class}")
        required = CalledBackendMethods(reference, target_class)
        how_required = DefinedBackendMethods(
            reference,
            mprt.import_module(reference),
            target_class,
            should_keep_empty=True,
        )
        how_defined = DefinedBackendMethods(backend, imported, target_class)

        missing = []
        for name in required:
            if name in how_defined:
                if name in how_required:
                    signa = how_required[name]
                    ture = how_defined[name]
                    issues = SignaturePairIssues(signa, ture)
                    if issues is not None:
                        print(f"{name}:\n    ", "\n    ".join(issues), sep="")
            else:
                missing.append(name)

        print("Missing required method(s):", str(missing)[1:-1].replace("'", ""))

    if hasattr(imported, "PLOTS"):
        defined = getattr(imported, "PLOTS")
        if isinstance(defined, dict):
            issues = plot_e.PlotsIssues(defined)
            if issues is not None:
                print(f"--- PLOTS:\n    ", "\n    ".join(issues), sep="")
        else:
            print(
                f'--- {type(defined).__name__}: Invalid type for "PLOTS". Expected=dict.'
            )
    else:
        print('--- Missing "PLOTS" dictionary')


if __name__ == "__main__":
    #
    if sstm.argv.__len__() < 2:
        print(
            "Missing backend argument\n"
            "(can be an absolute path to a Python module or "
            "a module specification such as module.submodule)"
        )
    else:
        CheckBackend(sstm.argv[1])
