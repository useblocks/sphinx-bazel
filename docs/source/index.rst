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

``Sphinx-Bazel`` supports and renders rst-syntax
(`reStructuredText <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_) in
`Docstrings <https://www.python.org/dev/peps/pep-0257/>`_ of the files ``WORKSPACE``, ``BUILD`` and any
target with file-extension ``.py`` or ``.bzl``.


Automated documentation
-----------------------

.. code-block:: rst

   .. autobazel-workspace:: ./bazel_example
      :packages:

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


Motivation
----------

This sphinx extension is based on the needs of a software development team inside a german automotive company.

The project team was searching a small and practical way to add project-specific information
(like requirements, test-cases, user manuals) to Bazel objects and accumulate this information inside a single
sphinx project.

``Sphinx-Bazel`` is part of a software bundle, which was designed to support the development of
ISO 26262 compliant software. Other tools are:
`sphinx-need <https://sphinxcontrib-needs.readthedocs.io>`_,
`sphinx-test-reports <https://sphinx-test-reports.readthedocs.io>`_ and
`tox-envreport <https://tox-envreport.readthedocs.io>`_.


Contents
--------

.. toctree::
   :maxdepth: 3

   domain
   autobazel





