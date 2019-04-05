.. _autobazel:

Autobazel
=========

Autobazel-directives allow the automatic documentation of Bazel workspaces, packages, targets, rules, marcos,
implementations and rule attributes.

All showed examples are based on the same Bazel example workspace, which structure and content is explained at
the end of this page: :ref:`project_example`.

.. contents::
   :local:

.. _autobazel_workspace:

autobazel-workspace
-------------------

Documents a whole Bazel workspace::

   .. autobazel-workspace:: ./bazel_example

**Result**

.. autobazel-workspace:: bazel_example

If the given path is relative, the sphinx configuration folder is taken as basedir (the one which contains your
``conf.py`` file)

.. _autobazel_package:

autobazel-package
-----------------

Documents a single Bazel package::

   .. autobazel-package:: //lib


**Result**

.. autobazel-package:: //lib

Sphinx-Bazel links all packages internally to a defined workspace, so that it is able to calculate needed folder and
file paths of the package.
Please be sure you use ``autobazel-workspace``, ``.. bazel:workspace::`` or :ref:`option_path` to define the
location of the workspace to use.

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

.. _autobazel_macro:

autobazel-macro
---------------

Documents a single Bazel macro::

   .. autobazel-macro:: //main:hello-world.bzl:custom_macro


**Result**

.. autobazel-macro:: //main:hello-world.bzl:custom_macro

Like in :ref:`autobazel_package` please make sure that a workspace got defined.

``autobazel-macro`` uses the docstring of the function/macro as macro description.

.. _autobazel_implementation:

autobazel-implementation
------------------------

Documents a Bazel implementation of a rule::

   .. autobazel-implementation:: //main:hello-world.bzl:__impl_custom_build_rule


**Result**

.. autobazel-implementation:: //main:hello-world.bzl:__impl_custom_build_rule

Like in :ref:`autobazel_package` please make sure that a workspace got defined.

``autobazel-implementation`` uses the docstring of the implementation as implementation description.

.. _autobazel_attribute:

autobazel-attribute
-------------------

Documents a specific Bazel rule attribute::

   .. autobazel-attribute:: //main:hello-world.bzl:custom_build_rule:package_script


**Result**

.. autobazel-attribute:: //main:hello-world.bzl:custom_build_rule:package_script


``autobazel-attribute`` searches for docstrings in the doc-attribute of an attribute.

Options
-------

Most options are supported by the above directives, as they are very common.
However, some are not. So here is an overview about which autobazel directive supports what kind of options.

Used abbreviations: ws=workspace, pack=package, targ=target, impl=implementation, attr=attribute

.. list-table::
   :header-rows: 1

   * - Option/autobazel-...
     - ws
     - pack
     - targ
     - rule
     - macro
     - impl
     - attr
   * - :ref:`option_path`
     - ⛔
     - 👍
     - 👍
     - 👍
     - 👍
     - 👍
     - 👍
   * - :ref:`option_name`
     - 👍
     - ⛔
     - ⛔
     - ⛔
     - ⛔
     - ⛔
     - ⛔
   * - :ref:`option_packages`
     - 👍
     - ⛔
     - ⛔
     - ⛔
     - ⛔
     - ⛔
     - ⛔
   * - :ref:`option_targets`
     - 👍
     - 👍
     - ⛔
     - ⛔
     - ⛔
     - ⛔
     - ⛔
   * - :ref:`option_rules`
     - 👍
     - 👍
     - 👍
     - ⛔
     - ⛔
     - ⛔
     - ⛔
   * - :ref:`option_macros`
     - 👍
     - 👍
     - 👍
     - ⛔
     - ⛔
     - ⛔
     - ⛔
   * - :ref:`option_implementations`
     - 👍
     - 👍
     - 👍
     - ⛔
     - ⛔
     - ⛔
     - ⛔
   * - :ref:`option_attributes`
     - 👍
     - 👍
     - 👍
     - 👍
     - ⛔
     - ⛔
     - ⛔
   * - :ref:`option_hide`
     - 👍
     - 👍
     - 👍
     - 👍
     - 👍
     - 👍
     - 👍
   * - :ref:`option_show_implementation`
     - 👍
     - 👍
     - 👍
     - 👍
     - ⛔
     - ⛔
     - ⛔
   * - :ref:`option_show_workspace`
     - 👍
     - 👍
     - 👍
     - 👍
     - 👍
     - 👍
     - 👍
   * - :ref:`option_show_workspace_path`
     - 👍
     - 👍
     - 👍
     - 👍
     - 👍
     - 👍
     - 👍

.. _option_path:

path
~~~~

.. list-table::
   :header-rows: 1

   * - ws
     - pack
     - targ
     - rule
     - macro
     - impl.
     - attr
   * - ⛔
     - 👍
     - 👍
     - 👍
     - 👍
     - 👍
     - 👍

If ``:path:`` is set, Sphinx-Bazel checks this folder directly without the need of a valid or existing Bazel workspace.

The following example package path is created from ``path`` + ``autobazel_package argument``::

    .. autobazel-package:: //main
       :path: ./bazel_example/
       :show_workspace_path:

This will look for a **BUILD** file in ``./bazel_examples/main``.

**Result**

.. autobazel-package:: //main
   :path: ./bazel_example/
   :show_workspace_path:

**Usage**

The normal way is to **not use** this option and use :ref:`autobazel_workspace` or :ref:`domain_workspace` instead.
These directives will create a workspace internally and all following directives like :ref:`autobazel_target` or
:ref:`domain_rule`: will use this workspace as reference automatically.

However, there may be use cases where a workspace does not exist (e.g. single .bzl. files in a git submodule).
In this cases this option can help.

.. _option_name:

name
~~~~

.. list-table::
   :header-rows: 1

   * - ws
     - pack
     - targ
     - rule
     - macro
     - impl.
     - attr
   * - 👍
     - ⛔
     - ⛔
     - ⛔
     - ⛔
     - ⛔
     - ⛔

``:name:`` can be used to define a specific name of a workspace.

Normally the name gets read from the ``WORKSPACE`` file. If no name is defined or there are reasons to
document workspaces with similar names, use ``:name``::

    .. autobazel-workspace:: ./bazel_example/
       :name: my custom workspace name
       :show_workspace_path:
       :show_workspace:

**Result**

.. autobazel-workspace:: ./bazel_example/
   :name: my custom workspace name
   :show_workspace_path:
   :show_workspace:

.. note::

   This documentation uses the same workspace ``bazel_example`` several times on the same page.
   To avoid warnings like ``WARNING: Duplicate ID: "workspace-hello_world_workspace"``, we use ``:name:`` to import
   the same workspace multiple times under different names.


.. _option_packages:

packages
~~~~~~~~

.. list-table::
   :header-rows: 1

   * - ws
     - pack
     - targ
     - rule
     - macro
     - impl.
     - attr
   * - 👍
     - ⛔
     - ⛔
     - ⛔
     - ⛔
     - ⛔
     - ⛔

If ``:packages:`` is set, all found Bazel packages inside workspace will be printed as well::

    .. autobazel-workspace:: ./bazel_example
       :packages:

**Result**

.. autobazel-workspace:: ./bazel_example
   :name: ws_package_example
   :packages:

.. _option_targets:

targets
~~~~~~~~

.. list-table::
   :header-rows: 1

   * - ws
     - pack
     - targ
     - rule
     - macro
     - impl.
     - attr
   * - 👍
     - 👍
     - ⛔
     - ⛔
     - ⛔
     - ⛔
     - ⛔


If ``:targets:`` is set, all found Bazel targets inside found packages will be printed as well::

    .. autobazel-package:: //main
       :path: ./bazel_example
       :targets:

**Result**

.. autobazel-package:: //main
   :path: ./bazel_example
   :targets:

.. _option_rules:

rules
~~~~~

.. list-table::
   :header-rows: 1

   * - ws
     - pack
     - targ
     - rule
     - macro
     - impl.
     - attr
   * - 👍
     - 👍
     - 👍
     - ⛔
     - ⛔
     - ⛔
     - ⛔

If ``:rules:`` is set, all found rules inside targets with extension ``.bzl`` files will be printed ::

    .. autobazel-target:: //main:hello-world.bzl
       :path: ./bazel_example
       :rules:

**Result**

.. autobazel-target:: //main:hello-world.bzl
   :path: ./bazel_example
   :rules:

.. _option_macros:

macros
~~~~~~

.. list-table::
   :header-rows: 1

   * - ws
     - pack
     - targ
     - rule
     - macro
     - impl.
     - attr
   * - 👍
     - 👍
     - 👍
     - ⛔
     - ⛔
     - ⛔
     - ⛔

If ``:macros:`` is set, all found macros inside targets with extension ``.bzl`` files will be printed ::

    .. autobazel-target:: //main:hello-world.bzl
       :path: ./bazel_example
       :macros:

Is only used, if ``:packages:`` and ``:targets:`` are provided as well!

**Result**

.. autobazel-target:: //main:hello-world.bzl
   :path: ./bazel_example
   :macros:

.. _option_implementations:

implementations
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - ws
     - pack
     - targ
     - rule
     - macro
     - impl.
     - attr
   * - 👍
     - 👍
     - 👍
     - ⛔
     - ⛔
     - ⛔
     - ⛔

If ``:implementations:`` is set, all found implementations inside targets with extension ``.bzl`` files will be printed ::

    .. autobazel-target:: //main:hello-world.bzl
       :path: ./bazel_example
       :implementations:

**Result**

.. autobazel-target:: //main:hello-world.bzl
   :path: ./bazel_example
   :implementations:

.. _option_attributes:

attributes
~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - ws
     - pack
     - targ
     - rule
     - macro
     - impl.
     - attr
   * - 👍
     - 👍
     - 👍
     - 👍
     - ⛔
     - ⛔
     - ⛔

If ``:attributes:`` is set, all found attributes of a rule will be printed ::

    .. autobazel-rule:: //main:hello-world.bzl:custom_build_rule
       :path: ./bazel_example
       :attributes:

**Result**

.. autobazel-rule:: //main:hello-world.bzl:custom_build_rule
   :path: ./bazel_example
   :attributes:


.. _option_hide:

hide
~~~~

.. list-table::
   :header-rows: 1

   * - ws
     - pack
     - targ
     - rule
     - macro
     - impl.
     - attr
   * - 👍
     - 👍
     - 👍
     - 👍
     - 👍
     - 👍
     - 👍

If ``:hide:`` is set, information about the workspace itself will not be printed. But packages and co, if requested::

   .. autobazel-workspace:: ./bazel_example
       :hide:
       :packages:

**Result**

.. autobazel-workspace:: ./bazel_example
    :name: ws_hide_example
    :hide:
    :packages:

.. _option_show_implementation:

show_implementation
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - ws
     - pack
     - targ
     - rule
     - macro
     - impl.
     - attr
   * - 👍
     - 👍
     - 👍
     - 👍
     - 👍
     - 👍
     - 👍

If ``show_implementation`` is given, the name of the implementation function of found rules gets printed::

    .. autobazel-rule:: //main:hello-world.bzl:custom_build_rule
       :path: ./bazel_example
       :show_implementation:

**Result**

.. autobazel-rule:: //main:hello-world.bzl:custom_build_rule
   :path: ./bazel_example
   :show_implementation:

.. _option_show_workspace:

show_workspace
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - ws
     - pack
     - targ
     - rule
     - macro
     - impl.
     - attr
   * - 👍
     - 👍
     - 👍
     - 👍
     - 👍
     - 👍
     - 👍

If ``:show_workspace`` is given, the workspace name will get added::

   .. autobazel-workspace:: ./bazel_example
      :show_workspace:
      :packages:

**Result**

.. autobazel-workspace:: ./bazel_example
   :name: ws_show_workspace_example
   :show_workspace:
   :packages:

.. _option_show_workspace_path:

show_workspace_path
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - ws
     - pack
     - targ
     - rule
     - macro
     - impl.
     - attr
   * - 👍
     - 👍
     - 👍
     - 👍
     - 👍
     - 👍
     - 👍

If ``:workspace_path`` is given, the workspace path will get added packages and targets::

   .. autobazel-attribute:: //main:hello-world.bzl:custom_build_rule:package_script
      :path: ./bazel_example
      :show_workspace_path:

**Result**

.. autobazel-attribute:: //main:hello-world.bzl:custom_build_rule:package_script
   :path: ./bazel_example
   :show_workspace_path:


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

Complete documentation
~~~~~~~~~~~~~~~~~~~~~~

The following documentation of the complete Bazel Workspace uses nearly every available option::

    .. autobazel-workspace:: ./bazel_example
       :name: ws_full_example
       :packages:               // from here content options
       :targets:
       :rules:
       :macros:
       :implementations:
       :attributes:
       :show_workspace:         // from here layout options only
       :show_workspace_path:
       :show_implementation:

**Result**

.. autobazel-workspace:: ./bazel_example
   :name: ws_full_example
   :packages:
   :targets:
   :rules:
   :macros:
   :implementations:
   :attributes:
   :show_workspace:
   :show_workspace_path:
   :show_implementation:
