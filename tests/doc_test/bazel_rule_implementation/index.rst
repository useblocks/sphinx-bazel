TEST DOCUMENT
=============

.. bazel:workspace:: workspace_rule_impl_example

   Workspace for testing ``implementation`` option

.. bazel:rule:: //my/package:target:rule
   :implementation: __my_rule_func
   :show_implementation:

   Some input