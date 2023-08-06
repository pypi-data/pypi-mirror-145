===============================
 Basic (non-recursive) schemata
===============================


Overview
========

This package allows to serialize/deserialize data in a JSON friendly manner by
using and manipulating types.

It features a `type system <xotl.plato.types>`:any: that is extensible and it
has been specifically designed to avoid non-termination issues with recursive
data.  In a word, we don't allow to create recursive types; any notion of
recursion is not part of the type system itself.

Having these types, we can now cast `dataclasses`:mod: into `schemata
<xotl.plato.schema>`:any: by attaching a `type <xotl.plato.types>`:any: to
them.  We can automatically build the type of most basic Python types,
enumerations and other.


Why not Pydantic_
=================

Most of the code in this package comes from two projects we have worked
before.  At the time we crafted the (actual) first version of this code, we
didn't know about Pydantic_.

Since then we have *fantasized* with the idea of ditching this code and go all
the way to Pydantic_, but we have failed to cover some specifics areas,
specially being able to deserialize objects without knowing their actual types
but only a base class.

Pydantic also strongly positions itself as *data validation* library, and
while need validation we also need serialization and deserialization.

Finally, the most important part of this package is the type system; schemata
were actually created after to provide a mechanized way to create types of
dataclasses.


.. _Pydantic: https://pydantic-docs.helpmanual.io/
