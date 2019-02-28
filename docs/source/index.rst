.. Sphinx-Bazel documentation master file, created by
   sphinx-quickstart on Mon Feb 18 12:08:31 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Sphinx-Bazel: rules inside sphinx
=================================

``Sphinx-Bazel`` is an extension for the `sphinx documentation generator <hhtps://sphinx-doc.org>`_ and allows the
documentation of `Bazel <https://bazel.build>`_ objects inside any sphinx project.

Following Bazel objects are supported:

* Workspace
* Package
* Target

The documentation can be written by hand or can be generated automatically based on existing Bazel folders and files.

Manual documentation
--------------------

.. code-block:: rst

   .. bazel:target:: //my/package:target

      This **Bazel** target builds my sources.

**Result**

.. bazel:workspace:: dummy_workspace
      :hide:

.. bazel:target:: //my/package:target

   This **Bazel** target builds my sources.

Following domain-specific directives are provided:

 * bazel:workspace
 * bazel:package
 * bazel:target

**Examples**

.. code-block:: rst

   .. bazel:workspace:: my_workspace

   .. bazel:package:: //my/package

   .. bazel:target:: //my/package:target


Automated documentation
-----------------------

.. code-block:: rst

   .. autobazel-workspace:: /home/me/projects/project_a

Following directives are supported:

 * autobazel-workspace
 * autobazel-package

**Examples**

.. code-block:: rst

   .. autobazel-workspace:: /home/me/projects/project_a

   .. autobazel-package:: /home/me/projects/project_a/package

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   domain
   autobazel



