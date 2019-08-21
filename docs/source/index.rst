.. Sphinx-Bazel documentation master file, created by
   sphinx-quickstart on Mon Feb 18 12:08:31 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. |nbsp| unicode:: 0xA0
   :trim:

.. role:: underline
    :class: underline

.. only:: html

   .. image:: https://img.shields.io/pypi/l/sphinx-bazel.svg
       :target: https://pypi.python.org/pypi/sphinx-bazel
       :alt: License
   .. image:: https://img.shields.io/pypi/pyversions/sphinx-bazel.svg
       :target: https://pypi.python.org/pypi/sphinx-bazel
       :alt: Supported versions
   .. image:: https://readthedocs.org/projects/sphinx-bazel/badge/?version=latest
       :target: https://readthedocs.org/projects/sphinx-bazel/
   .. image:: https://travis-ci.org/useblocks/sphinx-bazel.svg?branch=master
       :target: https://travis-ci.org/useblocks/sphinx-bazel
       :alt: Travis-CI Build Status
   .. image:: https://img.shields.io/pypi/v/sphinx-bazel.svg
       :target: https://pypi.python.org/pypi/sphinx-bazel
       :alt: PyPI Package latest release

   .. image:: https://img.shields.io/badge/sphinx-1.5%2C%201.6%2C%201.7%2C%201.8%2C%202.0%2C%202.1-blue.svg
       :target: https://www.sphinx-doc.org
       :alt: Supported Sphinx releases

Sphinx-Bazel: rules inside sphinx
=================================

``Sphinx-Bazel`` is an extension for the `Sphinx documentation generator <http://sphinx-doc.org>`_ and allows the
**manual** or **automated** documentation of following `Bazel <https://bazel.build>`_ objects inside any Sphinx project:



.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :stub-columns: 1

   * - Bazel object
     - Manual documentation
     - Automated documentation
   * - Workspace
     - :ref:`domain_workspace`
     - :ref:`autobazel_workspace`
   * - └ Package
     - :ref:`domain_package`
     - :ref:`autobazel_package`
   * - |nbsp| |nbsp| |nbsp| └ Target
     - :ref:`domain_target`
     - :ref:`autobazel_target`
   * - |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| ├ Rule
     - :ref:`domain_rule`
     - :ref:`autobazel_rule`
   * - |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| │ |nbsp| └ Attr.
     - :ref:`domain_attribute`
     - :ref:`autobazel_attribute`
   * - |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| ├ Macro
     - :ref:`domain_macro`
     - :ref:`autobazel_macro`
   * - |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| └ Impl.
     - :ref:`domain_implementation`
     - :ref:`autobazel_implementation`

``Sphinx-Bazel`` supports and renders rst-syntax
(`reStructuredText <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_) in
`Docstrings <https://www.python.org/dev/peps/pep-0257/>`_ of the files ``WORKSPACE``, ``BUILD`` and any
target with file-extension ``.bzl``. It also parses the ``doc`` attribute from rule-definitions.


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

   .. bazel:package:: //main
      :workspace:

      Stores some code

   .. bazel:target:: //main:build
      :workspace_path:

      This **Bazel** target builds my sources.

**Result**

.. bazel:workspace:: my_workspace
   :path: c:\workspaces\project_x

   Stores *files* and everything else.

.. bazel:package:: //main
   :show_workspace:

   Stores some code.

.. bazel:target:: //main:build
   :show_workspace_path:

   This **Bazel** target builds my sources.


See :ref:`bazel_domain` for the complete documentation.


Motivation
----------

This Sphinx extension is based on the needs of a software development team inside a german automotive company.

The project team was searching a small and practical way to add project-specific information
(like requirements, test-cases, user manuals) to Bazel objects and accumulate this information inside a single
sphinx project.

``Sphinx-Bazel`` is part of a software bundle, which was designed to support the development of
ISO 26262 compliant software. Other tools are:
`sphinx-needs <https://sphinxcontrib-needs.readthedocs.io>`_,
`sphinx-test-reports <https://sphinx-test-reports.readthedocs.io>`_,
`tox-envreport <https://tox-envreport.readthedocs.io>`_ and
`metric-farmer <https://metricfarmer.readthedocs.io/en/latest/>`_.




Contents
--------

.. toctree::
   :maxdepth: 3

   quickstart
   domain
   autobazel
   changelog





