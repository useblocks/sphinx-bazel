**Complete, rendered documentation**: http://sphinx-bazel.readthedocs.io/en/latest/

Sphinx-Bazel
============

Sphinx extension to provide information from bazel files to sphinx based documentations.


Installation
------------
.. code-block:: bash

   pip install sphinx-bazel


Usage
-----

Add ``sphinxcontrib.sphinx_bazel`` to the extension list of ``conf.py``::

   extensions = [
       'sphinx.ext.autodoc',
       'sphinx.ext.todo',
       'sphinx.ext.viewcode',
       'sphinxcontrib.sphinx_bazel',  # <-- That's our extension
   ]

Now you can start to use ``Sphinx-Bazel`` inside your project.

For instance open ``index.rst`` file and add::

   .. autobazel-workspace:: <path_to_bazel_workspace>
      :packages:

Where ``<path_to_bazel_workspace>`` must be an absolute path or a relative path to the location of the ``conf.py`` file
of your documentation project.

Fore more examples and a complete documentation, please visit http://sphinx-bazel.readthedocs.io/en/latest/