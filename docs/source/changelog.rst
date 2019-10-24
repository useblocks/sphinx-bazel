Changelog
=========

0.1.4
-----

* Bugfix: Various smaller bug fixes.

0.1.3
-----

* Improvement: :ref:`autobazel_package` now supports option :ref:`option_packages` to document nested packages.
* Improvement:  regular expression support for :ref:`option_packages` and :ref:`option_targets` (`#1 <https://github.com/useblocks/sphinx-bazel/issues/1>`_)
* Bugfix: Fixed ``:hide:`` handling for :ref:`autobazel_workspace`.
* Bugfix: Fixed error handling if target signature for :ref:`autobazel_target` is not valid.


0.1.2
-----

* Improvement: Added :ref:`option_raw` to stop rendering doc_strings.
* Improvement: Added :ref:`option_show_type` for autobazel and  :ref:`domain_option_show_type` for the domain
  to show the type of the object as prefix.
* Bugfix: Several minor fixes to  get a stable parsing of bazel-files.

0.1.1
-----

* Improvement: Added :ref:`domain_attribute` to document rule attributes
* Improvement: Added :ref:`autobazel_attribute` to automatically load attributes
* Improvement: Option :ref:`option_attributes` added to print attributes
* Improvement: Options :ref:`rule_invocation` and :ref:`rule_show_invocation` added to define and show invocations
  strings for rules, macros and implementations.
* Improvement: Option :ref:`option_name` added to define specific workspace names
* Improvement: Option :ref:`option_path` added to support documentation of Bazel objects without a valid workspace
  (`#6 <https://github.com/useblocks/sphinx-bazel/issues/6>`_)
* Bugfix: Better warnings, if package not found (`#13 <https://github.com/useblocks/sphinx-bazel/issues/13>`_)
* Bugfix: No Python file parsing anymore (`#10 <https://github.com/useblocks/sphinx-bazel/issues/10>`_)
* Bugfix: WORKSPACE file can be empty (`#5 <https://github.com/useblocks/sphinx-bazel/issues/5>`_)


0.1.0
-----

* Initial version
