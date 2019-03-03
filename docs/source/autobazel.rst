.. _autobazel:

Autobazel
=========

Autobazel-directives allow the automatic documentation of Bazel workspaces, packages, targets and rules.

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

rules
~~~~~

If ``:rules:`` is set, all found rules inside targets with extension ``.bzl`` files will be printed ::

    .. autobazel-workspace:: ./bazel_example
       :packages:
       :targets:
       :rules:

Is only used, if ``:packages:`` and ``:targets:`` are provided as well!

**Result**

.. autobazel-workspace:: ./bazel_example
   :packages:
   :targets:
   :rules:

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

implementation
~~~~~~~~~~~~~~
If ``implementation`` is given, the name of the implementation function of found rules gets printed::

    .. autobazel-workspace:: ./bazel_example
       :packages:
       :targets:
       :rules:
       :implementation:

**Result**

.. autobazel-workspace:: ./bazel_example
   :packages:
   :targets:
   :rules:
   :implementation:

``:implementation:`` is only used if also ``:rules``, ``:targets:`` and ``:packages`` are set.

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

rules
~~~~~

If ``:rules:`` is set, all found rules inside targets with extension ``.bzl`` files will be printed ::

    .. autobazel-package:: //main
       :targets:
       :rules:

Is only used, if ``:targets:`` is provided as well!

**Result**

.. autobazel-package:: //main
   :targets:
   :rules:


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

implementation
~~~~~~~~~~~~~~
If ``implementation`` is given, the name of the implementation function of found rules gets printed::

    .. autobazel-package:: //main
       :targets:
       :rules:
       :implementation:

**Result**

.. autobazel-package:: //main
   :targets:
   :rules:
   :implementation:

``:implementation:`` is only used if also ``:rules`` and ``:targets:`` are set.

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

``autobazel-target`` searches for docstrings in files with extension ``.py`` or ``.bzl`` and use this as
target-description. Other file-extension are not supported, as they normally do not follow the Python syntax.

rules
~~~~~

If ``:rules:`` is set, all found rules inside given target  will be printed::

    .. autobazel-target:: //main:hello-world.bzl
       :rules:

``Sphinx-Bazel`` checks only targets with ``.bzl`` as file extension for rules.

**Result**

.. autobazel-target:: //main:hello-world.bzl
   :rules:

implementation
~~~~~~~~~~~~~~
If ``implementation`` is given, the name of the implementation function of found rules gets printed::

    .. autobazel-target:: //main:hello-world.bzl
       :rules:
       :implementation:

**Result**

.. autobazel-target:: //main:hello-world.bzl
   :rules:
   :implementation:

``:implementation:`` is only used if also ``:rules`` is set to document the containing rules of target.

workspace
~~~~~~~~~

If ``:workspace`` is given, the workspace name will get added to target::

   .. autobazel-target:: //main:hello-world.bzl
      :workspace:

**Result**

.. autobazel-target:: //main:hello-world.bzl
   :workspace:

workspace_path
~~~~~~~~~~~~~~

If ``:workspace_path`` is given, the workspace path will get added to target::

   .. autobazel-target:: //main:hello-world.bzl
      :workspace_path:

**Result**

.. autobazel-target:: //main:hello-world.bzl
   :workspace_path:


.. _autobazel_rule:

autobazel-rule
--------------

Documents a single Bazel rule::

   .. autobazel-rule:: //main:hello-world.bzl:custom_build_rule


**Result**

.. autobazel-rule:: //main:hello-world.bzl:custom_build_rule

Like in :ref:`autobazel_package` please make sure that a workspace got defined.

``autobazel-rule`` searches for docstrings in the doc-attribute of a rule defined in files with
extension ``.bzl``. This is then used as rule description.

implementation
~~~~~~~~~~~~~~
If ``implementation`` is given, the name of the function which is used in the **implementation** attribute
of the rule definition is printed out::

    .. autobazel-rule:: //main:hello-world.bzl:custom_build_rule
       :implementation:

**Result**

.. autobazel-rule:: //main:hello-world.bzl:custom_build_rule
   :implementation:

workspace
~~~~~~~~~

If ``:workspace`` is given, the workspace name will get added to rule::

   .. autobazel-rule:: //main:hello-world.bzl:custom_build_rule
      :workspace:

**Result**

.. autobazel-rule:: //main:hello-world.bzl:custom_build_rule
   :workspace:

workspace_path
~~~~~~~~~~~~~~

If ``:workspace_path`` is given, the workspace path will get added to rule::

   .. autobazel-rule:: //main:hello-world.bzl:custom_build_rule
      :workspace_path:

**Result**

.. autobazel-rule:: //main:hello-world.bzl:custom_build_rule
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

main/hello-world.bzl content
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ./bazel_example/main/hello-world.bzl
   :language: text