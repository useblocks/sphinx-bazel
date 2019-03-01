.. _autobazel:

Autobazel
=========

Autobazel-directives allow the automatic documentation of Bazel workspaces, packages and targets.

All showed examples are based on the same Bazel example workspace, which structure and content is explained at
the end of this page: :ref:`project_example`.

.. contents::
   :local:

.. _autobazel_workspace:

autobazel-workspace
-------------------

Documents a whole Bazel workspace::

   .. autobazel-workspace: ./bazel_example

**Result**

.. autobazel-workspace:: bazel_example

If the given path is relative, the sphinx configuration folder is taken as basedir (the one which contains your
``conf.py`` file)


packages
~~~~~~~~

If ``:packages:`` is set, all found Bazel packages inside workspace will be printed as well::

    .. autobazel-workspace:: ./bazel_example
       :packages:

**Result**

.. autobazel-workspace:: ./bazel_example
   :packages:

targets
~~~~~~~~

If ``:targets:`` is set, all found Bazel targets inside found packages will be printed as well::

    .. autobazel-workspace:: ./bazel_example
       :packages:
       :targets:

Is only used, if ``:packages:`` is provided as well!

**Result**

.. autobazel-workspace:: ./bazel_example
   :packages:
   :targets:

hide
~~~~
If ``:hide:`` is set, information about the workspace itself will not be printed. But packages and co, if requested::

   .. autobazel-workspace:: ./bazel_example
       :hide:
       :packages:

**Result**

.. autobazel-workspace:: ./bazel_example
    :hide:
    :packages:

workspace
~~~~~~~~~

If ``:workspace`` is given, the workspace name will get added packages and targets::

   .. autobazel-workspace:: ./bazel_example
       :workspace:
       :packages:

**Result**

.. autobazel-workspace:: ./bazel_example
    :workspace:
    :packages:

workspace_path
~~~~~~~~~~~~~~

If ``:workspace_path`` is given, the workspace path will get added packages and targets::

   .. autobazel-workspace:: ./bazel_example
       :workspace_path:
       :packages:

**Result**

.. autobazel-workspace:: ./bazel_example
    :workspace_path:
    :packages:

.. _autobazel_package:

autobazel-package
-----------------

Documents a single Bazel package::

   .. autobazel-package:: //lib


**Result**

.. autobazel-package:: //lib

Sphinx-Bazel links all packages internally to a defined workspace, so that it is able to calculate needed folder and
file paths of the package.
Please be sure you have used ``autobazel-workspace`` or ``.. bazel:workspace::`` before starting to document
Bazel packages.


targets
~~~~~~~

If ``:targets:`` is set, all found Bazel targets inside given package will be printed::

    .. autobazel-package:: //main
       :targets:

**Result**

.. autobazel-package:: //main
   :targets:

hide
~~~~
If ``:hide:`` is set, information about the package itself will not be printed. But targets, if requested::

   .. autobazel-package:: //main
      :hide:
      :targets:

**Result**

.. autobazel-package:: //main
   :hide:
   :targets:

workspace
~~~~~~~~~

If ``:workspace`` is given, the workspace name will get added to package and targets::

   .. autobazel-package:: //main
      :workspace:
      :packages:

**Result**

.. autobazel-package:: //main
   :workspace:
   :packages:

workspace_path
~~~~~~~~~~~~~~

If ``:workspace_path`` is given, the workspace path will get added to package and targets::

   .. autobazel-package:: //main
      :workspace_path:
      :packages:

**Result**

.. autobazel-package:: //main
   :workspace_path:
   :packages:

.. _autobazel_target:

autobazel-target
----------------

Documents a single Bazel target::

   .. autobazel-target:: //main:hello-world.bzl


**Result**

.. autobazel-target:: //main:hello-world.bzl

Like in :ref:`autobazel_package` please make sure that a workspace got defined.

workspace
~~~~~~~~~

If ``:workspace`` is given, the workspace name will get added to package and targets::

   .. autobazel-target:: //main:hello-world.bzl
      :workspace:

**Result**

.. autobazel-target:: //main:hello-world.bzl
   :workspace:

workspace_path
~~~~~~~~~~~~~~

If ``:workspace_path`` is given, the workspace path will get added to package and targets::

   .. autobazel-target:: //main:hello-world.bzl
      :workspace_path:

**Result**

.. autobazel-target:: //main:hello-world.bzl
   :workspace_path:



.. _project_example:

Example project structure
-------------------------

The following project structure was used for the above examples::

   ./bazel_example
   ├── lib
   │   ├── BUILD
   │   ├── hello-time.cc
   │   └── hello-time.h
   ├── main
   │   ├── BUILD
   │   ├── hello-greet.cc
   │   ├── hello-greet.h
   │   ├── hello-world.bzl
   │   └── hello-world.cc
   └── WORKSPACE

This structure is coming from the original Bazel examples repository and was updated to provide more
internal documentation (e.g. docstrings):
https://github.com/bazelbuild/examples/

WORKSPACE content
~~~~~~~~~~~~~~~~~
.. literalinclude:: ./bazel_example/WORKSPACE
   :language: text


lib/BUILD content
~~~~~~~~~~~~~~~~~
.. literalinclude:: ./bazel_example/lib/BUILD
   :language: text

main/BUILD content
~~~~~~~~~~~~~~~~~~

.. literalinclude:: ./bazel_example/main/BUILD
   :language: text