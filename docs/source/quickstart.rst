Quickstart
==========

Installation
------------

Open a command line interface and type::

   pip install sphinx-bazel


If you like, you can also use the latest, unreleased code from our repository instead::

   git clone https://github.com/useblocks/sphinx-bazel
   cd sphinx-bazel
   pip install -e .

The above commands will install ``Sphinx-Bazel`` including all dependencies like **Sphinx** itself.

Project setup
-------------

After installation you can use ``Sphinx-Bazel`` inside existing Sphinx projects or create a new project via::

   sphinx-quickstart

Answer the questions by your needs and ``sphinx-quickstart`` will create a new, working project for you.

Then open the ``conf.py`` file to add ``Sphinx-Bazel`` support. All you need to do is to add
``sphinxcontrib.sphinx_bazel`` to the extension list::

   extensions = [
       'sphinx.ext.autodoc',
       'sphinx.ext.todo',
       'sphinx.ext.viewcode',
       'sphinxcontrib.sphinx_bazel',  # <-- That's our extension
   ]

After this call ``make html`` to generate the html output of the fresh project.
You will find the output under ``_build/html/``.

As alternative to **make** you can also call ``sphinx-build`` directly::

   sphinx-build -b html . _build/html

Document Bazel
--------------

Now you can start to use ``Sphinx-Bazel`` inside your project.

For instance open ``index.rst`` file and add::

   .. autobazel-workspace:: <path_to_bazel_workspace>
      :packages:

Where ``<path_to_bazel_workspace>`` must be an absolute path or a relative path to the location of the ``conf.py`` file
of your documentation project.


For more options and ideas how to document your Bazel project, please read :ref:`autobazel` and :ref:`bazel_domain`.

