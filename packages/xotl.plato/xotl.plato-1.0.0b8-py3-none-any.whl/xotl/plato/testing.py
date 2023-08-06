from __future__ import annotations

import contextlib
import difflib
import doctest
import pickle
import pprint
import string
import sys
import typing as t
import unittest
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from functools import partial
from types import ModuleType

from hypothesis import strategies as st
from hypothesis.strategies import DataObject
from hypothesis.strategies import SearchStrategy as Strategy
from xotl.plato.types import (
    BaseNumberType,
    BooleanType,
    DateTimeType,
    DateType,
    DurationType,
    FloatType,
    IntegerType,
    ListType,
    MappingType,
    MinMax,
    ObjectType,
    OptionalType,
    Path,
    PathItem,
    Selection,
    StringType,
    TupleType,
    Type,
)
from xotl.tools.fp.tools import fst
from xotl.tools.names import nameof
from xotl.tools.objects import import_object


def with_min_or_max(t: MinMax):
    "A predicate to filter types with some non-none min/max boundary."
    return t.min_value is not None or t.max_value is not None


#: A search strategy of valid type objects.
types: Strategy[Type] = st.deferred(lambda: hashable_types | nonhashable_types)
nonhashable_types: Strategy[Type] = st.deferred(
    lambda: object_types() | mapping_types() | tuple_types() | optional_types()
)

hashable_types: Strategy[Type] = st.deferred(
    lambda: integer_types
    | float_types
    | string_types
    | boolean_types
    | duration_types
    | date_types
    | datetime_types
    | optional_types(hashable_types)
)


_MIN_INT_DELTA = 1
_MAX_INT_DELTA = 10**6
_MIN_FLOAT = -1e9
_MAX_FLOAT = 1e9
_MIN_FLOAT_DELTA = 1.0
_MAX_FLOAT_DELTA = 1e6
_MIN_DURATION_DELTA = timedelta(hours=1)
_MAX_DURATION_DELTA = timedelta(hours=10**5)
_MIN_DATE_DELTA = timedelta(days=1)
_MAX_DATE_DELTA = timedelta(days=1000 * 365)
_MAX_DATETIME_VALUE = datetime(4000, 12, 31)
_MAX_DATE_VALUE = date(4000, 12, 31)


#: A search strategy of valid `IntegerType`:class: instances.
integer_types_with_selections: Strategy[IntegerType] = st.deferred(
    lambda: (
        st.sets(st.integers(), min_size=3, max_size=10).map(_integers_in_selection)
        | st.tuples(
            st.integers(),
            st.integers(
                min_value=_MIN_INT_DELTA,
                max_value=_MAX_INT_DELTA,
            ),
        )
        .flatmap(partial(_selections_with_bounds, st.integers))
        .map(_integers_in_range_and_selection)
    )
)

integer_types: Strategy[IntegerType] = st.deferred(
    lambda: (
        st.just(IntegerType())
        | st.integers().map(lambda m: IntegerType(min_value=m))
        | st.integers().map(lambda m: IntegerType(max_value=m))
        | st.tuples(
            st.integers(),
            st.integers(
                min_value=_MIN_INT_DELTA,
                max_value=_MAX_INT_DELTA,
            ),
        ).map(_integers_in_range)
        | integer_types_with_selections
    )
)


def floats(min_value=None, max_value=None, **extra):
    if min_value is not None:
        min_value = max(min_value, _MIN_FLOAT)
    else:
        min_value = _MIN_FLOAT
    if max_value is not None:
        max_value = min(max_value, _MAX_FLOAT)
    else:
        max_value = _MAX_FLOAT
    return st.floats(
        # These min/max are here to avoid generating values that won't serialize
        # well in JSONField.
        min_value=min_value,
        max_value=max_value,
        allow_nan=False,
        allow_infinity=False,
        **extra,
    )


#: A search strategy of valid `FloatType`:class: instances.
float_types: Strategy[FloatType] = st.deferred(
    lambda: (
        st.just(FloatType())
        | st.builds(FloatType, min_value=floats())
        | st.builds(FloatType, max_value=floats())
        | st.tuples(
            floats(),
            floats(
                min_value=_MIN_FLOAT_DELTA,
                max_value=_MAX_FLOAT_DELTA,
            ),
        ).map(_floats_in_range)
    )
)

ascii_strings = partial(
    st.text,
    alphabet=st.sampled_from(string.ascii_letters + " " + string.digits),
    min_size=5,
    max_size=10,
)

strings = partial(
    st.text,
    alphabet=st.characters(
        whitelist_categories=(
            # Chars in other categories might cause issues with JSONField trying
            # to store those chars.
            #
            # See
            # https://en.wikipedia.org/wiki/Unicode_character_property#General_Category
            NUMBERS := "N",
            LETTERS := "L",
            PUNTUACTION := "P",
            SEPARATORS := "Z",
            SYMBOLS := "S",
            MARKS := "M",
        )
    ),
    min_size=1,
    max_size=10,
)


@st.composite
def selections(
    draw,
    base: Strategy[T],
    names_base: Strategy[t.Optional[str]] = strings(),
    min_size=1,
    max_size=10,
) -> Selection[T]:
    values = draw(st.lists(base, min_size=min_size, max_size=max_size))
    names = [draw(names_base) for _ in range(len(values))]
    return Selection.from_pairs(zip(values, names))


#: A search strategy of valid `StringType`:class: instances.
string_types_with_selections: Strategy[StringType] = st.builds(
    StringType,
    selection=selections(ascii_strings()),
)
string_types: Strategy[StringType] = st.deferred(
    lambda: (
        st.builds(
            StringType,
            selection=st.none(),
            max_length=st.just(None) | st.integers(min_value=1, max_value=1024),
        )
        | string_types_with_selections
    )
)


#: A search strategy of the only possible `BooleanType`:class: intance.
boolean_types: Strategy[BooleanType] = st.just(BooleanType())

#: A search strategy of valid `DurationType`:class: instances.
duration_types: Strategy[DurationType] = st.deferred(
    lambda: st.just(DurationType())
    | st.builds(
        DurationType,
        min_value=st.timedeltas(min_value=DurationType.MIN_POSSIBLE_VALUE),
        max_value=st.none(),
    )
    | st.builds(
        DurationType,
        min_value=st.none(),
        max_value=st.timedeltas(min_value=DurationType.MIN_POSSIBLE_VALUE),
    )
    | st.tuples(
        st.timedeltas(min_value=DurationType.MIN_POSSIBLE_VALUE),
        st.timedeltas(
            min_value=_MIN_DURATION_DELTA,
            max_value=_MAX_DURATION_DELTA,
        ),
    ).map(partial(_type_in_range, DurationType))
)

#: A search strategy of valid `DateType`:class: instances.
date_types: Strategy[DateType] = st.deferred(
    lambda: st.just(DateType())
    | st.builds(
        DateType,
        min_value=st.dates(min_value=DateType.MIN_POSSIBLE_VALUE),
        max_value=st.none(),
    )
    | st.builds(
        DateType,
        min_value=st.none(),
        max_value=st.dates(min_value=DateType.MIN_POSSIBLE_VALUE),
    )
    | st.tuples(
        st.dates(
            min_value=DateType.MIN_POSSIBLE_VALUE,
            max_value=_MAX_DATE_VALUE,
        ),
        st.timedeltas(min_value=_MIN_DATE_DELTA, max_value=_MAX_DATE_DELTA),
    ).map(partial(_type_in_range, DateType))
)


#: A search strategy of valid `DateTimeType`:class: instances.
datetime_types: Strategy[DateTimeType] = st.deferred(
    lambda: st.just(DateTimeType())
    | st.builds(
        DateTimeType,
        min_value=st.datetimes(min_value=DateTimeType.MIN_POSSIBLE_VALUE),
        max_value=st.none(),
    )
    | st.builds(
        DateTimeType,
        min_value=st.none(),
        max_value=st.datetimes(min_value=DateTimeType.MIN_POSSIBLE_VALUE),
    )
    | st.tuples(
        st.datetimes(
            min_value=DateTimeType.MIN_POSSIBLE_VALUE,
            max_value=_MAX_DATETIME_VALUE,
        ),
        st.timedeltas(
            min_value=_MIN_DURATION_DELTA,
            max_value=_MAX_DURATION_DELTA,
        ),
    ).map(partial(_type_in_range, DateTimeType))
)


def optional_types(base: Strategy[Type] = types) -> Strategy[OptionalType]:
    "A search strategy of valid `OptionalType`:class: instances."
    return st.builds(OptionalType, type=base)


attrs = st.sampled_from([f"attr{i}" for i in range(10)])


def shapes(base: Strategy[Type] = types):
    return st.dictionaries(attrs, base, min_size=1, max_size=5)


def object_types(base: Strategy[Type] = types) -> Strategy[ObjectType]:
    "A search strategy of valid `ObjectType`:class: instances."
    return st.builds(ObjectType, shape=shapes(base))


def list_types(base: Strategy[Type] = types) -> Strategy[ListType]:
    "A search strategy of valid `ListType`:class: instances."
    return st.builds(ListType, of=base)


def mapping_types(
    key_base: Strategy[Type] = hashable_types,
    value_base: Strategy[Type] = types,
) -> Strategy[MappingType]:
    "A search strategy of valid `MappingType`:class: instances."
    return st.builds(MappingType, key_type=key_base, value_type=value_base)


def tuple_types(
    base: Strategy[Type] = types,
    min_size: int = 0,
    max_size: int = 10,
) -> Strategy[TupleType]:
    "A search strategy of valid `TupleType`:class: instances."
    return st.builds(TupleType, bases=st.lists(base, min_size=min_size, max_size=max_size))


@dataclass
class TypedValue:
    """A pair of a `value` and its type `t`.

    We allow the construction of invalid pairs so that you can test invalid
    samples.

    Instances can be unpacked to ``(type, value)``.

    Examples::

       >>> t, value = TypedValue.strategy(integer_types).example()
       >>> isinstance(t, IntegerType)
       True

       >>> isinstance(value, int)
       True

    """

    value: t.Any
    t: Type

    @classmethod
    def from_args(cls, args: t.Tuple[Type, t.Any]) -> TypedValue:
        "Create a instance of TypedValue from a tuple of ``(type, value)``."
        t, value = args
        return cls(value=value, t=t)

    @classmethod
    def strategy(
        cls,
        base_types: Strategy[Type] = types,
    ) -> Strategy[TypedValue]:
        """Return a hypothesis strategy that generates valid TypeValue instances.

        `base_types` is must be a strategy generating types, the instances
        generated will only be of those types.  By default we use a strategy
        that generates valid samples

        """
        return base_types.flatmap(lambda t: st.tuples(st.just(t), t.get_strategy())).map(
            cls.from_args
        )

    def __iter__(self):
        # This allows unpacking like ``t, val = typed_value``
        yield self.t
        yield self.value


@st.composite
def supertypes(draw, t: Type) -> Type:
    """Given a type ``t``, find a new type ``st`` such that ``t <= st``.

    This function only works for types defined in `xotl.plato.types`:mod:.  If
    you create new types, you should implement the supertype strategy for it.
    For unknown types, return the same type `t` (which should be a supertype of
    itself).

    """
    if isinstance(t, IntegerType):
        return draw(integer_supertypes(t))
    elif isinstance(t, FloatType):
        return draw(float_supertypes(t))
    elif isinstance(t, StringType):
        return draw(string_supertypes(t))
    elif isinstance(t, DateType):
        return draw(date_supertypes(t))
    elif isinstance(t, DateTimeType):
        return draw(datetime_supertypes(t))
    elif isinstance(t, DurationType):
        return draw(duration_supertypes(t))
    elif isinstance(t, ObjectType):
        return draw(object_supertypes(t))
    elif isinstance(t, OptionalType):
        return draw(optional_supertypes(t))
    elif isinstance(t, TupleType):
        return draw(tuple_supertypes(t))
    elif isinstance(t, ListType):
        return draw(list_supertypes(t))
    elif isinstance(t, MappingType):
        return draw(mapping_supertypes(t))
    else:
        return t


@st.composite
def integer_supertypes(draw, t: IntegerType) -> IntegerType:
    def _theres_room_for_more(low, up):
        if low is None:
            return True
        if up is None:
            return True
        return up - low > 100

    min_value, min_included = t.min_value, t.min_included
    max_value, max_included = t.max_value, t.max_included
    if min_value is not None:
        min_value = draw(
            st.just(None) | st.integers(min_value=min_value - 100, max_value=min_value)
        )
    if max_value is not None:
        max_value = draw(
            st.just(None) | st.integers(min_value=max_value, max_value=max_value + 100)
        )
    # Change the names of the selections and expand the selection to cover more
    # items.  We only introduce a selection if `t` had a selection, we only
    # expand it if there's enough room to pick up examples between min and max.
    if sel := t.selection:
        selection = [(v, draw(strings())) for v, _ in sel]
    else:
        selection = []
    if selection and _theres_room_for_more(min_value, max_value):
        present = {v for v, _ in selection}
        if min_value is not None and max_value is not None:
            strategy = st.integers(min_value=min_value, max_value=max_value)
        elif min_value is not None:
            strategy = st.integers(min_value=min_value)
        elif max_value is not None:
            strategy = st.integers(max_value=max_value)
        else:
            strategy = st.integers()
        if min_value is not None and not min_included:
            strategy = strategy.filter(lambda i: i != min_value)
        if max_value is not None and not max_included:
            strategy = strategy.filter(lambda i: i != max_value)
        strategy = strategy.filter(lambda i: i not in present)
        extra = draw(st.sets(strategy))
        selection.extend((v, draw(strings())) for v in extra)
    return IntegerType(
        min_value=min_value,
        min_included=min_included,
        max_value=max_value,
        max_included=max_included,
        selection=Selection.from_pairs(selection),
    )


@st.composite
def float_supertypes(draw, t: FloatType) -> FloatType:
    min_value, min_included = t.min_value, t.min_included
    max_value, max_included = t.max_value, t.max_included
    if min_value is not None:
        min_value = draw(
            st.just(None) | floats(min_value=min_value - 100, max_value=min_value)
        )
    if max_value is not None:
        max_value = draw(
            st.just(None) | floats(min_value=max_value, max_value=max_value + 100)
        )
    return FloatType(
        min_value=min_value,
        min_included=min_included,
        max_value=max_value,
        max_included=max_included,
    )


@st.composite
def string_supertypes(draw, t: StringType) -> StringType:
    if sel := t.selection:
        selection = [(v, draw(strings() | st.just(None))) for v, _ in sel]
    else:
        selection = []
    if selection:
        present = {v for v, _ in selection}
        extra = draw(selections(ascii_strings().filter(lambda s: s not in present)))
        selection.extend((v, draw(strings())) for v in extra)
        return StringType(selection=Selection.from_pairs(selection))
    else:
        return StringType()


@st.composite
def date_supertypes(draw, t: DateType) -> DateType:
    min_value, min_included = t.min_value, t.min_included
    max_value, max_included = t.max_value, t.max_included
    if min_value is not None:
        if min_value > DateType.MIN_POSSIBLE_VALUE:
            min_value = draw(
                st.just(None)
                | st.dates(
                    min_value=DateType.MIN_POSSIBLE_VALUE,
                    max_value=min_value,
                )
            )
        else:
            min_value = DateType.MIN_POSSIBLE_VALUE
    if max_value is not None:
        try:
            max_value += draw(
                st.timedeltas(
                    min_value=timedelta(0),
                    max_value=_MAX_DATE_DELTA,
                )
            )
        except OverflowError:
            # I don't want to fix an upper value for dates which might change
            # with the underlying Python impl; so OverflowError is the way to go
            # here.
            max_value = None
    return DateType(
        min_value=min_value,
        min_included=min_included,
        max_value=max_value,
        max_included=max_included,
    )


@st.composite
def datetime_supertypes(draw, t: DateTimeType) -> DateTimeType:
    min_value, min_included = t.min_value, t.min_included
    max_value, max_included = t.max_value, t.max_included
    if min_value is not None:
        if min_value > DateTimeType.MIN_POSSIBLE_VALUE:
            min_value = draw(
                st.just(None)
                | st.datetimes(
                    min_value=DateTimeType.MIN_POSSIBLE_VALUE,
                    max_value=min_value,
                )
            )
        else:
            min_value = DateTimeType.MIN_POSSIBLE_VALUE
    if max_value is not None:
        try:
            max_value += draw(
                st.timedeltas(
                    min_value=timedelta(0),
                    max_value=_MAX_DATE_DELTA,
                )
            )
        except OverflowError:
            # I don't want to fix an upper value for datetimes which might
            # change with the underlying Python impl; so OverflowError is the
            # way to go here.
            max_value = None
    return DateTimeType(
        min_value=min_value,
        min_included=min_included,
        max_value=max_value,
        max_included=max_included,
    )


@st.composite
def duration_supertypes(draw, t: DurationType) -> DurationType:
    min_value, min_included = t.min_value, t.min_included
    max_value, max_included = t.max_value, t.max_included
    if min_value is not None:
        if min_value > DurationType.MIN_POSSIBLE_VALUE:
            min_value = draw(
                st.just(None)
                | st.timedeltas(
                    min_value=DurationType.MIN_POSSIBLE_VALUE,
                    max_value=min_value,
                )
            )
        else:
            min_value = DurationType.MIN_POSSIBLE_VALUE
    if max_value is not None:
        try:
            max_value += draw(
                st.timedeltas(
                    min_value=timedelta(0),
                    max_value=_MAX_DURATION_DELTA,
                )
            )
        except OverflowError:
            max_value = None
    return DurationType(
        min_value=min_value,
        min_included=min_included,
        max_value=max_value,
        max_included=max_included,
    )


@st.composite
def object_supertypes(draw, t: ObjectType) -> ObjectType:
    return ObjectType({key: draw(supertypes(t)) for key, t in t.shape.items()})


@st.composite
def tuple_supertypes(draw, t: TupleType) -> TupleType:
    return TupleType([draw(supertypes(base)) for base in t.bases])


@st.composite
def list_supertypes(draw, t: ListType) -> ListType:
    return ListType(draw(supertypes(t.of)))


@st.composite
def optional_supertypes(draw, t: OptionalType) -> OptionalType:
    return OptionalType(draw(supertypes(t.type)))


@st.composite
def mapping_supertypes(draw, t: MappingType) -> MappingType:
    return MappingType(
        draw(supertypes(t.key_type)),
        draw(supertypes(t.value_type)),
    )


def _type_in_selection(Type: t.Type[BaseNumberType], vals):
    return Type(
        selection=Selection.from_pairs((val, None) for val in vals),
    )


def _type_in_range(Type: t.Type[BaseNumberType], args):
    min_value, delta = args
    return Type(
        min_value=min_value,
        min_included=True,
        max_value=min_value + delta,
        max_included=True,
    )


def _type_in_range_and_selection(Type: t.Type[BaseNumberType], args):
    min_value, delta, vals = args
    assert delta > 0
    max_value = min_value + delta
    assert all(min_value <= val <= max_value for val in vals), "\n".join(
        f"{min_value} <= {val} <= {max_value}" for val in vals
    )
    return Type(
        min_value=min_value,
        max_value=max_value,
        max_included=True,
        selection=Selection.from_pairs((val, None) for val in vals),
    )


_integers_in_range: t.Callable[[t.Tuple[int, int]], IntegerType] = partial(
    _type_in_range, IntegerType
)
_integers_in_selection: t.Callable[[t.Collection[int]], IntegerType] = partial(
    _type_in_selection, IntegerType
)
_integers_in_range_and_selection: t.Callable[
    [t.Tuple[int, int, t.Sequence[int]]],
    IntegerType,
] = partial(
    _type_in_range_and_selection,
    IntegerType,
)

_floats_in_range: t.Callable[[t.Tuple[float, float]], FloatType] = partial(
    _type_in_range, FloatType
)


def _selections_with_bounds(strategy, bounds):
    """Return a strategy to generate triplets of ``(min, max, values)``.

    The argument `bounds` MUST be a pair of ``(min, delta)``, and ``max`` is
    just ``min + delta``.  ``values`` is a list with values which hold ``min <=
    value < max``.

    This means that the provided ``delta`` MUST allow for some value to exists
    in that range.

    """
    min_value, delta = bounds
    assert delta > 0
    max_value = min_value + delta
    return st.tuples(
        st.just(min_value),
        st.just(delta),
        st.sets(
            strategy(min_value=min_value, max_value=max_value).filter(lambda v: v < max_value),
            min_size=3,
            max_size=10,
        ),
    )


T = t.TypeVar("T")


high_level_types = (
    optional_types() | object_types() | list_types() | tuple_types() | mapping_types()
)


class ExtendedBaseTestCase(unittest.TestCase):
    def runModuleDoctest(
        self,
        mod_or_name,
        *,
        additional_globals: t.Dict[str, t.Any] = None,
    ) -> None:
        """Run the doctests of the given module.

        All the symbols imported and/or defined in such module will be available
        to the doctests, additional symbols can be provided with
        `additional_globals`.

        All tests are run with NORMALIZE_WHITESPACE and ELLIPSIS.

        """
        runModuleDoctest(mod_or_name, additional_globals=additional_globals)

    def assertDictKVMembers(self, mapping: t.Mapping, **expected):
        "Assert `mapping` has the expected key-value pairs (and possibly more)."

        class _missing:
            def __repr__(self):
                return "<missing>"

        missing = _missing()

        actual_sequence = ()  # type: t.Tuple[t.Tuple[str, t.Any], ...]
        expected_sequence = ()  # type: t.Tuple[t.Tuple[str, t.Any], ...]
        for key, expected_value in expected.items():
            expected_sequence += ((key, expected_value),)
            try:
                actual_value = mapping[key]
            except KeyError:
                actual_sequence += ((key, missing),)
            else:
                actual_sequence += ((key, actual_value),)

        if actual_sequence != expected_sequence:
            diff = "\n" + "\n".join(
                difflib.ndiff(
                    pprint.pformat(expected_sequence).splitlines(),
                    pprint.pformat(actual_sequence).splitlines(),
                )
            )
            additional_values = {k: v for k, v in mapping.items() if k not in expected}
            if additional_values:
                lines = pprint.pformat(additional_values)
                additional = f"\n\nAdditional (non-matched) keys: \n{lines}"
            else:
                additional = ""
            self.fail(f"KV members were not a match. {diff}{additional}")

    def assertPickable(self, what):
        """Assert `what` is pickable."""
        for proto in range(pickle.DEFAULT_PROTOCOL, pickle.HIGHEST_PROTOCOL):
            serialized = pickle.dumps(what, proto)
            self.assertEqual(
                what,
                pickle.loads(serialized),
                msg=(
                    f"Object {what} didn't come up right after pickling/unpickling "
                    f"with protocol version {proto}"
                ),
            )


@contextlib.contextmanager
def captured_output(stream_name):
    """Return a context manager used by captured_stdout/stderr that
    temporarily replaces the sys stream *stream_name* with a StringIO.

    """
    import io

    orig_stdout = getattr(sys, stream_name)
    setattr(sys, stream_name, io.StringIO())
    try:
        yield getattr(sys, stream_name)
    finally:
        setattr(sys, stream_name, orig_stdout)


def captured_stdout():
    """Capture the output of sys.stdout:

    Example::

        with captured_stdout() as stdout:
            print("hello")
        self.assertEqual(stdout.getvalue(), "hello\\n")


    """
    return captured_output("stdout")


def captured_stderr():
    """Capture the output of sys.stderr:

    Example::

        with captured_stderr() as stderr:
            print("hello", file=sys.stderr)
        self.assertEqual(stderr.getvalue(), "hello\\n")

    """
    return captured_output("stderr")


def runModuleDoctest(
    mod_or_name,
    *,
    additional_globals: t.Dict[str, t.Any] = None,
):
    """Run the doctests of the given module.

    All the symbols imported and/or defined in such module will be available to
    the doctests, additional symbols can be provided with `additional_globals`.

    All tests are run with NORMALIZE_WHITESPACE and ELLIPSIS.

    """

    if isinstance(mod_or_name, str):
        module = import_object(mod_or_name)
        modname = mod_or_name
    else:
        module = mod_or_name
        modname = nameof(module, full=True, typed=False, inner=True)
    if not isinstance(module, ModuleType):
        raise ValueError(
            f"{mod_or_name} must be a module or fully qualified name "
            f"to a module.  Got {module}."
        )
    with captured_stdout() as stdout, captured_stderr() as stderr:
        globs = dict(vars(module))
        if additional_globals:
            globs.update(additional_globals)
        failure_count, test_count = doctest.testmod(
            module,
            globs=globs,
            verbose=True,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
            raise_on_error=False,
        )
    if test_count and failure_count:  # pragma: no cover
        print(stdout.getvalue())
        print(stderr.getvalue())
        raise AssertionError(f"{modname} doctest failed")


class BaseTypesTestCase(ExtendedBaseTestCase):
    assertSubtype = ExtendedBaseTestCase.assertLessEqual

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addTypeEqualityFunc(Type, "assertTypesEqual")

    def assertTypeProtocol(self, type_object, data: DataObject = None):
        """Test a type object protocols:

        - It must be full_repr reversible.
        - It must have a simplified_repr
        - It must have a depth greater than zero
        - It must be pickable
        - It must reflexible w.r.t ``==``
        - It must reflexible w.r.t ``<=``

        Additionally if `data` is not None, it must be an object returned by
        `hypothesis.strategies.data`:func:; we will draw a single sample from
        `~xotl.plato.types.Type.get_strategy`:meth: and test it is a member; and draw a single
        member from `~xotl.plato.types.Type.get_serialized_form_strategy`:meth: and test it can
        be parsed.

        We strongly suggest to run this is ``@given`` loop like this::

            @given(types, strategy.data())
            def test_type_protocol(self, type_object, data):
                self.assertTypeProtocol(type_object, data)

        """
        # full_repr is reversible
        self.assertEqual(
            type_object,
            Type.from_full_repr(type_object.full_repr),
        )

        # simplified_repr is not empty and starts with constructor's name
        self.assertTrue(type_object.simplified_repr.startswith(type_object.constructor_name))

        # all types have a depth
        self.assertGreaterEqual(type_object.depth, 0)

        # all types are pickable
        self.assertPickable(type_object)

        # types are reflexible both for equality and sub-typing
        self.assertSubtype(type_object, type_object)
        self.assertEqual(type_object, type_object)

        if data is not None:
            value = data.draw(type_object.get_strategy())
            self.assertTypeMember(value, type_object)

            serial = data.draw(type_object.get_serialized_form_strategy())
            self.assertTypeMember(type_object.parse(serial), type_object)

    @classmethod
    def findTypesFirstDiff(cls, t1, t2) -> t.Tuple[Path, Path]:
        """Find the first *branch* where t1 and t2 are different.

        Report is a pair attr paths that lead to the first, preferably non-high
        level type that is different in both types.

        The algorithm is very trivial and might not stop at the point where you
        expect.  But it will point a difference between the types.

        """
        if t1 == t2:
            return (), ()

        t1_branches: t.List[t.Tuple[PathItem, Type]] = list(t1.iter_typeattrs())
        t2_branches: t.List[t.Tuple[PathItem, Type]] = list(t2.iter_typeattrs())
        # The following 'type: ignore' are needed because type allows for None,
        # str, int which are not comparable between them; but types won't mix
        # them unless ill-implemented.
        t1_branches.sort(key=fst)  # type: ignore
        t2_branches.sort(key=fst)  # type: ignore
        while t1_branches and t2_branches:
            t1_key, t1_type = t1_branches.pop(0)
            t2_key, t2_type = t2_branches.pop(0)
            if t1_key != t2_key:
                return (t1_key,), (t2_key,)
            elif t1_type != t2_type:
                t1_depth = t1_type.depth
                t2_depth = t2_type.depth
                if t1_depth == t2_depth:
                    t1diff, t2diff = cls.findTypesFirstDiff(t1_type, t2_type)
                elif t1_depth < t2_depth:
                    t1diff, t2diff = cls.findTypesFirstDiff(t1, t2_type)
                else:
                    t1diff, t2diff = cls.findTypesFirstDiff(t1_type, t2)
                return (
                    (t1_key,) + tuple(t1diff),
                    (t2_key,) + tuple(t2diff),
                )
        if t1_branches:
            t1_key, _ = t1_branches.pop(0)
            return (t1_key,), ()
        elif t2_branches:
            t2_key, _ = t2_branches.pop(0)
            return (), (t2_key,)
        else:
            return (), ()

    def assertTypesEqual(self, t1, t2, msg=None):
        if t1 != t2:
            if msg is not None:
                raise self.failureException(msg)

            d1, d2 = self.findTypesFirstDiff(t1, t2)
            b1 = t1.traverse(d1)
            b2 = t2.traverse(d2)
            raise self.failureException(
                f"{t1} != {t2}.\nThe first different paths are {d1}, {d2}:\n{b1} != {b2}"
            )

    def assertNotSubtype(self, t, t1, msg=None):
        if t <= t1:
            raise self.failureException(msg or f"Unexpected sub-type {t!r} of {t1!r}")

    def assertTypeMember(
        self,
        value,
        type_object: Type,
        *,
        msg: str = None,
    ):
        try:
            type_object.dump(value, validate=True)
        except (TypeError, ValueError):
            raise self.failureException(
                msg
                or f"Value {value!r} is not a member of type {type_object.simplified_repr!r}"
            )

    def assertNotTypeMember(
        self,
        value,
        type_object: Type,
        *,
        msg: str = None,
    ):
        try:
            type_object.dump(value, validate=True)
        except (TypeError, ValueError):
            pass
        else:
            raise self.failureException(
                msg or f"Unexpected member {value!r} of type {type_object.simplified_repr!r}"
            )

    def assertSubtypeValueRelation(
        self,
        data,
        typed_value: TypedValue,
        supertypes_strategy: t.Callable[[Type], Strategy[Type]] = None,
    ):
        """Assert that a supertype of must contain values of a subtype.

        `data` is value from `hypothesis.strategies.data`:func:.  If
        `supertypes` is None, default to `supertypes`:func:.  Otherwise it must
        be a strategy that takes a type ``t`` and provides generates a supertype
        of ``t``.

        """
        if supertypes_strategy is not None:
            strategy = supertypes_strategy
        else:
            strategy = supertypes
        supertype = data.draw(strategy(typed_value.t))
        self.assertSubtype(typed_value.t, supertype)
        self.assertTypeMember(typed_value.value, supertype)
