.. _mod-xotl.plato.types:

============================================
 :mod:`xotl.plato.types` -- The type system
============================================

.. module:: xotl.plato.types

A simple type system which allows to communicate the structure of simple
(non-recursive) data structures.

Types are objects that allow to capture the basic structure of other objects
(values).

So a type lives two lives:

- When is just a value to be sent to frontends so they can choose the right
  widget for some value.

- As a serializer/parser of values of the type.

.. testsetup::

   from datetime import datetime, date, timedelta
   from xotl.plato.types import *


Base classes
============

.. class:: Type(typing.Generic[S, I])

   The base class for all type objects.  It's generic over type variables
   ``S`` (serialized form) and ``I`` (internal form).

   .. method:: parse(raw_value: S) -> I

      Take a *serialized form*, parse it and return the corresponding internal
      form.  Parsing can raise errors like ValueError, TypeError, KeyError,
      AttributeError depending on the type object, the actual type ``S``, and
      the nature of the error while trying to parse the `raw_value`.

   .. method:: dump(value: I, *, validate: bool = True) -> S

      Take an *internal form*, and return the corresponding internal form.

      When `validate` is False, most types skip *constraints* but still check
      the basic type of the `value`.  For instance:

      .. doctest::

         >>> IntegerType(1, 5).dump(5, validate=False)
         5

         >>> IntegerType(1, 5).dump(5)
         Traceback (most recent call last):
         ...
         ValueError: Value 5 not in Range(Included(1), Excluded(5))

         >>> IntegerType(1, 5).dump(None, validate=False)
         Traceback (most recent call last):
         ...
         TypeError: Invalid IntegerType value None


     Which constraints are skipped and which are not is type-specific.  But
     the general idea is to allow serialization of the same *internal forms*
     that make up the types arguments.

     For example, in order to `dump`:meth: the arguments of
     `DateTimeType`:class:, we need to use ``DateTimeType.dump()`` on them,
     and that could raise a ValueError if any of the boundaries is
     `xotless.ranges.Excluded`:class:.

   .. classmethod:: get_static_type() -> Type

      Return a `~xotl.plato.schema.SchemaType` that can parse/dump instances
      of the type object.

      Example:

      .. doctest::

         >>> t1 = IntegerType(1, 5)
         >>> IntegerType.get_static_type().dump(t1)
         {'min_value': 1, 'max_value': 5, 'min_included': True, 'max_included': False, 'selection': None}

         >>> metatype = IntegerType.get_static_type()
         >>> metatype.parse(metatype.dump(t1)) == t1
         True

      Internally types are also described using the core type systems with the
      `couple of extension <schemata-type-extensions>`:ref: use for schemata.


   .. property:: namespace
      :type: typing.Optional[str]
      :classmethod:

      Combined with `constructor_name`:attr: allows to identify the actual
      type in `full_repr`:attr:.  Types always return None, but some
      extensions might return a different value.

   .. property:: constructor_name
      :type: str
      :classmethod:

      This is basically the name of the class without is arguments.  It serves
      the purpose of recognizing the object during serialization
      (`full_repr`:attr:).

   .. property:: simplified_repr:
      :type: str

      A simplified string representation of the type, suitable for humans.

   .. property:: full_repr
      :type: xotl.plato.base.FullRepr

      A full dict representation of the type suitable for JSON dumping.

      The result always has the keys ":ns:" set to `namespace`:attr:, and
      ":base:" set to `constructor_name`:attr:.  Other keys depend on the
      specific object and match their arguments.

   .. method:: from_full_repr(full_repr: FullRepr) -> Type:
      :classmethod:

      Reconstruct the Type Object from its `full representation
      `full_repr`:class:.

      In order to this to work we have implemented ``__init_subclass__`` with
      keeps a registry of types based on the `namespace`:attr: and
      `constructor_name`:attr:.  This can cause some pain if you implement a
      custom type that uses the same values for those properties.

   .. rubric:: Traversing types

   .. automethod:: gettypeattr

   .. automethod:: traverse

   .. rubric:: Testing facilities

   .. automethod:: get_strategy

   .. automethod:: get_serialized_form_strategy

   .. rubric:: Basic sub-typing

   Types implement ``__le__`` to test whether a type of a sub-type of `other`.
   See `Sub-typing`_.

   .. warning:: Don't use other any other operator except ``<=`` for
                sub-typing testing.

Sub-typing
----------

This is a very trivial subtyping relation.

The following MUST hold, but we cannot ensure it for types made by third
parties:

- If ``t1 <= t2``, then for all value ``v: t1``, ``v: t2`` must also hold.
  The test for membership is actually that calling `~Type.dump`:meth: passing
  ``v`` doesn't fail.

- Reflexive: ``t <= t`` for all types ``t``.

- Transitive: If ``a <= b`` and ``b <= c``, then ``a <= c``.

- Antisymmetric: If ``a <= b`` and ``a != b``, then it cannot be
  ``b <= a``.

You should note that we don't follow Python's sub-typing.  In particular:

- No instance of `BooleanType`:class: is ever a sub-type of (instances of)
  `IntegerType`:class:.

- `IntegerType`:class: is never a subtype of `FloatType`:class:

- `ListType`:class: is covariant on its type-argument, i.e
  ``ListType(t1) <= ListType(t2)`` if and only if ``t1 <= t2``.


Types that support boundaries
=============================

.. class:: MinMax(typing.Generic[xotless.types.TOrd])

   Types that can constraint their values in a `range
   <xotless.ranges.Range>`:any:, inherit from this class.  They all have the
   following attributes:

   .. attribute:: min_value
      :type: t.Optional[TOrd]
      :value: None

   .. attribute:: max_value
      :type: t.Optional[TOrd]
      :value: None

   .. attribute:: min_included
      :type: bool
      :value: True

   .. attribute:: max_included
      :type: bool
      :value: False

   If `min_value`:attr: is None, `min_included`:attr: is ignored and values
   have no minimal boundary, except perhaps a boundary imposed by the
   *internal form type system* or the *serialized form type system*.  For
   instance, dates must greater or equal to `datetime.date.min`:attr: and less
   or equal to `datetime.date.max`:attr:.

   If `max_value`:attr: is None, `max_included`:attr: is ignored and values
   have no maximal boundary, except perhaps a boundary imposed by the
   *internal form type system* or the *serialized form type system*.

   Some of these types support the following attribute:

   .. attribute:: MIN_POSSIBLE_VALUE
      :type: typing.ClassVar[typing.Optional[xotless.types.TOrd]]
      :value: None

   which is exclusively used in tests to generate values that can be safely
   cast to JSON, stored in JSON columns in postgres, etc.

   .. property:: range
      :type: xotless.ranges.Range[TOrd]

      The `range <xotless.ranges.Range>`:class: over min/max values.

      This property always has a value and its memoized upon access.  When
      `min_value`:attr: is None, use ``Excluded(-Infinity)``.  When
      `max_value`:attr: is None, we ``Excluded(Infinity)``.

   .. rubric:: Sub-typing

   A min/max type ``t1`` is a subtype of another ``t2``, when
   ``t1.range <= t2.range``.


Types that support selections
=============================

.. class:: Selectable(typing.Generic[T])

   Mixin for types that support a selection.

   Type objects that allow selections, can be initialized with an argument
   `selection <Selection>`:class: with a sequence of `SelectionData`:class:
   objects describing each possible value.

   .. rubric:: Sub-typing

   A selection-based type ``t1`` is a subtype of another ``t2`` is the set of
   `values <Selection.get_values>`:any: of ``t1`` is a subset of the set of
   values of ``t2``.  Notice that names of each selection are not taken into
   account for sub-typing.

.. autoclass:: SelectionData

.. autoclass:: Selection
   :members: from_pairs, get_name, get_values


Catalog of types
================

.. autoclass:: IntegerType(min_value: int = None, max_value: int = None, min_included: bool = True, max_included: bool = False, selection: Selection[int] = None)

.. autoclass:: StringType(selection: Selection[str]=None, max_length: int = None)

.. autoclass:: FloatType(min_value: float = None, max_value: float = None, min_included: bool = True, max_included: bool = False)

.. autoclass:: DateType(min_value: date = None, max_value: date = None, min_included: bool = True, max_included: bool = False)

.. autoclass:: DateTimeType(min_value: datetime = None, max_value: datetime = None, min_included: bool = True, max_included: bool = False)

.. autoclass:: DurationType(min_value: timedelta = None, max_value: timedelta = None, min_included: bool = True, max_included: bool = False)

.. autoclass:: TupleType(bases: t.Sequence[Type])

.. autoclass:: ObjectType(shape: t.Mapping[str, Type])

.. autoclass:: ListType(of: Type[S, I])

.. autoclass:: OptionalType(type: Type[S, I])

.. autoclass:: MappingType(key_value: Type[KS, KI], value_type: Type[VS, VI])
