import importlib
import itertools
import os
import sys
from typing import Any


class _Everything:
    class _Globals:
        def __getattr__(self, name: str) -> Any:
            try:
                return globals()[name]
            except KeyError:
                raise AttributeError(f"_Globals has no attribute '{name}'")

        def __setattr__(self, name: str, value: Any) -> None:
            globals()[name] = value


    class _LazyImport:
        def __init__(self, name: str, parent) -> None:
            self._name = name
            self._parent = parent

        def __getattr__(self, attribute_name: str) -> Any:
            module = importlib.import_module(self._name)
            edge = self._name.rpartition(".")[-1]
            setattr(self._parent, edge, module)
            for child_name in _Everything._get_module_children_names(module=module):
                _Everything._LazyImport._lazy_import(name=child_name)
            return getattr(module, attribute_name)

        @staticmethod
        def _lazy_import(name: str) -> None:
            path = name.split(".")
            parent = _Everything._Globals()
            for depth, edge in enumerate(path):
                if isinstance(parent, _Everything._LazyImport):
                    return
                try:
                    parent = getattr(parent, edge)
                    # Returns if the entire name has been traversed.
                except AttributeError:
                    lazy_import = _Everything._LazyImport(
                        name=".".join(path[: depth + 1]),
                        parent=parent,
                    )
                    setattr(parent, edge, lazy_import)
                    return

    class _LazyImportAs:
        def __init__(self, name: str, as_name: str) -> None:
            self._name = name
            self._as_name = as_name

        def __getattr__(self, attribute_name: str) -> Any:
            attribute = getattr(globals()[self._name], attribute_name)
            globals()[self._as_name] = globals()[self._name]
            return attribute

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
