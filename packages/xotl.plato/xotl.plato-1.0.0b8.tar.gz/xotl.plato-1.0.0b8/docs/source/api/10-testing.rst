======================================
 :mod:`xotl.plato.testing` -- Testing
======================================

.. module:: xotl.plato.testing

.. class:: BaseTypesTestCase

   .. method:: assertSubtype(t: xotl.plato.types.Type, t1: xotl.plato.types.Type, msg: str=None)

      Assert `t` is a sub-type of `t1`.  This is basically an alias of
      `unittest.TestCase.assertLessEqual`.

   .. method:: assertNotSubtype(t: xotl.plato.types.Type, t1: xotl.plato.types.Type, msg: str=None)

      Assert `t` is not a sub-type of `t1`.

   .. method:: assertTypeMember(value: typing.Any, t: xotl.plato.types.Type, *, msg: str=None)

      Assert `value` is of type `t`.

   .. method:: assertNotTypeMember(value: typing.Any, t: xotl.plato.types.Type, *, msg: str=None)

      Assert `value` is not of type `t`.

   .. automethod:: assertSubtypeValueRelation

   .. automethod:: assertTypeProtocol

.. autoclass:: TypedValue
   :members: value, t, from_args, strategy

.. autofunction:: supertypes
