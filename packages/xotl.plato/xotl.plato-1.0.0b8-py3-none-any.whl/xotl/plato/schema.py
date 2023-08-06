import collections.abc
import contextlib
import dataclasses
import enum
import sys
import typing as t
from collections import ChainMap
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

from typing_extensions import Annotated, get_args, get_origin
from xotl.tools.context import context
from xotl.tools.names import nameof
from xotl.tools.objects import classproperty, memoized_property

from .base import D, Describable, FullRepr
from .types import (
    BooleanType,
    DateTimeType,
    DateType,
    DurationType,
    FloatType,
    I,
    IntegerType,
    ListType,
    MappingType,
    OptionalType,
    S,
    Selection,
    Shape,
    StringType,
    TupleType,
    Type,
    short_repr,
)

SB = t.TypeVar("SB", bound="SchemaBase")


@dataclass
class SchemaBase(Describable):
    """Base class for schema objects.

    Schema objects are those that can be *statically* cast into `types
    <xotl.plato.types>`:mod:.  These objects can be `dumped <dump>`:meth: using
    the type object obtained with `get_static_type`:meth:.

    """

    if t.TYPE_CHECKING:
        use_type_cache: t.ClassVar[bool] = True

    def __init_subclass__(cls, cached: bool = True, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.use_type_cache = cached

    @classproperty
    def namespace(cls) -> str:  # pragma: no cover
        return "schema"

    @classproperty
    def constructor_name(cls) -> str:  # pragma: no-cover
        return nameof(cls, typed=True, inner=True, full=True)

    @classmethod
    def get_static_type(cls, *, cached: bool = True) -> Type:
        """Get the static type of the schema.

        See `Caching of schema types <schema-base-caching>`:ref: for more
        details of `cached`.

        """
        if cls.use_type_cache and cached:
            res = _STATIC_TYPES_MAP.get(cls)
        else:
            res = None
        if res is None:
            res = SchemaType(cls)
        if cls.use_type_cache:
            _STATIC_TYPES_MAP[cls] = res
        return res

    @classmethod
    def reset_static_type_cache(cls) -> Type:
        """Reset the schema type cache."""
        return cls.get_static_type(cached=False)

    def dump(self) -> t.Mapping[str, t.Any]:  # pragma: no cover
        """Dumps the schema according the `static type <get_static_type>`:any:

        Notice that the SchemaBase makes no provition to ensure its attributes hold type-safe
        values; so you might get errors both from type-constraints or type mismatches.  These
        include ValueError, and TypeError.  Custom dump methods can also raise another kind of
        exceptions, but we recommend using ValueError or TypeError.

        """
        return self.get_static_type().dump(self)

    @classmethod
    def parse(cls: t.Type[SB], raw_value: t.Mapping[str, t.Any]) -> SB:  # pragma: no cover
        """Parse raw_value using the `static type <get_static_type>`:meth:.

        If the `raw_value` you might one of ValueError, TypeError, KeyError, AttributeError, or
        IndexError.  These exceptions are related to the kind of parsing error::

            >>> @dataclass
            ... class Rectangle(SchemaBase):
            ...     box: t.Tuple[int, int, int, int]

            >>> Rectangle.parse({'box': [1, ]})
            Traceback (most recent call last):
            ...
            ValueError: Expected 4 values, got 1

            >>> Rectangle.parse({'x': 1})
            Traceback (most recent call last):
            ...
            KeyError: 'x'

        .. note:: Some types like IntegerType allow both strings and integers; so the following
           will not raise an error (albeit being really weird)::

               >>> Rectangle.parse({'box': "1234"})
               Rectangle(box=(1, 2, 3, 4))

        """
        return cls.get_static_type().parse(raw_value)

    @property
    def full_repr(self):  # pragma: no cover
        """Return the *full representation* of the object.

        The full representation is the same as `dump`:meth: but including the keys ``:ns:`` and
        ``:base:`` which allow reconstruction of the object with `from_full_repr`:class:

        """
        return {
            ":ns:": self.namespace,
            ":base:": self.constructor_name,
            **self.dump(),
        }


class NonRegisteredType(Type[S, I], abstract=True):
    """Base class for types that don't support reconstruction from full_repr."""

    def __init_subclass__(cls, **kwargs):
        kwargs["abstract"] = True
        super().__init_subclass__(**kwargs)


# Schemata are reported as object types, its shape given by the schema's types.
# But internally we use the SchemaType to integrate the parse/dump methods with
# the type ecosystem.
@dataclass(unsafe_hash=True)
class SchemaType(NonRegisteredType[t.Mapping[str, S], SB]):
    schemacls: t.Type[SB]
    shape: Shape[Type] = field(init=False, compare=False, hash=False, default_factory=dict)

    def __post_init__(self):
        self.shape = self.get_shape()
        super().__post_init__()

    def get_shape(self) -> Shape[Type]:
        """Compute a (fresh) copy of the shape of the schema type.

        Most of the type you will access the cached property `shape`:attr:.

        """

        def _get_fields(cls):
            try:
                return dataclasses.fields(cls)
            except TypeError:
                return []

        # To be abel to evaluate the annotation (if it's a string, we need to know the class
        # were the field was defined, because then we can look the module's globals.  But we
        # still want the fields to have the order in the schemacls dataclass.
        classes = list(reversed([base for base in self.schemacls.mro()]))
        shape = {
            field.name: field_type
            for cls in classes
            for field in _get_fields(cls)
            if (field_type := self._get_type_for_attr(field, cls)) is not None
        }
        keys = [f.name for f in dataclasses.fields(self.schemacls)]
        return {attr: attr_type for attr in keys if (attr_type := shape.get(attr))}

    def __repr__(self):  # pragma: no cover
        return f"SchemaType({dict(self.shape)})"

    @classproperty
    def constructor_name(cls) -> str:  # pragma: no cover
        return "object"

    @property
    def simplified_repr(self) -> str:  # pragma: no cover
        shape_args = [f"{name}: {type_.simplified_repr}" for name, type_ in self.shape.items()]
        return f"{self.constructor_name}[{{{', '.join(shape_args)}}}]"

    @property
    def full_repr(self):  # pragma: no cover
        return {
            ":ns:": self.namespace,
            ":base:": self.constructor_name,
            "shape": {name: type_.full_repr for name, type_ in self.shape.items()},
        }

    def parse(self, raw_value: t.Mapping[str, S]) -> SB:
        return self.schemacls(
            **{attr: self.shape[attr].parse(value) for attr, value in raw_value.items()}
        )

    def dump(
        self,
        value: SB,
        *,
        validate: bool = True,
    ) -> t.Mapping[str, S]:
        return {
            attr: type.dump(getattr(value, attr), validate=validate)
            for attr, type in self.shape.items()
        }

    def _get_type_for_attr(
        self,
        field: dataclasses.Field,
        cls: t.Type,
    ) -> t.Optional[Type]:
        """Get the underlying BaseType of an attribute.

        :param attr_name:  The name of the attribute.

        If the underlying form doesn't have a type hint for `attr_name`,
        return None.

        Hints made by `typing_extensions.Annotated`:any: take precedence.  A
        BaseType in the anotations is selected.  No attempt to match the annotated
        type and the BaseType is made.

        If we can't find an appropriate BaseType, return None.  If the annotation
        has more that one possible BaseType, raise a TypeError.

        """
        attr_name = field.name
        if self._needs_custom_type(attr_name):
            return CustomizedAttrType(self.schemacls, attr_name)  # type: ignore
        try:
            annotation = getattr(cls, "__annotations__", {})[field.name]
        except KeyError:
            return None
        else:
            if isinstance(annotation, str):
                annotation = self._eval_annotation(annotation, cls)
            return self._get_type_from_annotation(annotation, attr_name)

    def _eval_annotation(
        self,
        annotation: str,
        cls,
    ) -> t.Any:  # pragma: no cover
        """Evaluates the annotation in the module of the schemacls."""
        module = sys.modules[cls.__module__]
        return eval(annotation, vars(module))

    def _get_type_from_annotation(
        self,
        annotation: t.Any,
        attr_name: str,
    ) -> t.Optional[Type]:
        candidates: t.List[Type] = []
        origin = get_origin(annotation) or annotation
        if origin is Annotated:
            main, *annotations = get_args(annotation)
            types = tuple(arg for arg in annotations if isinstance(arg, Type))
            candidates.extend(types)
            if not types:
                res = self._get_type_from_annotation(main, attr_name)
                if res is not None:
                    candidates.append(res)
        elif isinstance(origin, type) and issubclass(origin, enum.IntEnum):
            return IntEnumType(origin)
        elif isinstance(origin, type) and issubclass(origin, enum.Enum):
            return EnumType(origin)
        elif isinstance(origin, type) and issubclass(origin, SchemaBase):
            if origin._meta.get("abstract"):
                return FullReprType()

            # TODO: Detect recursive structures which are not supported by our
            # Type Language.  In any case Python will reach its recursion limit.
            candidate = origin.get_static_type()
            if candidate is not None:
                candidates.append(candidate)
        elif origin is tuple:
            args = get_args(annotation)
            bases: t.Tuple[Type, ...] = tuple(
                base_type
                for base in args
                if (base_type := self._get_type_from_annotation(base, attr_name)) is not None
            )
            if len(args) == len(bases):
                return TupleType(bases)
        elif origin in (
            list,
            collections.abc.Sequence,
            set,
            collections.abc.Set,
        ):
            arg = get_args(annotation)[0]
            res = self._get_type_from_annotation(arg, attr_name)
            if res is not None:
                candidates.append(ListType(res))
        elif origin is t.Union:
            args = get_args(annotation)
            subtypes = tuple(
                result
                for arg in args
                if arg is not type(None)  # noqa
                if (result := self._get_type_from_annotation(arg, attr_name)) is not None
            )
            if subtypes:
                if any(arg is type(None) for arg in args):  # noqa
                    candidates.extend(OptionalType(t) for t in subtypes)
                else:
                    candidates.extend(subtypes)
        elif origin in (collections.abc.Mapping, dict):
            key_annotation, value_annotation = get_args(annotation)
            key_type = self._get_type_from_annotation(key_annotation, attr_name)
            value_type = self._get_type_from_annotation(value_annotation, attr_name)
            if key_type is not None and value_type is not None:
                candidates.append(MappingType(key_type, value_type))

        active_context = context[_WITH_TEMP_TYPE_MAPS_CONTEXT]
        active_type_map = active_context.get("maps", _PYTHON_TYPES_MAP)
        if not candidates and (base := active_type_map.get(origin)) is not None:
            candidates.append(base())
        if not candidates:
            return None
        else:
            result, *extra = candidates
            if extra:
                raise TypeError(
                    f"Impossible to find a unique type for {attr_name!r} in {self.schemacls}"
                )
            return result

    def _needs_custom_type(self, attr_name):
        return self.schemacls._has_custom_parse_method(
            attr_name
        ) and self.schemacls._has_custom_dump_method(attr_name)


@dataclass
class EnumType(NonRegisteredType[t.Union[str, enum.Enum], enum.Enum]):
    """Allows to dump/parse values of a given `enum.Enum`:class:.

    .. rubric:: Parsing and dumping

    The serialized form is the *name of the member* in the enumeration class.

    `dump`:meth: only accepts values of the enumeration class.  `parse`:meth:
    looks by the name of the member in the enumeration class.

    Example::

       >>> class COLORS(enum.IntEnum):
       ...     RED = 0xFF0000
       ...     GREEN = 0x00FF00
       ...     BLUE = 0x0000FF

       >>> enumtype = EnumType(COLORS)
       >>> enumtype.parse('RED')
       <COLORS.RED: 16711680>

       >>> enumtype.parse(COLORS.BLUE)
       <COLORS.BLUE: 255>

       >>> enumtype.parse(255)
       Traceback (most recent call last):
       ...
       TypeError: Invalid member name 255

    """

    enumcls: t.Type[enum.Enum]

    @classproperty
    def constructor_name(cls) -> str:  # pragma: no cover
        return "str"

    @property
    def simplified_repr(self) -> str:  # pragma: no cover
        return self._base_type.simplified_repr

    @property
    def full_repr(self) -> FullRepr:  # pragma: no cover
        return self._base_type.full_repr

    @memoized_property
    def _base_type(self) -> StringType:  # pragma: no cover
        return StringType(selection=self.selection)

    @memoized_property
    def selection(self) -> Selection:
        return Selection.from_pairs(
            (str(value), name) for name, value in self.enumcls.__members__.items()
        )

    def parse(self, raw_value: t.Union[str, enum.Enum]) -> enum.Enum:
        if isinstance(raw_value, self.enumcls):
            return raw_value
        if not isinstance(raw_value, str):  # pragma: no cover
            raise TypeError(f"Invalid member name {short_repr(raw_value)}")
        try:
            return getattr(self.enumcls, raw_value)
        except AttributeError:  # pragma: no cover
            raise ValueError(f"Unknown member {short_repr(raw_value)} in {self.enumcls!r}")

    def dump(
        self,
        value: enum.Enum,
        *,
        validate: bool = True,
    ) -> str:
        # We must ignore `validate` because `value` must of the right
        # enumeration.
        if not isinstance(value, self.enumcls):  # pragma: no cover
            raise ValueError(f"Unkown value {short_repr(value)} in {self.enumcls!r}")
        return value.name


@dataclass
class IntEnumType(NonRegisteredType[t.Union[str, int], enum.IntEnum]):
    """Allows to dump/parse values of a given IntEnum.

    .. rubric:: Parsing and dumping

    The serialized form is the integer *value of the member* in the enumeration
    class.

    Example::

       >>> class COLORS(enum.IntEnum):
       ...     RED = 0xFF0000
       ...     GREEN = 0x00FF00
       ...     BLUE = 0x0000FF

       >>> enumtype = IntEnumType(COLORS)
       >>> enumtype.dump(COLORS.RED)
       16711680

       >>> enumtype.parse(COLORS.BLUE)
       <COLORS.BLUE: 255>

       >>> enumtype.parse(255)
       <COLORS.BLUE: 255>

    """

    enumcls: t.Type[enum.IntEnum]

    @classproperty
    def constructor_name(cls) -> str:  # pragma: no cover
        return "int"

    @property
    def simplified_repr(self) -> str:  # pragma: no cover
        return self._base_type.simplified_repr

    @property
    def full_repr(self) -> FullRepr:
        return self._base_type.full_repr

    @memoized_property
    def _base_type(self) -> IntegerType:
        return IntegerType(selection=self.selection)

    @memoized_property
    def selection(self) -> Selection:
        return Selection.from_pairs(
            (int(value), name) for name, value in self.enumcls.__members__.items()
        )

    def parse(self, raw_value: t.Union[str, int]) -> enum.IntEnum:
        if isinstance(raw_value, str):
            which = raw_value
        else:
            which = next(
                (name for value, name in self.selection if value == int(raw_value)),
                "",
            )
        try:
            return getattr(self.enumcls, which)
        except AttributeError:  # pragma: no cover
            raise ValueError(f"Unknown member {short_repr(raw_value)} in {self.enumcls!r}")

    def dump(
        self,
        value: enum.IntEnum,
        *,
        validate: bool = True,
    ) -> t.Union[str, int]:
        # We must ignore `validate` because `value` must of the right
        # enumeration.
        if not isinstance(value, self.enumcls):  # pragma: no cover
            raise ValueError(f"Unkown value {short_repr(value)} in {self.enumcls!r}")
        return int(value)


@dataclass
class FullReprType(NonRegisteredType[FullRepr, D]):
    @classproperty
    def constructor_name(cls) -> str:  # pragma: no cover
        return "fullrepr"

    @property
    def simplified_repr(self) -> str:  # pragma: no cover
        return f"fullrepr"

    @property
    def full_repr(self):  # pragma: no cover
        return {}

    def dump(self, value: D, *, validate=True) -> FullRepr:
        return value.full_repr

    def parse(self, raw_value: FullRepr) -> D:
        return Describable.from_full_repr(raw_value)  # type: ignore


# DON'T make this a subclass of BaseType; it is not a type in the language of
# ADR 59 (and it cannot be).  We only need this to customize the *type* of
# form's field that have a ``parse_`` method.
@dataclass(unsafe_hash=False)
class CustomizedAttrType(t.Generic[S, I]):
    schemacls: t.Type[SchemaBase]
    field_name: str

    def __post_init__(self):
        assert self.schemacls._has_custom_parse_method(self.field_name)
        assert self.schemacls._has_custom_dump_method(self.field_name)

    @classproperty
    def constructor_name(cls) -> str:  # pragma: no cover
        return "customized"

    @property
    def simplified_repr(self) -> str:  # pragma: no cover
        return f"customized[{self.field_name}@{self.schemacls.__name__}]"

    @property
    def full_repr(self):  # pragma: no cover
        return {}

    def parse(self, raw_value: S) -> I:
        return getattr(self.schemacls, f"parse_{self.field_name}")(raw_value)

    def dump(self, value: I, *, validate: bool = True) -> S:
        return getattr(self.schemacls, f"dump_{self.field_name}")(value, validate=validate)


_PYTHON_TYPES_MAP: t.MutableMapping[t.Type, t.Callable[[], Type]] = {
    bool: BooleanType,
    int: IntegerType,
    str: StringType,
    float: FloatType,
    date: DateType,
    datetime: DateTimeType,
    timedelta: DurationType,
    Type: FullReprType,
}
_DEFAULT_TYPES_MAP = dict(_PYTHON_TYPES_MAP)


def register_simple_type_map(
    which: t.Type,
    type_factory: t.Callable[[], Type],
) -> None:
    """Register a type factory for SchemaType.

    When casting python types to the type system we use, this registry to know
    which type to instance.

    This can be used to change (globally) the default type builder for a given
    type.

    For instance, if your applications uses pytz_ instead of `zoneinfo`:mod:,
    you can make all your schemata use ``use_pytz`` like this::

       >>> from datetime import datetime
       >>> register_simple_type_map(datetime, lambda: DateTimeType(use_pytz=True))

       >>> @dataclass
       ... class Foo(SchemaBase, cached=False):
       ...     dt: datetime

       >>> st = Foo.get_static_type()
       >>> st.shape['dt'].use_pytz
       True

       >>> reset_simple_type_map(datetime)

       >>> st = Foo.get_static_type()
       >>> st.shape['dt'].use_pytz
       False

    .. _pytz: https://pypi.org/project/pytz/

    """
    _PYTHON_TYPES_MAP[which] = type_factory


def reset_simple_type_map(type: t.Type) -> None:
    """Reset the type map register for the fiven `type`."""
    register_simple_type_map(type, _DEFAULT_TYPES_MAP[type])


@contextlib.contextmanager
def temp_simple_type_map(which: t.Type, type_factory: t.Callable[[], Type]):
    """Return a context manager with temporary simple type mappings.

    Example::

       >>> from datetime import datetime

       >>> @dataclass
       ... class Foo(SchemaBase, cached=False):
       ...     dt: datetime

       >>> st = Foo.get_static_type()
       >>> st.shape['dt'].use_pytz
       False

       >>> with temp_simple_type_map(datetime, lambda: DateTimeType(use_pytz=True)):
       ...     stemp = Foo.get_static_type()
       >>> stemp.shape['dt'].use_pytz
       True

       >>> Foo.get_static_type().shape['dt'].use_pytz
       False

    """
    active_context = context[_WITH_TEMP_TYPE_MAPS_CONTEXT]
    previous_map = active_context.get("maps", _PYTHON_TYPES_MAP)
    current_map = {which: type_factory}
    with context(
        _WITH_TEMP_TYPE_MAPS_CONTEXT,
        maps=ChainMap(current_map, previous_map),
    ):
        yield


_STATIC_TYPES_MAP: t.Dict[t.Type[SchemaBase], Type] = {}

_WITH_TEMP_TYPE_MAPS_CONTEXT = object()
