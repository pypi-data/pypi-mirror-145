import typing as t
from datetime import date, datetime, timedelta
from types import MethodType

from xotl.tools.objects import classproperty

Values = t.Union[str, int, float, date, datetime, timedelta]
D = t.TypeVar("D", bound="Describable")
Shape = t.Mapping[str, D]


class _FullRepr(t.Dict[str, t.Union[Values, "_FullRepr"]]):
    pass


FullRepr = t.Dict[str, t.Union[Values, _FullRepr]]
Unset = object()


class Describable:
    def __post_init__(self):
        # This is here only to make it safe to always call `super().__post_init__()` in
        # subclasses of types and schemata.
        pass

    @classproperty
    def namespace(cls) -> t.Optional[str]:  # pragma: no-cover
        """The namespace of describable.

        This is allows to distinguish between branches of the class hierarchy
        that might share some constructors names, but for different classes.

        .. note:: We might have just include the namespace in the constructor
           name, but that also requires changes in the external clients.

        The value None is reserved to subclasses of Type, to avoid issues with
        previous values.

        """
        raise NotImplementedError(f"{cls} didn't implement namespace")

    @classproperty
    def constructor_name(cls) -> str:  # pragma: no-cover
        """The constructor name.

        This is basically the name of the class without is arguments.  It serves
        the purpose of recognizing the object during serialization for the
        external applications.

        """
        raise NotImplementedError(f"{cls} didn't implement constructor_name")

    @property
    def simplified_repr(self) -> str:  # pragma: no-cover
        "A simplified string representation of the type, suitable for humans."
        raise NotImplementedError(f"{self} didn't implement simplified_repr")

    @property
    def full_repr(self) -> FullRepr:  # pragma: no-cover
        """A full dict representation of the type suitable for JSON dumping.

        The result always has the keys ":ns:" set to `namespace`:prop:, and
        ":base:" set to `constructor_name`:prop:.  Other keys depend on the
        specific object.

        """
        raise NotImplementedError(f"{self} didn't implement full_repr")

    def __init_subclass__(cls, abstract: bool = False, **kwargs):
        super().__init_subclass__(**kwargs)
        if abstract:
            return
        name = cls.constructor_name
        ns = cls.namespace
        _REGISTRY[(ns, name)] = cls  # type: ignore

    @classproperty
    def _meta(cls):
        name = cls.constructor_name
        ns = cls.namespace
        return {"abstract": not bool(_REGISTRY.get((ns, name)))}

    @classmethod
    def from_full_repr(cls: t.Type[D], full_repr: FullRepr) -> D:
        """Reconstruct the Type Object from its full representation."""
        # This is a bit unfortunate, we have to treat Type and SchemaBase
        # specially because we implement Type's full_repr in terms of Type's own
        # parsing/dumping facilities.  In some sense Describable, could be
        # completely replaced by SchemaBase.
        #
        # This makes creating new type objects and schemata less verbose (just
        # do `git blame` and see that we removed lots of
        # `_from_full_repr_args_*` methods); at the cost of making the code of
        # SchemaBase more complex.
        from .schema import SchemaBase
        from .types import Type

        try:
            cls = _REGISTRY[(full_repr.get(":ns:"), full_repr[":base:"])]  # type: ignore
        except KeyError as cause:
            raise TypeError(f"Invalid full_repr {full_repr!r}") from cause
        if issubclass(cls, (SchemaBase, Type)):
            args = {
                arg: val for arg, val in full_repr.items() if arg[0] != ":" and arg[-1] != ":"
            }
            return cls.get_static_type().parse(args)
        else:
            args = {
                arg: cls._from_full_repr_arg(arg, val)
                for arg, val in full_repr.items()
                if arg[0] != ":" and arg[-1] != ":"
            }
            return cls(**args)

    @classmethod
    def _has_custom_parse_method(cls, field_name: str) -> bool:
        method = getattr(cls, f"parse_{field_name}", None)
        return method is not None and isinstance(method, MethodType)

    @classmethod
    def _has_custom_dump_method(cls, field_name: str) -> bool:
        method = getattr(cls, f"dump_{field_name}", None)
        return method is not None and isinstance(method, MethodType)

    @classmethod
    def _from_full_repr_arg(cls, arg, val, *, _default=Unset):
        def _impl(val):
            if isinstance(val, (str, int, float, date, timedelta, bool)):
                return val
            elif isinstance(val, Describable):  # pragma: no cover
                return val
            elif val is None:
                return val
            if isinstance(val, dict) and ":ns:" in val and ":base:" in val:
                return cls.from_full_repr(val)
            elif isinstance(val, tuple):
                return tuple(_impl(item) for item in val)
            elif isinstance(val, list):
                return [_impl(item) for item in val]
            elif isinstance(val, dict):
                return {key: _impl(item) for key, item in val.items()}
            elif isinstance(val, set):
                return {_impl(item) for item in val}
            elif _default is not Unset:
                return _default
            else:  # pragma: no cover
                raise ValueError(f"Unknown type representation argument {arg}={val}")

        method = getattr(cls, f"_from_full_repr_arg_{arg}", None)
        if method is not None:
            return method(val)
        return _impl(val)


_REGISTRY: t.Dict[t.Tuple[t.Optional[str], str], t.Type[Describable]] = {}
