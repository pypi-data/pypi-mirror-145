.. _mod-xotl.plato.schema:

==============================================================================
 :mod:`xotl.plato.schema` -- Automatic cast to the type system using schemata
==============================================================================

.. module:: xotl.plato.schema

This module a bridge between `dataclasses`:class: and the `our type system
<xotl.plato.types>`:any:.  We provide a `SchemaBase`:class: applicable to
dataclasses, that then can be easily parsed/dumped with the types.

.. testsetup::

   import enum
   import dataclasses
   from datetime import datetime, date, timedelta
   from xotl.plato.types import *
   from xotl.plato.schema import *


Schemata
========

Schema objects are those that can be *statically* cast into `types
<xotl.plato.types>`:any:.  These objects can be `dumped
<SchemaBase.dump>`:any: using the type object obtained with
`~SchemaBase.get_static_type`:meth:.

The type object basically maps *primitive* python types to the type system of
`xotl.plato.types`:mod:.  This means that there cannot be recursive
definitions.  You can provide a type yourself using `typing.Annotated`:obj:.

Example::

   >>> from dataclasses import dataclass
   >>> from typing_extensions import Annotated
   >>> from xotl.plato.types import *
   >>> from xotl.plato.schema import SchemaBase

   >>> @dataclass
   ... class Foo(SchemaBase):
   ...     name: str
   ...     tags: t.Sequence[str]
   ...     number: t.Optional[int]
   ...     age: Annotated[int, IntegerType(min_value=0, max_value=1000)]

   >>> Foo.get_static_type()
   SchemaType({'name': StringType(),
               'tags': ListType(StringType(...)),
               'number': OptionalType(IntegerType()),
               'age': IntegerType(0, 1000)})

   >>> foo = Foo(name="bar", tags=["baz"], number=-100, age=2)
   >>> foo.dump()
   {'name': 'bar', 'tags': ['baz'], 'number': -100, 'age': 2}

   >>> infoolid = Foo(name="bar", tags=None, number=-100, age=2)
   >>> infoolid.dump()
   Traceback (most recent call last):
   ...
   TypeError: 'NoneType' object is not iterable

Nested schemata are allowed::

   >>> @dataclass
   ... class Bar(SchemaBase):
   ...    name: str
   ...    foo: Foo

   >>> Bar.get_static_type()
   SchemaType({'name': StringType(), 'foo': SchemaType(...)})

   >>> bar = Bar("bat", foo)
   >>> bar.dump()
   {'name': 'bat', 'foo': {...}}

   >>> inbarlid = Bar("bar", infoolid)
   >>> inbarlid.dump()
   Traceback (most recent call last):
   ...
   TypeError: 'NoneType' object is not iterable


Inheritance works::

   >>> @dataclass
   ... class Entity(SchemaBase, abstract=True):
   ...     name: str

   >>> @dataclass
   ... class Person(Entity):
   ...     phone: str

   >>> john = Person("John Doe", "+999 555 000000")
   >>> rel.dump()
   {'name': 'John Doe', 'phone': '+999 555 000000'}

   >>> Person.get_static_type()
   SchemaType({'name': StringType() 'target': StringType()})

.. seealso:: `Abstract schemata`_ for more details.


Annotations that yield two (or more) different types are rejected::

   >>> @dataclass
   ... class NotAChance(SchemaBase):
   ...    something: t.Union[str, int]

   >>> NotAChance.get_static_type()
   Traceback (most recent call last):
   ...
   TypeError: Impossible to find a unique type for 'something' in ...

Annotations of a classes inheriting from `enum.IntEnum`:class:, use
`IntEnumType`:class: Annotations of classes inheriting from `enum.Enum`:class:
(but not from `enum.IntEnum`:class:), use `EnumType`:class:.


Custom parsing and dumping class methods
----------------------------------------

If some of the attributes of your object cannot be feasible represented by a
type object they won't be included in the schema type::

   >>> @dataclass
   ... class Model:   # pretend is an ORM model
   ...    id: int

   >>> @dataclass
   ... class Reference(SchemaBase):
   ...     ref: Model

   >>> Reference.get_static_type()
   SchemaType({})

You can provide the classmethods ``parse_<fieldname>`` and
``dump_<fieldname>`` to parse and dump the values of that attribute::

   >>> @dataclass
   ... class Reference(SchemaBase):
   ...     ref: Model
   ...
   ...     @classmethod
   ...     def parse_ref(cls, value: int) -> Model:
   ...         return Model(value)
   ...
   ...     @classmethod
   ...     def dump_ref(cls, value: Model, *, validate: bool = True) -> int:
   ...          return value.id

   >>> r = Reference(Model(10))
   >>> r.dump()
   {'ref': 10}

.. warning:: You must provide **both** classmethods; otherwise the attribute
   is not included in the schema type.

Custom parsing and dumping completely override the standard types.  You can
use it, for instance to enforce constrains which are not provided by the core
type system.

.. _abstract schemata:

Abstract schemata
-----------------

There a couple of times where you don't really know the actual type of an
schema-object until you call ``dump``.

For instance::

    >>> @dataclass
    ... class Figure(SchemaBase, abstract=True):
    ...     pass

    >>> @dataclass
    ... class Circle(Figure):
    ...     center: t.Tuple[float, float]
    ...     radius: float

    >>> @dataclass
    ... class Rectangle(Figure):
    ...     box: t.Tuple[float, float, float, float]

    >>> @dataclass
    ... class Canvas(SchemaBase):
    ...    figures: t.Sequence[Figure]


In this case ``Figure`` is just a base class for the ``Canvas`` dataclass.  We
mark it with ``abstract=True`` and that makes that dumping a canvas uses a
type-annotated full representation::

    >>> canvas = Canvas([
    ...     Circle((0, 0), 1),
    ...     Rectangle((-1, -1, 1, 1)),
    ... ])
    >>> canvas.dump()
    {'figures': [{':ns:': 'schema', ':base:': '...Circle',
                  'center': (0, 0), 'radius': 1},
                 {':ns:': 'schema', ':base:': '...Rectangle',
                  'box': (-1, -1, 1, 1)}]}

Notice the keys ``:ns:`` and ``:base:`` in the representation of the figures.
This is the way to include the actual schema-type so that it can be parsed
back::

    >>> canvas == Canvas.parse(canvas.dump())
    True

.. note:: `typing.Sequence`:class: uses `~xotl.plato.types.ListType`:class:
   but if you want your classes to store a tuple, use a ``__post_init__`` to
   ensure it.

`SchemaBase`:class: has an empty implementation of ``__post_init__``, this is
allow subclasses to always call ``super().__post_init__()`` in non-trivial
setups of abstract schemata.


.. _schema-base-caching:

Caching of schema types
-----------------------

By default subclasses will use a cache for `get_static_type`:meth:.  There
are two ways to control this cache.

To remove the cache completely you can create the schema class with
`cached=False`::

     >>> @dataclass
     ... class Foo(SchemaBase, cached=False):
     ...     name: str

     >>> Foo.get_static_type() is not Foo.get_static_type()
     True

Calling `get_static_type`:meth: with the argument ``cached=False``::

     >>> @dataclass
     ... class Foo(SchemaBase):
     ...     name: str

     >>> Foo.get_static_type() is Foo.get_static_type()
     True

     >>> Foo.get_static_type() is not Foo.get_static_type(cached=False)
     True

.. note:: Calling ``get_static_type(cached=False)`` doesn't read the cache but
   **it does update it**.

   This allows to reset the cache after calls to
   `register_simple_type_map`:func: or `temp_simple_type_map`:func:\ ::

       >>> @dataclass
       ... class Foo(SchemaBase):
       ...     dt: datetime

       >>> Foo.get_static_type().shape['dt'].use_pytz
       False

       >>> register_simple_type_map(datetime, lambda: DateTimeType(use_pytz=True))
       >>> Foo.get_static_type().shape['dt'].use_pytz  # still cached
       False

       >>> Foo.get_static_type(cached=False).shape['dt'].use_pytz
       True

       >>> reset_simple_type_map(datetime)
       >>> Foo.get_static_type().shape['dt'].use_pytz  # still cached
       True

       >>> Foo.get_static_type(cached=False).shape['dt'].use_pytz
       False

API
---

.. autoclass:: SchemaBase

   .. automethod:: get_static_type

   .. automethod:: dump

   .. automethod:: parse

   .. autoattribute:: full_repr

   .. method:: from_full_repr
      :classmethod:

      Rebuild the object from the `full representation <full_repr>`:class:.

      This mostly only used in some specific scenarios and directly by the
      `abstract schemata`_ machinery.

      `from_full_repr` disregards the actual class from you're calling it and
      will return a type depending solely on the keys ``:ns:`` and ``:base:``.
      (However, to keep static checkers happy, you should do it in from
      super-classes.)

   .. automethod:: reset_static_type_cache

      .. seealso:: `Caching of schema types`_.


.. _schemata-type-extensions:

Extensions to the core type system to support schemata
======================================================

Schemata's type system includes some extensions to the type system which are
useful to bridge some Python's type that don't have an obvious type object in
`xotl.plato.types`:mod:.

.. class:: SchemaType

   This is the type object returned by `SchemaBase.get_static_type`:meth:.
   It's similar to `~xotl.plato.types.ObjectType`:class: but it must keep a
   reference to the dataclass to be able to create instances with
   `SchemaBase.from_full_repr`:meth:

.. autoclass:: EnumType

.. autoclass:: IntEnumType

.. autoclass:: FullReprType

   This type will simply use ``full_repr`` and ``from_full_repr`` to dump and
   parse.  So it will only work for values that support that protocol (i.e
   `SchemaBase`:class: and `~xotl.plato.types.Type`:class:).

   It was specifically create to support the parsing and dumping based on
   `abstract schemata`:ref:.

.. autofunction:: register_simple_type_map

.. autofunction:: reset_simple_type_map

.. autofunction:: temp_simple_type_map
