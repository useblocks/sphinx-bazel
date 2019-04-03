TEST DOCUMENT
=============

.. bazel:package:: //domain_package/main
   :path: ./domain_package-bazel-example
   :show_workspace_path:

   domain_package_test_data

.. bazel:target:: //domain_target/main:target
   :path: ./domain_target-bazel-example
   :show_workspace_path:

   domain_target_test_data

.. bazel:rule:: //domain_rule/main:target:rule
   :path: ./domain_rule-bazel-example
   :show_workspace_path:

   domain_rule_test_data


.. autobazel-package:: //main
   :path: ./bazel_example
   :show_workspace:
   :targets:
   :rules:

