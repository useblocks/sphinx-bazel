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
* Rule
* Macro

The documentation can be written by hand or can be generated automatically based on existing Bazel folders and files.

Manual documentation
--------------------

.. code-block:: rst

   .. bazel:rule:: My Bazel rule

      This **Bazel** rule builds my sources.

Following domain-specific directives are provided:

 * bazel:workspace
 * bazel:package
 * bazel:target
 * bazel:rule
 * bazel:macro

**Examples**

.. code-block:: rst

   .. bazel:workspace:: My workspace

   .. bazel:package:: My package

   .. bazel:target:: My target

   .. bazel:rule:: My rule

   .. bazel:macro:: My macro


Automated documentation
-----------------------

.. code-block:: rst

   .. autobazel-rule:: //workspace//package/my_rule.blz::rule_one

Following directives are supported:

 * autobazel-workspace
 * autobazel-package
 * autobazel-target
 * autobazel-rule
 * autobazel-macro

**Examples**

.. code-block:: rst

   .. autobazel-workspace:: My workspace

   .. autobazel-package:: My package

   .. autobazel-target:: My target

   .. autobazel-rule:: My rule

   .. autobazel-macro:: My macro

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   domain
   autobazel



