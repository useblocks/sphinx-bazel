"""
Bazel domain implementation for Sphinx.

Domain overview
===============

* **workspace**: contains the ``WORKSPACE`` file. Container for multiple packages

 * **package**: contains a ``BUILD`` file. Container for multiple targets

  * **target**: any file or .bzl-file. If last, following is available:
  
   * **rule**:  a defined rule inside a .bzl-file
   * **macro**: a defined macro-function inside a .bzl file
   
   
Domain directives
=================

* bazel-workspace
* bazel-package
* bazel-target
* bazel-rule
* bazel-macro
"""