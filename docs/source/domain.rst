Bazel domain
============

Bazel Workspace
---------------

To describe a bazel workspace use ``bazel:workspace::`` ::

   .. bazel:workspace:: my_workspace_name

      Package content

This has no direct output, but following definitions of packages or targets are assigned to this workspace.

.. bazel:workspace:: my_workspace_name


Bazel Package
-------------

To describe a bazel package use ``bazel:package::``::

   .. bazel:package:: Package

      Package content

**Result**

.. bazel:package:: /#+34/testmy/package

   Package content




python domain tests
-------------------

**module**

.. py:module:: my_module

*os*

.. py:module:: os

**function**

.. py:function:: my_function(arg1, arg2, name=arg3)

   my test function

   :type test: tuple(float, string)
   :param test: argh


**exception**

.. py:exception:: MY_EXCEPTION

   Ohh nooo, BUMM!


**class**

.. py:class:: Foo

   .. py:method:: quux()

-- or --

.. py:class:: Bar

.. py:method:: Bar.quux()