==========================================
 Basic (non-recursive) "platonic" schemata
==========================================

This package allows to serialize/deserialize data in a JSON friendly manner by
using and manipulating types.

It features a type system that is extensible and it has been specifically
designed to avoid non-termination issues with recursive data.  In a word, we
don't allow to create recursive types; any notion of recursion is not part of
the type system itself.

Having these types, we can now cast dataclasses into schemata by attaching a
type to it.  We can automatically build the type of most basic Python types,
enumerations and other.
