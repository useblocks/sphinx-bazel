.. _bazel_domain:

Bazel domain
============

The Sphinx Bazel domain allows the definition and documentation of Bazel objects like ``Workspace`` and ``Package``.

Therefore it provides the following directives:

   * bazel:workspace
   * bazel:package

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

workspace
~~~~~~~~~

``:workspace:`` can be used to print also the name of related workspace::

   .. bazel:workspace:: workspace_example

      Workspace for testing ``workspace`` option

   .. bazel:package:: //my/package
      :workspace:

      Some input

**Result**

.. bazel:workspace:: workspace_example

   Workspace for testing ``workspace`` option

.. bazel:package:: //my/package
      :workspace:

      Some input


workspace_path
~~~~~~~~~~~~~~

``:workspace_path:`` can be used to get the path of the used workspace printed::

   .. bazel:workspace:: workspace_path_example
      :path: /path/to/my/workspace

      Workspace for testing ``workspace_path`` option

   .. bazel:package:: //my/package
      :workspace_path:

      Some input

**Result**

.. bazel:workspace:: workspace_path_example
   :path: /path/to/my/workspace

   Workspace for testing ``workspace_path`` option

.. bazel:package:: //my/package
   :workspace_path:

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

workspace
~~~~~~~~~

``:workspace:`` can be used to print also the name of related workspace::

   .. bazel:workspace:: workspace_target_example

      Workspace for testing ``workspace`` option

   .. bazel:target:: //my/package
      :workspace:

      Some input

**Result**

.. bazel:workspace:: workspace_target_example

   Workspace for testing ``workspace`` option

.. bazel:target:: //my/package:target
      :workspace:

      Some input


workspace_path
~~~~~~~~~~~~~~

``:workspace_path:`` can be used to get the path of the used workspace printed::

   .. bazel:workspace:: workspace_target_path_example
      :path: /path/to/my/workspace

      Workspace for testing ``workspace_path`` option

   .. bazel:target:: //my/package
      :workspace_path:

      Some input

**Result**

.. bazel:workspace:: workspace_target_path_example
   :path: /path/to/my/workspace

   Workspace for testing ``workspace_path`` option

.. bazel:target:: //my/package:target
   :workspace_path:

   Some input