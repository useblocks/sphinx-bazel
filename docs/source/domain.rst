Bazel domain
============

Bazel Workspace
---------------

To describe a bazel workspace use ``bazel:workspace::`` ::

   .. bazel:workspace:: my_workspace_name

      Package content

This has no direct output, but following definitions of packages or targets are assigned to this workspace.

.. bazel:workspace:: my_workspace_name


Bazel Package
-------------

To describe a bazel package use ``bazel:package::``::

   .. bazel:package:: Package

      Package content

**Result**

.. bazel:package:: //testmy/package

   Package content