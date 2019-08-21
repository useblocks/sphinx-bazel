.. _bazel_domain:

Bazel domain
============

The Sphinx Bazel domain allows the definition and documentation of Bazel objects like ``Workspace`` and ``Package``.

Therefore it provides the following directives:

   * :ref:`domain_workspace`
   * :ref:`domain_package`
   * :ref:`domain_target`
   * :ref:`domain_rule`
   * :ref:`domain_macro`
   * :ref:`domain_implementation`
   * :ref:`domain_attribute`

The content part of each directive supports fully RsT, so you are free to add lists, images or functions from
other Sphinx extensions.

.. contents::
   :local:

.. _domain_workspace:

bazel:workspace
---------------

To describe a bazel workspace use ``bazel:workspace``::

   .. bazel:workspace:: my_workspace_name

      Some **awesome** workspace description.

**Result**

.. bazel:workspace:: my_workspace_name

   Some **awesome** workspace description.

Every following definition of a package or a target get automatically assigned this this workspace, until you defined
a new workspace.

hide
~~~~

``:hide:`` can be used to get the defined workspace not printed into the document.
But it was created and packages/targets defined after this get assigned to it. ::

   .. bazel:workspace:: my_invisible_workspace
      :hide:

      You will not see anything

**Result**

Ohh surprise, nothing to show here :)


path
~~~~

``:path:`` allows to define a folder path, which stores the workspace.
If set the path will be printed after the workspace name.

**Example**

Use ``:path:`` like this::

   .. bazel:workspace:: another_workspace
      :path: C:\\projects\proj_a\workspace\

      Some workspace description.

**Result**

.. bazel:workspace:: another_workspace
   :path: C:\\projects\proj_a\workspace\

   Some workspace description.

.. _domain_package:

bazel:package
-------------

To describe a Bazel package use ``bazel:package``::

   .. bazel:package:: //my/package

      Package content:

      * rule A
      * macro X
      * file 1

**Result**

.. bazel:package:: //my/package

      Package content:

      * rule A
      * macro X
      * file 1

show_workspace
~~~~~~~~~~~~~~

``:show_workspace:`` can be used to print also the name of related workspace::

   .. bazel:workspace:: workspace_example

      Workspace for testing ``workspace`` option

   .. bazel:package:: //my/package
      :show_workspace:

      Some input

**Result**

.. bazel:workspace:: workspace_example

   Workspace for testing ``workspace`` option

.. bazel:package:: //my/package
      :show_workspace:

      Some input


show_workspace_path
~~~~~~~~~~~~~~~~~~~

``:show_workspace_path:`` can be used to get the path of the used workspace printed::

   .. bazel:workspace:: workspace_path_example
      :path: /path/to/my/workspace

      Workspace for testing ``workspace_path`` option

   .. bazel:package:: //my/package
      :show_workspace_path:

      Some input

**Result**

.. bazel:workspace:: workspace_path_example
   :path: /path/to/my/workspace

   Workspace for testing ``workspace_path`` option

.. bazel:package:: //my/package
   :show_workspace_path:

   Some input

.. _domain_target:

bazel:target
------------

To describe a Bazel target use ``bazel:target``::

   .. bazel:target:: //my/package:target

      This target is a really nice looking one.

**Result**

.. bazel:target:: //my/package:target

   This target is a really nice looking one.

It gets automatically assigned to latest defined workspace.

show_workspace
~~~~~~~~~~~~~~

``:show_workspace:`` can be used to print also the name of related workspace::

   .. bazel:workspace:: workspace_target_example

      Workspace for testing ``workspace`` option

   .. bazel:target:: //my/package
      :show_workspace:

      Some input

**Result**

.. bazel:workspace:: workspace_target_example

   Workspace for testing ``workspace`` option

.. bazel:target:: //my/package:target
      :show_workspace:

      Some input


show_workspace_path
~~~~~~~~~~~~~~~~~~~

``:show_workspace_path:`` can be used to get the path of the used workspace printed::

   .. bazel:workspace:: workspace_target_path_example
      :path: /path/to/my/workspace

      Workspace for testing ``workspace_path`` option

   .. bazel:target:: //my/package
      :show_workspace_path:

      Some input

**Result**

.. bazel:workspace:: workspace_target_path_example
   :path: /path/to/my/workspace

   Workspace for testing ``workspace_path`` option

.. bazel:target:: //my/package:target
   :show_workspace_path:

   Some input

.. _domain_rule:

bazel:rule
----------

To describe a Bazel rule use ``bazel:rule``::

   .. bazel:rule:: //my/package:file.bzl:my_rule

      This is **my_rule**

**Result**

.. bazel:rule:: //my/package:file.bzl:my_rule

   This is **my_rule**

It gets automatically assigned to latest defined workspace.

implementation
~~~~~~~~~~~~~~

``:implementation:`` can be used to define the name of the used implementation function for the rule::

   .. bazel:workspace:: workspace_rule_impl_example

      Workspace for testing ``implementation`` option

   .. bazel:rule:: //my/package:target:rule
      :implementation: __my_rule_func

      Some input

**Result**

.. bazel:workspace:: workspace_rule_impl_example
   :path: /path/to/my/workspace

   Workspace for testing ``implementation`` option

.. bazel:rule:: //my/package:target:rule
   :implementation: __my_rule_func

   Some input

.. note::

   You have to use :ref:`rule_show_implementation` to get the value also printed.

.. _rule_invocation:

invocation
~~~~~~~~~~

``:invocation:`` allows the definition of a invocation string to show how to call/use this rule::

   .. bazel:rule:: //my/package:target:rule
      :invocation: rule(attribute_1, attribute_2)

      Some input

.. bazel:rule:: //my/package:target:rule
   :invocation: rule(attribute_1, attribute_2)

   Some input

.. note::

   You have to use :ref:`rule_show_invocation` to get the value also printed.

.. _rule_show_implementation:

show_implementation
~~~~~~~~~~~~~~~~~~~

``:show_implementation:`` can be used to print the name of the used implementation function for the rule::

   .. bazel:workspace:: workspace_rule_impl_example

      Workspace for testing ``implementation`` option

   .. bazel:rule:: //my/package:target:rule
      :implementation: __my_rule_func
      :show_implementation:

      Some input

**Result**

.. bazel:workspace:: workspace_rule_show_impl_example
   :path: /path/to/my/workspace

   Workspace for testing ``implementation`` option

.. bazel:rule:: //my/package:target:rule
   :implementation: __my_rule_func
   :show_implementation:

   Some input

.. _rule_show_invocation:

show_invocation
~~~~~~~~~~~~~~~

``:show_invocation:`` prints the invocation string::

    .. bazel:rule:: //my/package:target:rule
      :invocation: rule(attribute_1, attribute_2)
      :show_invocation:

      Some input

**Result**

.. bazel:rule:: //my/package:target:rule
   :invocation: rule(attribute_1, attribute_2)
   :show_invocation:

   Some input

show_workspace
~~~~~~~~~~~~~~

``:show_workspace:`` can be used to print also the name of related workspace::

   .. bazel:workspace:: workspace_rule_example

      Workspace for testing ``workspace`` option

   .. bazel:rule:: //my/package:target:rule
      :show_workspace:

      Some input

**Result**

.. bazel:workspace:: workspace_rule_example

   Workspace for testing ``workspace`` option

.. bazel:rule:: //my/package:target:rule
   :show_workspace:

   Some input


show_workspace_path
~~~~~~~~~~~~~~~~~~~

``:show_workspace_path:`` can be used to get the path of the used workspace printed::

   .. bazel:workspace:: workspace_ule_path_example
      :path: /path/to/my/workspace

      Workspace for testing ``workspace_path`` option

   .. bazel:rule:: //my/package:target:rule
      :show_workspace_path:

      Some input

**Result**

.. bazel:workspace:: workspace_rule_path_example
   :path: /path/to/my/workspace

   Workspace for testing ``workspace_path`` option

.. bazel:rule:: //my/package:target:rule
   :show_workspace_path:

   Some input

.. _domain_macro:

bazel:macro
-----------

To describe a Bazel macro use ``bazel:macro``::

   .. bazel:macro:: //my/package:file.bzl:my_macro

      This is a **macro**

**Result**

.. bazel:macro:: //my/package:file.bzl:my_macro

   This is a **macro**

It gets automatically assigned to latest defined workspace.

.. _domain_implementation:

bazel:implementation
--------------------
**Shortcut**: ``bazel:impl``

To describe a Bazel implementation use ``bazel:implementation``::

   .. bazel:implementation:: //my/package:file.bzl:_my_impl

      You can also use ``bazel:impl`` to define this.

**Result**

.. bazel:implementation:: //my/package:file.bzl:_my_impl

   You can also use ``bazel:impl`` to define this.

It gets automatically assigned to latest defined workspace.

.. _domain_attribute:

bazel:attribute
---------------

Attributes are used inside Bazel rules.

To document a single attribute use
``bazel:attribute``::

   .. bazel:attribute:: //my/package:file.bzl:my_rule:attribute_1

      Takes a string, which is used to perform **awesome** stuff


**Result**

.. bazel:attribute:: //my/package:file.bzl:my_rule:attribute_1

      Takes a string, which is used to perform **awesome** stuff

Common options
--------------

Following options have all above directives in common.

.. _domain_option_show_type:

show_type
~~~~~~~~~

Adds a prefix like ``package:`` to show the type.

If using HTML as builder, the prefix will have the css classes: **bazel** , **type** and one of the following
types: **workspace**, **package**, **rule**, **implementation**, **macro** or **attribute**.


.. code-block:: rst

   .. bazel:package:: //main
      :show_type:

      An awesome bazel package


**Result**

.. bazel:package:: //main
   :show_type:

   An awesome bazel package


