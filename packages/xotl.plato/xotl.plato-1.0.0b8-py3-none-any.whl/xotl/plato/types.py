# This code has been taken from
# https://gitlab.merchise.org/mercurio-2018/xhg2/-/blob/master/sources/dists/xhg.ca.website/xhg/ca/xhg_ca_catalog_types/types.py
# and modified to include ranges in MinMax types.
#
# Original copyright is: Copyright (c) Merchise Autrement [~º/~] and Contributors
#
# LICENSE of the original code is the MIT License
#

"""Type System.

We need a simple type system which allows to communicate the different types
of variables a survey can have.  For instance, ratings which is simply a
restricted ``IntegerType(1, 5)``.

Types are objects that allow to capture the basic structure of other objects
(values).

So a type lives two lives:

- When is just a value to be sent to frontends so they can choose the right
  widget for some value.

- As a serializer/parser of values of the type.

Validation is considered *secondary* while parsing a serialized value.

"""
from __future__ import annotations

import dataclasses
import typing as t
import warnings
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone

from xotl.tools.objects import classproperty

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo  # type: ignore

try:
    import pytz
except ImportError:
    pytz = None  # type: ignore

import immutables
from hypothesis import strategies
from hypothesis.strategies import SearchStrategy as Strategy
from xotl.tools.objects import memoized_property
from xotless.ranges import Bound, Excluded, Included, Range
from xotless.types import TOrd

from .base import Describable, Shape

T = t.TypeVar("T")
Ty = t.TypeVar("Ty", bound="Type")


#: See `Type.gettypeattr`:meth:
PathItem = t.Union[str, int, None]

#: See `Type.traverse`:meth:
Path = t.Sequence[PathItem]

# Notes about serialization/deserialization of values
#
# We assume the serialization is done from a Python type to a *simpler* type
# system (int, str, float, list, dicts) which is compatible with
# `json.dumps`:func:.
#
# Each Type Object is then associated with two (meta)types: the S
# (serialized) type and the I (internalized) type.  For instance, DatetimeType
# use str for S, and Python's datetime for I; ObjectType use dicts of
# serialized types for S, and dicts of internal types for I.
#
# So the `parse` signature is `parse(raw: S) -> I`, meaning it will take
# serialized value and return a internalized value.  The `dump` signature is
# always the reverse `dump(value: I) -> S`.
S = t.TypeVar("S")
I = t.TypeVar("I")  # noqa


class Type(t.Generic[S, I], Describable, abstract=True):
    """The base class for all types.

    Types have a basic API to allow them to be easily described.  The property
    `full_repr`:prop: yields basic representation of the type.

    """

    @classmethod
    def get_static_type(cls) -> Type:
        # This closes the loop in our type systems and we can use our type
        # system to describe the type objects.
        from .schema import SchemaType

        return SchemaType(cls)

    @property
    def depth(self) -> int:  # pragma: no-cover
        """The depth a type is a measure of the complexity of a type.

        Basically, types that don't take other other type objects have depth 1,
        while types that take others types increase the depth by one.  We made
        an exception with `OptionalType`:class:, which keeps the same depth as
        its underlying type object.

        """
        raise NotImplementedError

    # Serialization/deserialization API
    def parse(self, raw_value: S) -> I:  # pragma: no-cover
        "Parse a value in the Serial representation, and return an Internal type."
        raise NotImplementedError

    def dump(self, value: I, *, validate: bool = True) -> S:  # pragma: no-cover
        """Take a value of Internal type and return its serial representation.

        If `validate` is True, `value` must abide any possible restriction of
        the type, otherwise it must only type-compatible with this type
        object.

        """
        raise NotImplementedError

    # Testing facilities
    def get_strategy(self) -> Strategy[I]:  # pragma: no cover
        """Return a hypothesis strategy that yields values for the type.

        All values generated from the strategy must be `dumpable <dump>`:any:
        by the type object, this means that the following must never fail::

           >>> import warnings
           >>> from xotl.plato.testing import types as type_objects
           >>> with warnings.catch_warnings():
           ...     typeobj = type_objects.example()
           ...     value = typeobj.get_strategy().example()
           >>> typeobj.dump(value, validate=True)  # doctest: +SKIP

        """
        raise NotImplementedError

    def get_serialized_form_strategy(self) -> Strategy[S]:
        """Return a hypothesis strategy that yields serialized forms for the type.

        All values generated from the strategy must be `parseable <parse>`:any:
        by the type object, this means that the following must never fail::

           >>> import warnings
           >>> from xotl.plato.testing import types as type_objects
           >>> with warnings.catch_warnings():
           ...     typeobj = type_objects.example()
           ...     serial = typeobj.get_serialized_form_strategy().example()
           >>> typeobj.parse(serial)  # doctest: +SKIP

        .. note:: The default implementation is simply to `map`__ `get_strategy`:meth: with
           `dump`:meth:.

        __ https://hypothesis.readthedocs.io/en/latest/data.html#mapping

        """
        return self.get_strategy().map(self.dump)

    # Not really sub-typing
    def __le__(self, other: Type[S, I]) -> bool:
        """Test whether this type kind of a sub-type of `other`.

        This is a very restrictive subtyping relation.  However, the following
        MUST hold:

        - Reflexive: ``t <= t`` for all types ``t``.

        - Transitive: If ``a <= b`` and ``b <= c``, then ``a <= c``.

        - Antisymmetric: If ``a <= b`` and ``a != b``, then it cannot be
          ``b <= a``.

        - If ``t1 <= t2``, then for all value ``v: t1``, ``v: t2`` must also
          hold.

        """
        if isinstance(other, Type):
            return self == other
        return NotImplemented

    def __ge__(self, other: Type[S, I]) -> bool:
        if isinstance(other, Type):
            return other <= self
        return NotImplemented

    def __lt__(self, other):
        return NotImplemented

    __gt__ = __lt__

    @classproperty
    def namespace(cls) -> t.Optional[str]:
        return None  # None is reserved for types.

    def replace(self: Ty, **new_attrs) -> Ty:  # pragma: no cover
        attrs = dataclasses.asdict(self)
        attrs.update(new_attrs)
        return type(self)(**attrs)

    @property
    def full_repr(self):
        return {
            ":ns:": self.namespace,
            ":base:": self.constructor_name,
            **self.get_static_type().dump(self),
        }

    def gettypeattr(self, typeattr: PathItem) -> Type:
        """Get the type of the given *attribute* of this type.

        Composite types (e.g ``object[{'a': int[str]}]``) can be peeked-into to
        obtaing different parts of the its value.  This method and
        `traverse`:meth: are the equivalent type-level traversing operation.

        Examples::

           >>> t1 = TupleType((ObjectType({'a0': ListType(IntegerType())}),
           ...                 OptionalType(StringType())))

           >>> t1.gettypeattr(1)
           OptionalType(StringType())

           >>> t1.traverse((0, 'a0', None))
           IntegerType()

        Primitives types are not traversable and the raise an AttributeError::

           >>> IntegerType().gettypeattr('a')  # doctest: +ELLIPSIS
           Traceback (most recent call last):
           ...
           AttributeError: ...

        Invalid could also raise IndexError, KeyError or AttributeError
        (depending on the actual type object)::

           >>> t1.gettypeattr(10)
           Traceback (most recent call last):
           ...
           IndexError: ...

        To traverse a MappingType, either use 'keys', 'values', or 'items'::

           >>> mt = MappingType(StringType(), IntegerType())
           >>> mt.gettypeattr('keys')
           StringType()

           >>> mt.gettypeattr('items')
           TupleType((StringType(), IntegerType()))

        To traverse a ListType and OptionalType use None.

        """
        raise AttributeError(
            f"Type object {self.simplified_repr!s} doesnt have type-attribute '{typeattr}'"
        )

    def traverse(self, path: Path) -> Type:
        """Get the type obtained by looking at a given `path`.

        This operation is basically the application of `gettypeattr`:meth: many
        times.

        """
        res = self
        for attr in path:
            res = res.gettypeattr(attr)
        return res

    def iter_typeattrs(self) -> t.Iterator[t.Tuple[PathItem, Type]]:
        """Return an iterator with pairs of inner types.

        Types which take no other types, yield nothing::

           >>> list(IntegerType().iter_typeattrs())
           []

        Higher-level types yields as many tuples as needed::

           >>> list(ListType(OptionalType(IntegerType())).iter_typeattrs())
           [(None, OptionalType(IntegerType()))]

           >>> list(ObjectType({'int': IntegerType(), 'str': StringType()}).iter_typeattrs())
           [('int', IntegerType()), ('str', StringType())]

           >>> list(OptionalType(StringType()).iter_typeattrs())
           [(None, StringType())]

           >>> list(ListType(StringType()).iter_typeattrs())
           [(None, StringType())]

           >>> list(TupleType((StringType(), IntegerType())).iter_typeattrs())
           [(0, StringType()), (1, IntegerType())]

        The first item is always compatible with `gettypeattr`:meth:.

        """
        return
        yield


@dataclass(unsafe_hash=True)
class BooleanType(Type[bool, bool]):
    @classproperty
    def constructor_name(cls) -> str:
        return "boolean"

    @property
    def simplified_repr(self) -> str:
        return self.constructor_name

    depth: t.ClassVar[int] = 1

    # Serialization/deserialization API
    def parse(self, raw_value: bool) -> bool:
        if isinstance(raw_value, bool):
            return raw_value
        else:
            raise TypeError(f"Invalid BooleanType {raw_value}")

    def dump(self, value: bool, *, validate: bool = True) -> bool:
        if isinstance(value, bool):
            return value
        else:
            raise TypeError(f"Invalid BooleanType {value}")

    def get_strategy(self) -> Strategy[bool]:
        return strategies.booleans()

    def __le__(self, other):
        if isinstance(other, Type):
            return isinstance(other, BooleanType)
        return NotImplemented


@dataclass(unsafe_hash=True)
class SelectionData(t.Generic[T]):
    "The data of a selection item."
    name: t.Optional[str]
    value: T

    # This allows to treat SelectionData as a tuple of (value, name)
    def __iter__(self):
        yield self.value
        yield self.name


class Selection(tuple, t.Sequence[SelectionData[T]]):
    """A specialized `tuple`:class: for selections."""

    @classmethod
    def from_pairs(
        cls,
        data: t.Iterable[t.Tuple[T, t.Optional[str]]],
    ) -> Selection[T]:
        """Build the selection for an iterable of pairs of ``(value, name)``."""
        return cls(SelectionData(name, value) for value, name in data)

    def get_name(self, by_value: T) -> t.Optional[str]:
        """Return the 'name' of given value in the selection.

        .. doctest::

           >>> sel = Selection.from_pairs([(1, "one"), (2, "two")])
           >>> sel.get_name(1)
           'one'

           >>> sel.get_name(10) is None
           True

        """
        for value, name in self:
            if value == by_value:
                return name
        return None

    def get_values(self) -> t.Sequence[T]:
        "Return the sequence of all values in the selection."
        return tuple(value for value, _ in self)

    def __le__(self, other):
        """A selection maintains type-identity only by equality of its value."""
        if isinstance(other, Selection):
            self_values = {v for v, _ in self}
            other_values = {v for v, _ in other}
            return self_values <= other_values
        return NotImplemented


class Selectable(t.Generic[T]):
    """Mixin for types that support a selection.

    Type objects that allow selections, can be initialized with an argument
    `selection` with a sequence of `SelectionData`:class: objects describing
    each possible value.

    """

    if t.TYPE_CHECKING:
        selection: t.Optional[t.Sequence[SelectionData[T]]]

    @property
    def selection_args(self):
        if self.selection is not None:
            res = ", ".join(
                f"{s.value} as {s.name!r}" if s.name else str(s.value) for s in self.selection
            )
        else:
            res = ""
        if res:
            return (f"selection=[{res}]",)
        else:
            return ()

    def _ensure_value_in_selection(self, value: T):
        "Raise a ValueError is value is not valid in the selection"
        if self.selection and not any(sel.value == value for sel in self.selection):
            raise ValueError(
                f"Unexpected value {short_repr(value)}, is not a valid value of {self.selection_args}"
            )

    def _apply_selection_strategy(
        self,
        strategy: Strategy[T],
        *,
        only_filter: bool = False,
    ) -> Strategy[T]:
        from hypothesis import strategies

        if selection := self.selection:
            values = {value for value, _ in selection}
            if not only_filter:
                return strategies.sampled_from(tuple(values))
            else:
                return strategy.filter(lambda v: v in values)
        return strategy

    def _le_selectable(self, other):
        if isinstance(other, Selectable):
            # Notice that a selection acts a constraint *reducing* the space of possible
            # values; so `self.selection` is None means no constraints and thus is the entire
            # universe of possible values.  That's why when we have no selection constraint
            # other cannot have a selection constraint.
            #
            # Of course, this is only partially correct; because the following type would be
            # equivalent::
            #
            #    IntegerType(1, 5)
            #    IntegerType(selection=[1, 2, 3, 4])
            #
            # But they are not sub-types; because we don't try to enumerate all possible items
            # in the underlying type.  You would have to do clever things to check, say,
            # IntegerType(0, 2**10000**100) (even trying to compute that number takes a very
            # long time).
            if self.selection is None:
                return other.selection is None
            return other.selection is None or self.selection <= other.selection
        return NotImplemented

    @classmethod
    def dump_selection(
        cls,
        value: t.Optional[t.Sequence[SelectionData[T]]],
        *,
        validate: bool = True,
    ):
        if value is not None:
            return [{"value": s.value, "name": s.name} for s in value]
        else:
            return None

    @classmethod
    def parse_selection(cls, raw_value):
        if raw_value is not None:
            return Selection.from_pairs((item["value"], item["name"]) for item in raw_value)
        else:
            return None


class MinMax(t.Generic[TOrd]):
    "Mixin for types that support a min/max constraint."
    min_value: t.Optional[TOrd] = None
    max_value: t.Optional[TOrd] = None
    min_included: bool = True
    max_included: bool = False

    @property
    def minmax_args(self):
        args = ()
        if self.min_value is not None:
            op = ">=" if self.min_included else ">"
            args += (f"min{op}{self.dump(self.min_value, validate=False)}",)
        if self.max_value is not None:
            op = "<=" if self.max_included else "<"
            args += (f"max{op}{self.dump(self.max_value, validate=False)}",)
        return args

    @memoized_property
    def range(self) -> Range[TOrd]:
        min_value = self.min_value
        lower = Bound.normalized_lower_bound(
            min_value,
            Included if self.min_included else Excluded,
        )
        upper = Bound.normalized_upper_bound(
            self.max_value,
            Included if self.max_included else Excluded,
        )
        return Range(lower, upper)

    @property
    def minmax_repr_args(self):
        args, kwargs = (), {}
        if self.min_value is not None:
            args += (self.dump(self.min_value, validate=False),)
        elif self.max_value is not None:
            # We must include the min_value when there is max_value, eg.
            # IntegerType(None, max_value)
            args += (None,)
        if self.max_value is not None:
            args += (self.dump(self.max_value, validate=False),)
        # Only include the values which are not the defaults
        if not self.min_included and self.min_value is not None:
            kwargs["min_included"] = self.min_included
        if self.max_included and self.max_value is not None:
            kwargs["max_included"] = self.max_included
        return args, kwargs

    def _ensure_value_in_range(self, value: TOrd):
        if value not in self.range:
            raise ValueError(f"Value {short_repr(value)} not in {self.range!r}")

    def __repr__(self):
        args, kw = self.minmax_repr_args
        res = f"{type(self).__name__}("
        if args or kw:
            if args:
                res += ", ".join(f"{arg!r}" for arg in args)
                if kw:
                    res += ", "
            if kw:
                res += ", ".join(f"{name}={val!r}" for name, val in kw.items())
        res += ")"
        return res

    def _le_minmax(self, other):
        if isinstance(other, MinMax):
            return self.range <= other.range
        return NotImplemented

    # This is only a minimal value to generate values, is not stored in the
    # type.  But we enfore the limit for values and hypothesis strategies.
    MIN_POSSIBLE_VALUE: t.ClassVar[t.Optional[t.Any]] = None

    def _get_min_max_strategy(
        self,
        fn: t.Callable[[], Strategy[I]],
        **kwargs,
    ) -> Strategy[I]:
        if (min_value := self.min_value) is not None:
            kwargs.setdefault("min_value", min_value)
        elif (min_possible_value := self.MIN_POSSIBLE_VALUE) is not None:
            kwargs.setdefault("min_value", min_possible_value)
        if (max_value := self.max_value) is not None:
            kwargs.setdefault("max_value", max_value)
        res = fn(**kwargs)
        if not self.min_included:
            res = res.filter(lambda i: i != min_value)
        if not self.max_included:
            res = res.filter(lambda i: i != max_value)
        return res


@dataclass(unsafe_hash=True)
class BaseNumberType(Type, MinMax[TOrd], Selectable[T], abstract=True):
    "Commom implemetation of types that combine min/max and selections."

    min_value: t.Optional[TOrd] = None
    max_value: t.Optional[TOrd] = None
    min_included: bool = True
    max_included: bool = False
    selection: t.Optional[t.Sequence[SelectionData[T]]] = None

    def __post_init__(self):
        # Cast empty selections  to None
        if self.selection is not None and not self.selection:
            self.selection = None
        super().__post_init__()

    @property
    def simplified_repr(self) -> str:
        args = self.minmax_args + self.selection_args
        if args:
            return f"{self.constructor_name}[{', '.join(args)}]"
        else:
            return self.constructor_name

    def __repr__(self):
        res = MinMax.__repr__(self)[:-1]  # remove the closing ')'
        if self.selection:
            if res[-1] != "(":
                res += f", selection={self.selection!r})"
            else:
                res += f"selection={self.selection!r})"
        else:
            res += ")"
        return res


@dataclass(unsafe_hash=True, repr=False)  # repr is implemented in bases.
class IntegerType(BaseNumberType, MinMax[int], Selectable[int]):
    """A type object for values of type `int`:class.

    This type allows for both a `selection <Selection>`:class: and `min/max
    boundaries<MinMax>`:class:.  Usually you won't combine both kinds of
    restrictions and we don't check that every member of the selection lies
    between min/max boundaries (if provided).

    .. rubric:: Parsing and dumping

    This type uses `int`:class: for both the *internal form* and the
    *serialized form*.

    When `validate` is False, `dump <Type.dump>`:meth: skips checking the
    min/max values and selections.

    """

    min_value: t.Optional[int] = None
    max_value: t.Optional[int] = None
    min_included: bool = True
    max_included: bool = False
    selection: t.Optional[t.Sequence[SelectionData[int]]] = None

    @classproperty
    def constructor_name(cls) -> str:
        return "int"

    depth: t.ClassVar[int] = 1

    def parse(self, raw_value: t.Union[str, int]) -> int:
        if isinstance(raw_value, bool):
            raise TypeError("Booleans are not integers, not matter what Python thinks.")
        result = int(raw_value)
        self._ensure_value_in_range(result)
        self._ensure_value_in_selection(result)
        return result

    def dump(self, value: int, *, validate: bool = True) -> t.Union[str, int]:
        if isinstance(value, bool):
            raise TypeError("Booleans are not integers, not matter what Python thinks.")
        if not isinstance(value, int):
            raise TypeError(f"Invalid IntegerType value {short_repr(value)}")
        if validate:
            self._ensure_value_in_range(value)
            self._ensure_value_in_selection(value)
        return value

    def get_strategy(self) -> Strategy[int]:
        res = self._get_min_max_strategy(strategies.integers)
        return self._apply_selection_strategy(res)

    def __le__(self, other):
        if isinstance(other, IntegerType):
            return _and_cmp(self._le_minmax(other), self._le_selectable(other))
        elif isinstance(other, Type):
            return False
        return NotImplemented


@dataclass(unsafe_hash=True)
class StringType(Type[str, str], Selectable[str]):
    """A type object for values of type `str`:class:

    This type object allows `selection <Selectable>`:class:; or to set a
    `max_length`.  Setting both constraints at the same time, raises a
    TypeError.

    .. rubric:: Parsing and dumping

    This type uses `str`:class: for both the *internal form* and the
    *serialized form*.

    When `validate` is False, `dump <Type.dump>`:meth: skips checking the
    selections and `max_length`.

    """

    selection: t.Optional[t.Sequence[SelectionData[str]]] = None
    max_length: t.Optional[int] = None

    def __post_init__(self) -> None:
        if (max_length := self.max_length) is not None and max_length < 1:
            raise TypeError(
                f"StringType max_length must be positive and greater than 0, "
                f"got {max_length}"
            )
        if self.selection and max_length:
            warnings.warn(
                "Using max_length and selection at the same time makes little "
                "sense; max_length is ignored."
            )
        super().__post_init__()

    def __repr__(self):
        if not self.selection and not self.max_length:
            return "StringType()"
        elif self.selection:
            return f"StringType(selection={self.selection!r})"
        else:
            assert self.max_length
            return f"StringType(max_length={self.max_length})"

    @classproperty
    def constructor_name(cls) -> str:
        return "str"

    @property
    def simplified_repr(self) -> str:
        args = self.selection_args
        if args:
            return f"{self.constructor_name}[{', '.join(args)}]"
        else:
            return self.constructor_name

    depth: t.ClassVar[int] = 1

    def _parse_dump(self, value: str, *, validate: bool = True) -> str:
        if not isinstance(value, str):
            raise TypeError(f"Unexpected type of value {short_repr(value)}, expected a str")
        if validate:
            self._ensure_value_in_selection(value)
            if not self.selection and self.max_length:
                if len(value) > self.max_length:
                    raise TypeError(
                        f"Value {short_repr(value)} exceeds the maximum length allowed."
                    )
        return value

    def parse(self, raw_value: str) -> str:
        return self._parse_dump(raw_value)

    def dump(self, value: str, *, validate: bool = True) -> str:
        return self._parse_dump(value, validate=validate)

    def get_strategy(self) -> Strategy[str]:
        if self.selection:
            return self._apply_selection_strategy(strategies.text())
        elif self.max_length:
            return strategies.text(max_size=self.max_length)
        else:
            return strategies.text()

    def __le__(self, other):
        if isinstance(other, StringType):
            return self._le_selectable(other)
        elif isinstance(other, Type):
            return False
        return NotImplemented


@dataclass(unsafe_hash=True, repr=False)
class MinMaxType(Type[S, TOrd], MinMax[TOrd], abstract=True):
    """Common implementation of types objects that allow min/max boundaries.

    Types that support min/max boundaries can be initialized with arguments
    ``min``, ``min_included``, ``max``, and ``max_included``.  Both ``min`` and
    ``max`` can be None to indicate no boundary.  ``min_included`` and
    ``max_excluded`` are True and False by default; they indicate whether the
    corresponding boundary is a valid value or not.

    """

    min_value: t.Optional[TOrd] = None
    max_value: t.Optional[TOrd] = None
    min_included: bool = True
    max_included: bool = False

    depth: t.ClassVar[int] = 1

    def __post_init__(self):
        super().__post_init__()
        if self.min_value is not None and self.MIN_POSSIBLE_VALUE is not None:
            assert self.min_value >= self.MIN_POSSIBLE_VALUE
        if self.max_value is not None and self.MIN_POSSIBLE_VALUE is not None:
            assert self.max_value >= self.MIN_POSSIBLE_VALUE
        if self.min_value is not None and self.max_value is not None:
            assert self.min_value <= self.max_value

    @property
    def simplified_repr(self) -> str:
        args = self.minmax_args
        if args:
            return f"{self.constructor_name}[{', '.join(args)}]"
        else:
            return self.constructor_name

    def __le__(self, other):
        if isinstance(other, type(self)):
            return self._le_minmax(other)
        elif isinstance(other, Type):
            return False
        return NotImplemented


@dataclass(unsafe_hash=True, repr=False)
class FloatType(MinMaxType[t.Union[str, float], float]):
    """A type object for values of type `float`:class:

    .. rubric:: Parsing and dumping

    This type uses `float`:class: for the *internal form* and both `str`:class:
    and `float`:class: for the *serialized form*.

    When parsing from a string we simply call `float`:class: when the value
    provided.

    """

    min_value: t.Optional[float] = None
    max_value: t.Optional[float] = None
    min_included: bool = True
    max_included: bool = False

    @classproperty
    def constructor_name(cls) -> str:
        return "float"

    def parse(self, raw_value: t.Union[str, float]) -> float:
        result = float(raw_value)
        self._ensure_value_in_range(result)
        return result

    def dump(
        self,
        value: float,
        *,
        validate: bool = True,
    ) -> t.Union[str, float]:
        try:
            if isinstance(value, (str, bool)):
                raise TypeError
            else:
                float(value)  # ValueError for other types
        except (ValueError, TypeError, OverflowError):
            raise TypeError(f"Invalid FloatType value {short_repr(value)}")
        if validate:
            self._ensure_value_in_range(value)
        return value

    def get_strategy(self) -> Strategy[float]:
        return self._get_min_max_strategy(
            strategies.floats,
            allow_nan=False,
            allow_infinity=False,
        )


@dataclass(unsafe_hash=True)
class DateType(MinMaxType[str, date]):
    """A type object for values of `datetime`:class:.

    .. rubric:: Parsing and dumping

    This type uses `date`:class: for the *internal form* and `str`:class: for
    the *serialized form*.  The format for serialization if ``YYYY-MM-DD``.

    """

    min_value: t.Optional[date] = None
    max_value: t.Optional[date] = None
    min_included: bool = True
    max_included: bool = False

    MIN_POSSIBLE_VALUE = date(1978, 10, 21)

    @classproperty
    def constructor_name(cls) -> str:
        return "date"

    def parse(self, raw_value: str) -> date:
        result = datetime.strptime(raw_value, "%Y-%m-%d").date()
        self._ensure_value_in_range(result)
        return result

    def dump(self, value: date, *, validate: bool = True) -> str:
        if not isinstance(value, date):
            raise ValueError(f"Invalid DateType value {short_repr(value)}")
        if validate:
            self._ensure_value_in_range(value)
        return value.strftime("%Y-%m-%d")

    def get_strategy(self) -> Strategy[date]:
        return self._get_min_max_strategy(strategies.dates)


@dataclass(unsafe_hash=True)
class DateTimeType(MinMaxType[str, datetime]):
    """A type object for values of `datetime`:class:.

    `min_value` and `max_value` MUST NOT HAVE a tzinfo.  They will be regarded
    as UTC.  For validation purposes only values are normalized to UTC before
    checking the boundaries.

    .. rubric:: Parsing and dumping

    This type uses `datetime`:class: for the *internal form* and `str`:class:
    for the *serialized form*.

    The format for serialization changes when the value is naive and when it has
    attached a `zoneinfo.ZoneInfo`:class: object (or `backport.zoneinfo
    <https://pypi.org/project/backports.zoneinfo>`_ for Python 3.8).

    If the datetime is naive, the format is ``YYYY-MM-DDTHH:mm:ss.microZ``; when
    it has a zoneinfo ``YYYY-MM-DDTHH:mm:ss.micro <zone name>``::

       >>> try:
       ...     import zoneinfo
       ... except:
       ...     from backports import zoneinfo

       >>> DateTimeType().dump(datetime(2022, 3, 20, tzinfo=zoneinfo.ZoneInfo("America/Havana")))
       '2022-03-20T00:00:00.000000 America/Havana'

       >>> DateTimeType().dump(datetime(2022, 3, 20, tzinfo=None))
       '2022-03-20T00:00:00.000000Z'

    When parsing we test both the length of the string and whether it ends in
    'Z' to decide the format.

    .. rubric:: Using `pytz`

    By default we use `zoneinfo.ZoneInfo`:class: when trying to parse time zone
    names.  You can set `use_pytz` to True when creating the type::

       >>> import pytz
       >>> d = DateTimeType(use_pytz=True).parse('2022-03-20T00:00:00.000000 America/Havana')
       >>> d.tzinfo == pytz.timezone('America/Havana')
       True

    Notice `SchemaBase <xotl.plato.schema.SchemaBase>`:class: always uses the
    default, so you would have either override the default with
    `register_simple_type_map
    <xotl.plato.schema.register_simple_type_map>`:func: or use
    `typing.Annotated`.

    """

    min_value: t.Optional[datetime] = None
    max_value: t.Optional[datetime] = None
    min_included: bool = True
    max_included: bool = False

    use_pytz: bool = False

    MIN_POSSIBLE_VALUE = datetime(1978, 10, 21)

    def __post_init__(self):
        if self.min_value is not None:
            assert self.min_value.tzinfo is None
        if self.max_value is not None:
            assert self.max_value.tzinfo is None
        super().__post_init__()

    @classproperty
    def constructor_name(cls) -> str:
        return "datetime"

    def parse(self, raw_value: str) -> datetime:
        result = self._parse(raw_value, use_pytz=self.use_pytz)
        self._ensure_value_in_range(self._normalize_value(result))
        return result

    def dump(self, value: datetime, *, validate: bool = True) -> str:
        if not isinstance(value, datetime):
            raise TypeError(f"Invalid DateTimeType value {short_repr(value)}")
        normalized = self._normalize_value(value)
        if validate:
            self._ensure_value_in_range(normalized)
        tzinfo = value.tzinfo
        if tzinfo is not None:
            result = value.strftime("%Y-%m-%dT%H:%M:%S.%f")
            if isinstance(tzinfo, ZoneInfo):
                tzname = tzinfo.key
            else:
                # This works with pytz's tzname implementation
                tzname = tzinfo.tzname(None)  # type: ignore
            return f"{result} {tzname}"
        else:
            return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def _normalize_value(self, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value
        else:
            return value.astimezone(UTC).replace(tzinfo=None)

    @classmethod
    def _parse(cls, raw_value: str, use_pytz: bool = False) -> datetime:
        # We agreed to use different formats one for naive datetimes which are
        # deemed to be exchanged in UTC.  Another for time-zone aware
        # datetimes.  See issue
        # https://gitlab.merchise.org/mercurio-2018/xhg2/-/issues/1453
        #
        # In order to know which format is being used I'm going to simply test
        # if raw_value ends with Z it length to be 27 (the length of
        # 'YYYY-MM-MMT00:00:00.000000Z').
        if len(raw_value) == 27 and raw_value[-1] == "Z":
            # This is the case where the raw_value comes and goes *implicitly* in
            # UTC, we use naive datetimes
            result = datetime.strptime(raw_value, "%Y-%m-%dT%H:%M:%S.%fZ")
            assert result.tzinfo is None
        else:
            unparsed, zone = raw_value.split(" ", 1)
            if use_pytz and pytz is not None:
                tzinfo: t.Any = pytz.timezone(zone)
            else:
                tzinfo = ZoneInfo(zone)
            result = datetime.strptime(unparsed, "%Y-%m-%dT%H:%M:%S.%f")
            result = result.replace(tzinfo=tzinfo)
        return result

    def get_strategy(self) -> Strategy[datetime]:
        from datetime import tzinfo

        def _astimezone(args: t.Tuple[datetime, tzinfo]) -> datetime:
            dt, tz = args
            return dt.replace(tzinfo=UTC).astimezone(tz)

        values = self._get_min_max_strategy(strategies.datetimes)
        zones = strategies.sampled_from(_AVAILABLE_ZONE_INFOS)
        return values | strategies.tuples(values, zones).map(_astimezone)


@dataclass(unsafe_hash=True)
class DurationType(MinMaxType[t.Tuple[int, int, int], timedelta]):
    """A type object for values of type `timedelta`:class:.

    The minimum resolution possible is 1 microsecond.  The maximum possible
    value is not defined, it will depend on the application; for instance if you
    plan this type to be interoperable with Javascript, JS does have an upper
    limit for integers.

    .. rubric:: Parsing and dumping

    The serialized form is a tuple of three integers ``(days, seconds,
    microseconds)``::

       >>> DurationType().dump(timedelta(0))
       (0, 0, 0)

    """

    min_value: t.Optional[timedelta] = None
    max_value: t.Optional[timedelta] = None
    min_included: bool = True
    max_included: bool = False

    MIN_POSSIBLE_VALUE = timedelta(microseconds=0)

    @classproperty
    def constructor_name(cls) -> str:
        return "timedelta"

    def parse(self, raw_value: t.Tuple[int, int, int]) -> timedelta:
        days, secs, ms = raw_value
        result = timedelta(days=days, seconds=secs, microseconds=ms)
        self._ensure_value_in_range(result)
        return result

    def dump(
        self,
        value: timedelta,
        *,
        validate: bool = True,
    ) -> t.Tuple[int, int, int]:
        if not isinstance(value, timedelta):
            raise TypeError(f"Invalid DurationType value {short_repr(value)}")
        if validate:
            self._ensure_value_in_range(value)
        return value.days, value.seconds, value.microseconds

    def get_strategy(self) -> Strategy[timedelta]:
        return self._get_min_max_strategy(strategies.timedeltas)


@dataclass(unsafe_hash=True)
class TupleType(Type[t.Tuple[t.Any, ...], t.Tuple[t.Any, ...]]):
    """The type of fixed-sized tuples of many other types.

    .. rubric:: Parsing and dumping

    The serialization form is a tuple that will have as many items as there are
    `bases`, each one using the serialized form of the corresponding base.

    The internal form is a tuple with as many items as there are `bases`, each
    one using the internal form of the corresponde base.

    """

    bases: t.Sequence[Type]

    def __init__(self, bases: t.Sequence[Type]) -> None:
        self.bases = tuple(bases)

    def __repr__(self):
        return f"TupleType({self.bases!r})"

    @classproperty
    def constructor_name(cls) -> str:
        return "tuple"

    @property
    def simplified_repr(self) -> str:
        bases = ", ".join(base.simplified_repr for base in self.bases)
        return f"{self.constructor_name}[{bases}]"

    @memoized_property
    def depth(self):
        return max((base.depth for base in self.bases), default=-1) + 1

    def parse(self, raw_value: t.Tuple[t.Any, ...]) -> t.Tuple[t.Any, ...]:
        if not self.bases and raw_value != ():
            raise TypeError(f"Invalid value {short_repr(raw_value)}")
        if (many := len(self.bases)) != (this_many := len(raw_value)):
            raise ValueError(f"Expected {many} values, got {this_many}")
        return tuple(base.parse(value) for base, value in zip(self.bases, raw_value))

    def dump(
        self,
        value: t.Tuple[t.Any, ...],
        *,
        validate: bool = True,
    ) -> t.Tuple[t.Any, ...]:
        if not self.bases and value != ():
            raise TypeError(f"Invalid value {short_repr(value)}")
        if (many := len(self.bases)) != (this_many := len(value)):
            raise ValueError(f"Expected {many} values, got {this_many}")
        return tuple(base.dump(v, validate=validate) for base, v in zip(self.bases, value))

    def get_strategy(self) -> Strategy[t.Tuple[t.Any, ...]]:
        return strategies.tuples(*(base.get_strategy() for base in self.bases))

    def __le__(self, other):
        if isinstance(other, TupleType):
            if len(self.bases) == len(other.bases):
                return all(
                    self_base <= other_base
                    for self_base, other_base in zip(self.bases, other.bases)
                )
            else:
                return False
        elif isinstance(other, Type):
            return False
        return NotImplemented

    def gettypeattr(self, typeattr: PathItem) -> Type:
        if isinstance(typeattr, int):
            return self.bases[typeattr]
        else:
            raise TypeError

    def iter_typeattrs(self) -> t.Iterator[t.Tuple[PathItem, Type]]:
        yield from enumerate(self.bases)


@dataclass(unsafe_hash=True)
class ObjectType(Type):
    """A type for values that are records.

    .. rubric:: Parsing and dumping

    The serialization form is a mapping from strings to the serialized
    form of the corresponding attribute in the `shape`.

    The internal form is a mapping strings to the internal form of the
    corresponding attribute in the `shape`.

    """

    shape: Shape[Type]

    # We expect the given mapping preserves the order of the keys, it's not a
    # strong requirement, but it's nice to run doctests.
    def __init__(self, shape: t.Mapping[str, Type]) -> None:
        self.shape = immutables.Map(shape)
        self._keys = tuple(shape)

    def __repr__(self):
        shape = {key: self.shape[key] for key in self._keys}
        return f"ObjectType({shape!r})"

    @classproperty
    def constructor_name(cls) -> str:
        return "object"

    @property
    def simplified_repr(self) -> str:
        shape_args = ", ".join(
            f"{name}: {type_.simplified_repr}" for name, type_ in self.shape.items()
        )
        return f"{self.constructor_name}[{{{shape_args}}}]"

    @memoized_property
    def depth(self) -> int:
        return max(t.depth for t in self.shape.values()) + 1

    def parse(self, raw_value: t.Mapping[str, S]) -> t.Mapping[str, I]:
        try:
            return {
                attr: base_type.parse(raw_value[attr])
                for attr, base_type in self.shape.items()
            }
        except KeyError as cause:
            raise ValueError(
                f"Cannot parse {short_repr(raw_value)} for type {self.simplified_repr!r}"
            ) from cause

    def dump(
        self,
        value: t.Mapping[str, I],
        *,
        validate: bool = True,
    ) -> t.Mapping[str, S]:
        try:
            return {
                attr: base_type.dump(value[attr], validate=validate)
                for attr, base_type in self.shape.items()
            }
        except KeyError as cause:
            raise ValueError(
                f"Cannot dump {short_repr(value)} for type {self.simplified_repr!r}"
            ) from cause

    def get_strategy(self) -> Strategy[t.Mapping[str, I]]:
        return strategies.fixed_dictionaries(
            {attr: base.get_strategy() for attr, base in self.shape.items()}
        )

    def __le__(self, other):
        if isinstance(other, ObjectType):
            self_keys = set(self.shape)
            other_keys = set(other.shape)
            if self_keys == other_keys:
                return all(
                    key_type <= other.shape[key] for key, key_type in self.shape.items()
                )
            else:
                return False
        elif isinstance(other, Type):
            return False
        return NotImplemented

    def gettypeattr(self, typeattr: PathItem) -> Type:
        if isinstance(typeattr, str):
            return self.shape[typeattr]
        else:
            raise TypeError

    def iter_typeattrs(self) -> t.Iterator[t.Tuple[PathItem, Type]]:
        # Use _keys to preseve the order of the original dict if possible.
        yield from ((key, self.shape[key]) for key in self._keys)


@dataclass(unsafe_hash=True)
class ListType(Type[t.List[S], t.Sequence[I]]):
    """A list of items of the same type.

    .. rubric:: Parsing and dumping

    The serialization form is a list of the serialized form of each item.

    The internal form is a sequence of items in the internal form of the base
    type.

    """

    of: Type[S, I]

    @classproperty
    def constructor_name(cls) -> str:
        return "list"

    @property
    def simplified_repr(self) -> str:
        return f"{self.constructor_name}[{self.of.simplified_repr}]"

    @memoized_property
    def depth(self) -> int:
        return self.of.depth + 1

    def parse(self, raw_value: t.Sequence[S]) -> t.Sequence[I]:
        return [self.of.parse(value) for value in raw_value]

    def dump(
        self,
        value: t.Sequence[I],
        *,
        validate: bool = True,
    ) -> t.List[S]:
        return [self.of.dump(val, validate=validate) for val in value]

    def get_strategy(self) -> Strategy[t.List[I]]:
        return strategies.lists(self.of.get_strategy())

    def __le__(self, other):
        if isinstance(other, ListType):
            return self.of <= other.of
        elif isinstance(other, Type):
            return False
        return NotImplemented

    def gettypeattr(self, typeattr: PathItem) -> Type:
        if typeattr is None:
            return self.of
        else:
            raise AttributeError(
                f"Type object {self.simplified_repr!s} doesnt "
                f"have type-attribute '{typeattr}'"
            )

    def iter_typeattrs(self) -> t.Iterator[t.Tuple[PathItem, Type]]:
        yield (None, self.of)

    def __repr__(self):
        return f"ListType({self.of!r})"


@dataclass(unsafe_hash=True)
class OptionalType(Type[t.Optional[S], t.Optional[I]]):
    """The optional type that allows a None value.

    .. rubric:: Parsing and dumping

    The serialization form is simply the base type's serialized form extended with
    the value None.

    The internal form the base type's internal form extended with the value
    None.

    .. rubric:: Sub-typing

    .. warning:: Optional types are only sub-types of other optional types.

       It's tempting to allow ``t1 <= OptionalType(t2)`` for all ``t1`` and
       ``t2`` where ``t1 <= t2`` , since any value of type ``t1`` will also be a
       valid value for ``OptionalType(t2)``.

       But that's not the behavior of the current sub-typing relation.

    """

    type: Type[S, I]

    def __post_init__(self):
        # Flatten OptionalType(OptionalType(x)) to OptionalType(x)
        if isinstance(t := self.type, OptionalType):
            self.type = t.type
        super().__post_init__()

    @classproperty
    def constructor_name(cls) -> str:
        return "optional"

    @property
    def simplified_repr(self) -> str:
        return f"{self.constructor_name}[{self.type.simplified_repr}]"

    # Notice the OptionalType does not increase the depth measure of complexity
    # of a type.  This is because, while it does introduce a little bit of
    # complexity it's not of the same kind other nested type can introduce.  The
    # value of `depth` is mostly useful to limit the complexity of the types
    # used in applications, (for instance, to avoid list of objects which
    # contain lists of other objects.)
    @memoized_property
    def depth(self) -> int:
        return self.type.depth

    def parse(self, raw_value: t.Optional[S]) -> t.Optional[I]:
        if raw_value is not None:
            return self.type.parse(raw_value)
        else:
            return None

    def dump(
        self,
        value: t.Optional[I],
        *,
        validate: bool = True,
    ) -> t.Optional[S]:
        if value is not None:
            return self.type.dump(value, validate=validate)
        else:
            return None

    def get_strategy(self) -> Strategy[t.Optional[I]]:
        return strategies.just(None) | self.type.get_strategy()

    def __le__(self, other):
        if isinstance(other, OptionalType):
            return self.type <= other.type
        elif isinstance(other, Type):
            return False

        # I'm tempted to allow ``t1 <= OptionalType(t2)`` for all ``t1`` and
        # ``t2`` where ``t1 <= t2`` , since any value of type ``t1`` will also
        # be a valid value for ``OptionalType(t2)``.

        # elif isinstance(other, type(self.type)):
        #     return other <= self.type
        return NotImplemented

    def gettypeattr(self, typeattr: PathItem) -> Type:
        if typeattr is None:
            return self.type
        else:
            raise AttributeError(
                f"Type object {self.simplified_repr!s} doesnt "
                f"have type-attribute '{typeattr}'"
            )

    def iter_typeattrs(self) -> t.Iterator[t.Tuple[PathItem, Type]]:
        yield (None, self.type)

    def __repr__(self):
        return f"OptionalType({self.type!r})"


# Mapping's serial/internal types: a type for the serialized key (KS),
# serialized value (VS), internal key (KI), and internal value (VI).
KS = t.TypeVar("KS")
KI = t.TypeVar("KI")
VS = t.TypeVar("VS")
VI = t.TypeVar("VI")


@dataclass(unsafe_hash=True)
class MappingType(Type[t.Mapping[KS, VS], t.Mapping[KI, VI]]):
    """A type of mappings from keys of given type to values of another type.

    .. rubric:: Parsing and dumping

    The serialization form is mapping from the key type's serialized form to the
    value type's serialized form.

    The internal form is mapping from the key type's internal form to the
    value type's internal form.

    """

    key_type: Type[KS, KI]
    value_type: Type[VS, VI]

    @classproperty
    def constructor_name(cls) -> str:
        return "map"

    @property
    def simplified_repr(self) -> str:
        return f"{self.constructor_name}[{self.key_type.simplified_repr}, {self.value_type.simplified_repr}]"

    @memoized_property
    def depth(self) -> int:
        return max(self.key_type.depth, self.value_type.depth) + 1

    def parse(self, raw_value: t.Mapping[KS, VS]) -> t.Mapping[KI, VI]:
        try:
            items = raw_value.items()
        except AttributeError as cause:
            raise TypeError(f"Invalid raw_value for {self}") from cause
        return {self.key_type.parse(key): self.value_type.parse(val) for key, val in items}

    def dump(
        self,
        value: t.Mapping[KI, VI],
        *,
        validate: bool = True,
    ) -> t.Mapping[KS, VS]:
        try:
            items = value.items()
        except AttributeError as cause:
            raise TypeError(f"Invalid value for {self}") from cause
        return {
            self.key_type.dump(key, validate=validate): self.value_type.dump(
                val, validate=validate
            )
            for key, val in items
        }

    def get_strategy(self) -> Strategy[t.Dict[KI, VI]]:
        return strategies.dictionaries(
            self.key_type.get_strategy(),
            self.value_type.get_strategy(),
        )

    def __le__(self, other):
        if isinstance(other, MappingType):
            return self.key_type <= other.key_type and self.value_type <= other.value_type
        elif isinstance(other, Type):
            return False
        return NotImplemented

    def gettypeattr(self, typeattr: PathItem) -> Type:
        if typeattr == "keys":
            return self.key_type
        elif typeattr == "values":
            return self.value_type
        elif typeattr == "items":
            return TupleType((self.key_type, self.value_type))
        else:
            raise AttributeError(
                f"Type object {self.simplified_repr!s} doesnt "
                f"have type-attribute '{typeattr}'"
            )

    def iter_typeattrs(self) -> t.Iterator[t.Tuple[PathItem, Type]]:
        yield ("keys", self.key_type)
        yield ("values", self.value_type)


def _and_cmp(first: bool, second: bool) -> bool:
    """AND taking into account NotImplemented"""
    if first is NotImplemented or second is NotImplemented:
        return NotImplemented
    return first and second


UTC = ZoneInfo("UTC")

try:
    import zoneinfo

    _AVAILABLE_ZONE_INFOS = [
        ZoneInfo(key) for key in zoneinfo.available_timezones() if "/" in key
    ]
except ImportError:
    _AVAILABLE_ZONE_INFOS = [UTC]


def short_repr(v):
    res = repr(v)
    if len(res) > 25:
        return f"{res[:20]}...{res[-5:]}"
    return res
