import inspect
import itertools


SPECIAL_METHOD_NAMES = [ "__abs__", "__add__", "__aenter__", "__aexit__", "__aiter__", "__and__", "__anext__", "__annotate__", "__await__", "__bool__", "__buffer__", "__bytes__", "__call__", "__ceil__", "__complex__", "__contains__", "__delattr__", "__delete__", "__delitem__", "__dir__", "__divmod__", "__enter__", "__eq__", "__exit__", "__float__", "__floor__", "__floordiv__", "__format__", "__func__", "__ge__", "__get__", "__getitem__", "__gt__", "__hash__", "__iadd__", "__iand__", "__ifloordiv__", "__ilshift__", "__imatmul__", "__imod__", "__imul__", "__index__", "__init__", "__instancecheck__", "__int__", "__invert__", "__ior__", "__ipow__", "__irshift__", "__isub__", "__iter__", "__itruediv__", "__ixor__", "__le__", "__len__", "__length_hint__", "__lshift__", "__lt__", "__matmul__", "__missing__", "__mod__", "__mro_entries__", "__mul__", "__ne__", "__neg__", "__new__", "__or__", "__pos__", "__pow__", "__radd__", "__rand__", "__rdivmod__", "__release_buffer__", "__repr__", "__reversed__", "__rfloordiv__", "__rlshift__", "__rmatmul__", "__rmod__", "__rmul__", "__ror__", "__round__", "__rpow__", "__rrshift__", "__rshift__", "__rsub__", "__rtruediv__", "__rxor__", "__set__", "__setattr__", "__setitem__", "__str__", "__sub__", "__subclasscheck__", "__subclasses__", "__truediv__", "__trunc__", "__xor__", "clear", "close", "indices", "mro", "replace", "send", "throw"]


class SwitchToUnsetException(ValueError):
    pass


class _Null:
    pass


class Switcheroo:
    def __init__(self, switch_to=_Null, switch_variable_name=None):
        self._switch_to = switch_to
        self._switch_variable_name = switch_variable_name
        self._initial_self_id = id(self)
        self._hide___getattribute__ = _BoolWrapper(False)

    def _load_switch_to(self, _unused_attribute_name):
        return self._switch_to

    def __getattribute__(self, attribute_name):
        self__hide___getattribute__ = super().__getattribute__("_hide___getattribute__")
        if self__hide___getattribute__:
            return super().__getattribute__(attribute_name)

        self__hide___getattribute__.set(True)
        try:
            self._switch_to = self._load_switch_to(attribute_name)
            self._switch()
            return getattr(self, attribute_name)
        finally:
            self__hide___getattribute__.set(False)

    def _switch(self):
        if self._switch_to is _Null:
            raise SwitchToUnsetException(
                "Class `Switcheroo' instance fields cannot be accessed"
                " with `switch_to' unset and `_load_switch_to' not overridden."
            )

        switch_to = self._switch_to
        switch_variable_name = self._switch_variable_name
        initial_self_id = self._initial_self_id

        all_scopes = itertools.chain.from_iterable(
            [frame_info.frame.f_locals, frame_info.frame.f_globals]
            for frame_info in inspect.stack()
        )

        # `self' becomes `self._switch_to' while the `for' is running.
        for scope in all_scopes:
            if switch_variable_name is not None:
                if id(scope.get("self", _Null)) == initial_self_id:
                    scope["self"] = switch_to
                if id(scope.get(switch_variable_name, _Null)) == initial_self_id:
                    scope[switch_variable_name] = switch_to
            else:
                for variable_name, variable_value in scope.items():
                    if id(variable_value) == initial_self_id:
                        scope[variable_name] = switch_to

    @staticmethod
    def _special_method_factory(special_method_name):
        exec_locals = {}
        exec(
            fr"""
class {Switcheroo.__name__}:
    def {special_method_name}(self, *a, **kw):
        # `self.{special_method_name}' becomes `self._switch_to.{special_method_name}'.
        return self.{special_method_name}(*a, **kw)
            """,
            globals=None,
            locals=exec_locals,
        )
        special_method = getattr(exec_locals[Switcheroo.__name__], special_method_name)
        return special_method

    @staticmethod
    def _add_special_method_if_doesnt_exist(special_method_name):
        if getattr(Switcheroo, special_method_name, _Null) is _Null:
            special_method = Switcheroo._special_method_factory(special_method_name)
            setattr(Switcheroo, special_method_name, special_method)


for special_method_name in SPECIAL_METHOD_NAMES:
    Switcheroo._add_special_method_if_doesnt_exist(special_method_name)


class _BoolWrapper:
    def __init__(self, value):
        self.set(value)

    def set(self, value):
        self.value = bool(value)

    def __bool__(self):
        return self.value
