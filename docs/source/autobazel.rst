autobazel
=========

Autobazel-directives allow the automatically documentation of Bazel workspaces, packages and targets.

The showed examples here document always the same exmpale workspace, which structure and content is explained at
the end of this page: :ref:`project_example`.

.. contents::
   :local:


autobazel-workspace
-------------------

Documents a whole Bazel workspace::

   .. autobazel-workspace: ./bazel_example


**Result**

.. autobazel-workspace:: bazel_example


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




autobazel-package
-----------------

Documents a single Bazel package::

   .. autobazel-package:: //lib


**Result**

.. autobazel-package:: //lib

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