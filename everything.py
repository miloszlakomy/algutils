import importlib
import itertools
import os
import sys
import types
from typing import Any

import algutils.switcheroo
import algutils.deep_getattr


class _Everything:
    class _Globals:
        def __getattr__(self, name: str) -> Any:
            try:
                return globals()[name]
            except KeyError:
                raise AttributeError(f"_Globals has no attribute '{name}'")

        def __setattr__(self, name: str, value: Any) -> None:
            globals()[name] = value


    class _LazyImport(algutils.switcheroo.Switcheroo):
        def __init__(self, name: str) -> None:
            super().__init__()

            self._name = name

        def _load_switch_to(self, _unused_attribute_name: str) -> Any:
            module = importlib.import_module(self._name)
            _Everything._LazyImport._populate_module_children(module=module)
            return module

        @staticmethod
        def _populate_module_children(module: types.ModuleType) -> None:
            for child_name in _Everything._get_module_children_names(module=module):
                child_edge = child_name.rpartition(".")[-1]
                if child_edge in dir(module):
                    continue
                lazy_import = _Everything._LazyImport(name=child_name)
                setattr(module, child_edge, lazy_import)

        @staticmethod
        def _lazy_import(name: str) -> None:
            path = name.split(".")
            if len(path) == 1 and name not in globals():
                globals()[name] = _Everything._LazyImport(name=name)
                return

            parent = _Everything._Globals()
            for depth, edge in enumerate(path):
                parent = getattr(parent, edge)
                if isinstance(parent, _Everything._LazyImport):
                    return
                _Everything._LazyImport._populate_module_children(module=parent)

    class _LazyImportAs(algutils.switcheroo.Switcheroo):
        def __init__(self, name: str, as_name: str) -> None:
            super().__init__()

            self._name = name
            self._as_name = as_name

        def _load_switch_to(self, _unused_attribute_name: str) -> Any:
            lazy_import_or_module_or_obj = deep_getattr.deep_getattr(_Everything._Globals(), self._name)
            return deep_getattr.deep_getattr(_Everything._Globals(), self._name)

        @staticmethod
        def _lazy_import_as(name: str, as_name: str) -> None:
            _Everything._LazyImport._lazy_import(name=name)
            if as_name in globals():
                return
            globals()[as_name] = _Everything._LazyImportAs(name=name, as_name=as_name)

    @staticmethod
    def _get_directories_contents(paths):
        contents = set()
        for path in paths:
            try:
                listing = os.listdir(path)
            except (FileNotFoundError, NotADirectoryError):
                continue
            contents.update(listing)
        return contents

    @staticmethod
    def _get_paths_children_names(paths, prefix):
        children_filenames = _Everything._get_directories_contents(paths=paths)
        children_edges = {filename.partition(".")[0] for filename in children_filenames}
        children_names = {f"{prefix}{edge}" for edge in children_edges if str.isidentifier(edge)}
        return children_names

    @staticmethod
    def _get_module_children_names(module):
        module_paths = getattr(module, "__path__", [])
        return _Everything._get_paths_children_names(paths=module_paths, prefix=f"{module.__name__}.")

    @staticmethod
    def _get_toplevel_module_names():
        return (
            _Everything._get_paths_children_names(paths=sys.path, prefix="")
            | set(sys.builtin_module_names)
            | {'__main__'}
         )

    @staticmethod
    def lazy_import_everything() -> None:
        for toplevel_module_name in _Everything._get_toplevel_module_names():
            _Everything._LazyImport._lazy_import(name=toplevel_module_name)

    @staticmethod
    def lazy_import_as(name: str, as_name: str) -> None:
        _Everything._LazyImportAs._lazy_import_as(name=name, as_name=as_name)


_Everything.lazy_import_everything()

_Everything.lazy_import_as("numpy", "np")
_Everything.lazy_import_as("pandas", "pd")

if "nptyping" in globals():
    # python3 -c 'import string, nptyping; print([as_name for as_name in dir(nptyping) if as_name[0] in string.ascii_uppercase])'
    NPTYPING_TYPE_NAMES = ['Bool', 'Bool8', 'Byte', 'Bytes', 'Bytes0', 'CDouble', 'CFloat', 'CLongDouble', 'CLongFloat', 'CSingle', 'Character', 'Complex', 'Complex128', 'Complex64', 'ComplexFloating', 'DType', 'DataFrame', 'Datetime64', 'Double', 'Flexible', 'Float', 'Float16', 'Float32', 'Float64', 'Floating', 'Half', 'Inexact', 'Int', 'Int0', 'Int16', 'Int32', 'Int64', 'Int8', 'IntC', 'IntP', 'Integer', 'InvalidArgumentsError', 'InvalidDTypeError', 'InvalidShapeError', 'InvalidStructureError', 'LongComplex', 'LongDouble', 'LongFloat', 'LongLong', 'NDArray', 'NPTypingError', 'Number', 'Object', 'Object0', 'RecArray', 'Shape', 'Short', 'SignedInteger', 'Single', 'SingleComplex', 'Str0', 'String', 'Structure', 'Timedelta64', 'UByte', 'UInt', 'UInt0', 'UInt16', 'UInt32', 'UInt64', 'UInt8', 'UIntC', 'UIntP', 'ULongLong', 'UShort', 'Unicode', 'UnsignedInteger', 'Void', 'Void0']
    for as_name in NPTYPING_TYPE_NAMES:
        _Everything.lazy_import_as(f"nptyping.{as_name}", as_name)


from typing import *
