import contextlib
import dataclasses
import typing as t
from dataclasses import dataclass

from hypothesis import given, settings
from hypothesis import strategies as st
from xotl.plato.schema import CustomizedAttrType, SchemaBase
from xotl.plato.testing import (
    BaseTypesTestCase,
    ExtendedBaseTestCase,
    TypedValue,
    date_types,
    datetime_types,
    duration_types,
    float_types,
    floats,
    hashable_types,
    high_level_types,
    integer_types,
    integer_types_with_selections,
    nonhashable_types,
    object_types,
    optional_types,
    string_types,
    string_types_with_selections,
    strings,
    supertypes,
    types,
    with_min_or_max,
)
from xotl.plato.types import (
    BaseNumberType,
    DateTimeType,
    DateType,
    DurationType,
    FloatType,
    IntegerType,
    ListType,
    MinMaxType,
    ObjectType,
    OptionalType,
    StringType,
    Type,
)
from xotl.tools.objects import temp_attributes


class TestTypes(BaseTypesTestCase):
    @given(types)
    def test_type_full_reprs(self, type_object):
        self.assertTypeProtocol(type_object)

    @given(types)
    def test_type_reprs(self, type_object):
        import datetime

        from xotl.plato.types import BooleanType, MappingType, SelectionData, TupleType

        context = dict(
            globals(),
            datetime=datetime,
            BooleanType=BooleanType,
            MappingType=MappingType,
            SelectionData=SelectionData,
            TupleType=TupleType,
        )
        type_object_full_repr = type_object.full_repr
        reconstructed = eval(repr(type_object), context)
        self.assertEqual(
            type_object,
            reconstructed,
            msg=f"{type_object_full_repr} != {reconstructed.full_repr}",
        )

    @given(TypedValue.strategy(hashable_types))
    def test_parsing_dumping_hashable_values(self, typed_value: TypedValue):
        type_object, value = typed_value
        assert type_object.parse(type_object.dump(value)) == value

    @given(TypedValue.strategy(nonhashable_types))
    def test_parsing_dumping_nonhashable_values(self, typed_value: TypedValue):
        type_object, value = typed_value
        assert type_object.parse(type_object.dump(value)) == value

    @settings(deadline=None)
    @given(st.data(), integer_types.filter(with_min_or_max))
    def test_integer_type_ensure_min_and_max(self, data, t: IntegerType):
        self._test_minmax(data, t, st.integers)

    @settings(deadline=None)
    @given(st.data(), float_types.filter(with_min_or_max))
    def test_float_types_ensure_min_and_max(self, data, t: FloatType):
        self._test_minmax(data, t, floats)

    @settings(deadline=None)
    @given(st.data(), date_types.filter(with_min_or_max))
    def test_date_types_ensure_min_and_max(self, data, t: DateType):
        def dates(**kwargs):
            min_value = max(
                kwargs.pop(
                    "min_value",
                    DateType.MIN_POSSIBLE_VALUE,
                ),
                DateType.MIN_POSSIBLE_VALUE,
            )
            return st.dates(min_value=min_value, **kwargs)

        self._test_minmax(data, t, dates)

    @settings(deadline=None)
    @given(st.data(), datetime_types.filter(with_min_or_max))
    def test_datetime_types_ensure_min_and_max(self, data, t: DateTimeType):
        def datetimes(**kwargs):
            min_value = max(
                kwargs.pop("min_value", DateTimeType.MIN_POSSIBLE_VALUE),
                DateTimeType.MIN_POSSIBLE_VALUE,
            )
            return st.datetimes(min_value=min_value, **kwargs)

        self._test_minmax(data, t, datetimes)

    @settings(deadline=None)
    @given(st.data(), duration_types.filter(with_min_or_max))
    def test_duration_types_ensure_min_and_max(self, data, t: DurationType):
        def durations(**kwargs):
            min_value = max(
                kwargs.pop(
                    "min_value",
                    DurationType.MIN_POSSIBLE_VALUE,
                ),
                DurationType.MIN_POSSIBLE_VALUE,
            )
            return st.timedeltas(min_value=min_value, **kwargs)

        self._test_minmax(data, t, durations)

    def _test_minmax(
        self,
        data,
        t: t.Union[MinMaxType, BaseNumberType],
        minmax_strategy_factory,
    ):
        if (min_value := t.min_value) is not None:
            invalid_values = minmax_strategy_factory(max_value=min_value)
            if t.min_included:
                invalid_values = invalid_values.filter(lambda i: i != min_value)
        elif (max_value := t.max_value) is not None:
            invalid_values = minmax_strategy_factory(min_value=max_value)
            if t.max_included:
                invalid_values = invalid_values.filter(lambda i: i != max_value)
        value = data.draw(invalid_values)
        self.assertNotTypeMember(value, t)

    @settings(deadline=None)
    @given(st.data(), string_types.filter(lambda t: t.selection))
    def test_string_types_ensure_selection(self, data, t: StringType):
        possible_values = {v for v, _ in t.selection}  # type: ignore
        value = data.draw(strings().filter(lambda s: s not in possible_values))
        self.assertNotTypeMember(value, t)

    @settings(deadline=None)
    @given(st.data(), integer_types.filter(lambda t: t.selection))
    def test_integer_types_ensure_selection(self, data, t: StringType):
        possible_values = {v for v, _ in t.selection}  # type: ignore
        value = data.draw(st.integers().filter(lambda s: s not in possible_values))
        self.assertNotTypeMember(value, t)

    @given(optional_types())
    def test_optional_type_flattens(self, optional_type: OptionalType):
        self.assertEqual(OptionalType(optional_type), optional_type)

    @given(high_level_types | types)
    def test_iter_typeattrs(self, type_object: Type):
        for typeattr, expected in type_object.iter_typeattrs():
            result = type_object.gettypeattr(typeattr)
            self.assertEqual(result, expected, msg=f"{result} != {expected}")


class TestSubtyping(BaseTypesTestCase):
    @given(types)
    def test_types_are_reflexible(self, type_object):
        self.assertSubtype(type_object, type_object)
        self.assertSubtype(
            type_object,
            Type.from_full_repr(type_object.full_repr),
        )

    def assertSubtypeValueRelation(self, data, t: Type, value: t.Any):
        supertype = data.draw(supertypes(t))
        self.assertSubtype(t, supertype)
        self.assertTypeMember(value, supertype)

    @given(st.data(), TypedValue.strategy())
    def test_subtype_values(self, data, typed_value: TypedValue):
        self.assertSubtypeValueRelation(data, typed_value.t, typed_value.value)

    @settings(deadline=None)
    @given(st.data(), object_types(), types)
    def test_object_types_require_match(
        self,
        data,
        object_type: ObjectType,
        type_object: Type,
    ):
        shape = dict(object_type.shape)
        # Our strategy only generates keys from 'attr0' to 'attr9', so can
        # assume 'extra' is already in the shape.
        shape["extra"] = OptionalType(type_object)
        self.assertNotSubtype(object_type, t2 := ObjectType(shape))
        try:
            value = data.draw(object_type.get_strategy())
        except TypeError as cause:
            raise TypeError(f"While drawing values from {object_type!r}") from cause
        self.assertNotTypeMember(value, t2)

    def test_types_docstests(self):
        self.runModuleDoctest("xotl.plato.types")

    def test_testing_docstests(self):
        self.runModuleDoctest("xotl.plato.testing")

    @given(types, types)
    def test_types_are_comparable(self, t1, t2):
        # Basically,  t1 <= t2 will always be True or False, not a TypeError.
        self.assertIn(t1 <= t2, (True, False))

    @given(string_types_with_selections | integer_types_with_selections)
    def test_subtyping_with_selections(self, with_selection):
        without_selection = dataclasses.replace(with_selection, selection=None)
        self.assertSubtype(with_selection, without_selection)

        self.assertSubtype(OptionalType(with_selection), OptionalType(without_selection))
        self.assertSubtype(ListType(with_selection), ListType(without_selection))


class TestSchemata(ExtendedBaseTestCase):
    def test_schema_docstests(self):
        self.runModuleDoctest("xotl.plato.schema")

    def test_regression_inheriting_customized_attrs(self):
        @dataclass
        class Customized(SchemaBase, abstract=True):
            attr_path: t.Sequence[t.Union[int, str, None]]

            @classmethod
            def parse_attr_path(cls, raw_value):
                return raw_value

            @classmethod
            def dump_attr_path(cls, value, *, validate: bool = True):
                return value

        @dataclass
        class Inherited(Customized):
            pass

        self.assertIsInstance(
            Inherited.get_static_type().shape["attr_path"],
            CustomizedAttrType,
        )
