.. Sphinx-Bazel documentation master file, created by
   sphinx-quickstart on Mon Feb 18 12:08:31 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Sphinx-Bazel: rules inside sphinx
=================================

``Sphinx-Bazel`` is an extension for the `sphinx documentation generator <hhtps://sphinx-doc.org>`_ and allows the
documentation of following `Bazel <https://bazel.build>`_ objects inside any sphinx project:

* Workspace
* Package
* Target

``Sphinx-Bazel`` provides a Bazel domain to Sphinx, which allows the manual documentation of Bazel objects:

* :ref:`domain_workspace`
* :ref:`domain_package`
* :ref:`domain_target`

For automated documentation of existing Bazel workspaces ``Sphinx-Bazel`` provides the following directives:

* :ref:`autobazel_workspace`
* :ref:`autobazel_package`
* :ref:`autobazel_target`


Automated documentation
-----------------------

.. code-block:: rst

   .. autobazel-workspace:: ./bazel_example
      :packages:
      :targets:

**Result**

.. autobazel-workspace:: ./bazel_example
      :packages:


Please take a look into :ref:`autobazel` for the complete documentation.


Manual documentation
--------------------

.. code-block:: rst

   .. bazel:workspace:: my_workspace
      :path: c:\workspaces\project_x

      Stores *files* and everything else.

   .. bazel:target:: //main
      :workspace:

      Stores some _code_

   .. bazel:target:: //main:build
      :workspace_path:

      This **Bazel** target builds my sources.

**Result**

.. bazel:workspace:: my_workspace
   :path: c:\workspaces\project_x

   Stores *files* and everything else.

.. bazel:target:: //main
   :workspace:

   Stores some code.

.. bazel:target:: //main:build
   :workspace_path:

   This **Bazel** target builds my sources.


See :ref:`bazel_domain` for the complete documentation.

Contents
--------

.. toctree::
   :maxdepth: 3

   domain
   autobazel





